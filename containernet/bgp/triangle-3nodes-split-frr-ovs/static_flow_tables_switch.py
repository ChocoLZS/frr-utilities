# Copyright (C) 2011 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3, inet
from ryu.lib.packet import packet, ethernet, arp, tcp
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.topology import event

from ryu.lib.packet import tcp, packet_base

TCP = tcp.tcp.__name__

LOCAL_PORT = ofproto_v1_3.OFPP_LOCAL
LOCAL_PORT = 1


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        # 提前记录交换机的邻居arp表
        self.mac_to_port = {}
        # 每一个交换机都有其邻居的arp表
        self.arp_table = {}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # 1. ARP -> 控制器
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_ARP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 20, match, actions)

    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(
                datapath=datapath,
                buffer_id=buffer_id,
                priority=priority,
                match=match,
                instructions=inst,
            )
        else:
            mod = parser.OFPFlowMod(
                datapath=datapath, priority=priority, match=match, instructions=inst
            )
        datapath.send_msg(mod)

    def _extract_ev(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.match["in_port"]
        pkt = packet.Packet(msg.data)
        return msg, datapath, in_port, pkt

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        print("--------------------------")
        print(ev.timestamp)
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug(
                "packet truncated: only %s of %s bytes",
                ev.msg.msg_len,
                ev.msg.total_len,
            )
        msg, datapath, in_port, pkt = self._extract_ev(ev)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        eth = pkt.get_protocols(ethernet.ethernet)[0]
        print(pkt.protocols)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data
        # ARP 处理：控制器代理回复
        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            is_handled = self._handle_arp(ev)
            if is_handled:
                return

        # 广播包（一般是 ARP 请求)
        if dst == "ff:ff:ff:ff:ff:ff":
            print("[BROADCAST] Received unhandled ARP broadcast")
            return

        print("packet in", hex(dpid), src, dst, in_port)
        print("--------------------------")
        actions = []
        if dst in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst]
            actions = [parser.OFPActionOutput(out_port)]

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    def _handle_arp(self, ev) -> bool:
        msg, datapath, in_port, pkt = self._extract_ev(ev)
        dpid = datapath.id
        parser = datapath.ofproto_parser
        ofproto = datapath.ofproto
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        src = eth.src
        dst = eth.dst
        arp_pkt = pkt.get_protocol(arp.arp)
        src_ip = arp_pkt.src_ip
        dst_ip = arp_pkt.dst_ip
        print(
            f"[ARP] [{hex(dpid)}] Received ARP packet from {src_ip} to {dst_ip}, port: {in_port}"
        )
        data = None
        if msg.buffer_id == datapath.ofproto.OFP_NO_BUFFER:
            data = msg.data

        if dpid not in self.mac_to_port:
            self.mac_to_port[dpid] = {}
        if src not in self.mac_to_port[dpid]:
            self.mac_to_port[dpid][src] = in_port
            self.add_flow(
                datapath,
                10,
                parser.OFPMatch(eth_dst=src),
                [parser.OFPActionOutput(in_port)],
            )
            print(
                f"[MAC] [{hex(dpid)}] Learning: {src} is at {in_port}: {self.mac_to_port}"
            )

        # 学习发送方 IP 对应的 MAC 地址
        self.arp_table[src_ip] = src
        print(f"[ARP] Learning: {src_ip} is at {src}")
        if arp_pkt.opcode == arp.ARP_REQUEST:
            if dst_ip in self.arp_table:
                dst_mac = self.arp_table[dst_ip]
                print(f"[ARP] [{hex(dpid)}] Replying: {dst_ip} is at {dst_mac}")
                self.send_arp_reply(datapath, src, src_ip, dst_mac, dst_ip, in_port)
                return True
            else:
                # flood to neighbor
                print(f"[ARP] [{hex(dpid)}] Flooding: {dst_ip} is not in ARP table")
                # 如果是主机的请求，并且没命中arp table，向邻居一跳节点泛洪
                if in_port == LOCAL_PORT:
                    # flood to all neighbors except in_port
                    print(
                        f"[ARP] [{hex(dpid)}] Flooding to all neighbors except {in_port}"
                    )
                    out_port = ofproto.OFPP_FLOOD
                    actions = [parser.OFPActionOutput(out_port)]
                    out = parser.OFPPacketOut(
                        datapath=datapath,
                        buffer_id=msg.buffer_id,
                        in_port=in_port,
                        actions=actions,
                        data=data,
                    )
                    datapath.send_msg(out)
                    return True
                # 如果不是主机的请求，说明来自邻居节点，往主机发送即可
                else:
                    print(
                        f"[ARP] [{hex(dpid)}] Received ARP request from {in_port}, send to host"
                    )
                    # send to host
                    out_port = LOCAL_PORT
                    actions = [parser.OFPActionOutput(out_port)]
                    out = parser.OFPPacketOut(
                        datapath=datapath,
                        buffer_id=msg.buffer_id,
                        in_port=in_port,
                        actions=actions,
                        data=data,
                    )
                    datapath.send_msg(out)
                    return True
        if arp_pkt.opcode == arp.ARP_REPLY:
            print(f"[ARP] [{hex(dpid)}] Received ARP reply from {src_ip} to {dst_ip}")
            self.send_arp_reply(datapath, src, src_ip, dst, dst_ip, in_port)
            return True
        return False

    def send_arp_reply(
        self, datapath, target_mac, target_ip, src_mac, src_ip, out_port
    ):
        pkt = packet.Packet()
        pkt.add_protocol(
            ethernet.ethernet(
                ethertype=ether_types.ETH_TYPE_ARP, dst=target_mac, src=src_mac
            )
        )
        pkt.add_protocol(
            arp.arp(
                opcode=arp.ARP_REPLY,
                src_mac=src_mac,
                src_ip=src_ip,
                dst_mac=target_mac,
                dst_ip=target_ip,
            )
        )
        pkt.serialize()

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=datapath.ofproto.OFP_NO_BUFFER,
            in_port=datapath.ofproto.OFPP_CONTROLLER,
            actions=actions,
            data=pkt.data,
        )
        datapath.send_msg(out)
