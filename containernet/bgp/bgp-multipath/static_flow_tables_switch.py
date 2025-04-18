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

from ryu.lib.packet import tcp, packet_base

TCP = tcp.tcp.__name__


class SimpleSwitch13(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        # 提前记录交换机的邻居arp表
        self.mac_to_port = {
            0x11: {
                "00:00:00:00:00:12": 12,
                "00:00:00:00:00:11": 1,
            },
            0x12: {
                "00:00:00:00:00:11": 11,
                "00:00:00:00:00:12": 1,
                "00:00:00:00:00:21": 21,
                "00:00:00:00:00:22": 22,
            },
            0x21: {
                "00:00:00:00:00:12": 12,
                "00:00:00:00:00:23": 23,
                "00:00:00:00:00:21": 1,
            },
            0x22: {
                "00:00:00:00:00:12": 12,
                "00:00:00:00:00:23": 23,
                "00:00:00:00:00:22": 1,
            },
            0x23: {
                "00:00:00:00:00:21": 21,
                "00:00:00:00:00:22": 22,
                "00:00:00:00:00:23": 1,
                "00:00:00:00:00:31": 31,
                "00:00:00:00:00:32": 32,
            },
            0x31: {
                "00:00:00:00:00:23": 23,
                "00:00:00:00:00:33": 33,
                "00:00:00:00:00:31": 1,
            },
            0x32: {
                "00:00:00:00:00:23": 23,
                "00:00:00:00:00:33": 33,
                "00:00:00:00:00:32": 1,
            },
            0x33: {
                "00:00:00:00:00:31": 31,
                "00:00:00:00:00:32": 32,
                "00:00:00:00:00:33": 1,
            },
        }
        # 每一个交换机都有其邻居的arp表
        self.arp_table = {
            "1.0.1.1": "00:00:00:00:00:11",
            "1.0.1.2": "00:00:00:00:00:12",
            "2.0.2.1": "00:00:00:00:00:21",
            "2.0.2.2": "00:00:00:00:00:22",
            "2.0.2.3": "00:00:00:00:00:23",
            "3.0.3.1": "00:00:00:00:00:31",
            "3.0.3.2": "00:00:00:00:00:32",
            "3.0.3.3": "00:00:00:00:00:33",
            # r11
            "10.11.12.1": "00:00:00:00:00:11",
            # r12
            "10.11.12.2": "00:00:00:00:00:12",
            "10.12.21.1": "00:00:00:00:00:12",
            "10.12.22.1": "00:00:00:00:00:12",
            # r21
            "10.12.21.2": "00:00:00:00:00:21",
            "10.21.23.1": "00:00:00:00:00:21",
            # r22
            "10.12.22.2": "00:00:00:00:00:22",
            "10.22.23.1": "00:00:00:00:00:22",
            # r23
            "10.21.23.2": "00:00:00:00:00:23",
            "10.22.23.2": "00:00:00:00:00:23",
            "10.23.31.1": "00:00:00:00:00:23",
            "10.23.32.1": "00:00:00:00:00:23",
            # r31
            "10.23.31.2": "00:00:00:00:00:31",
            "10.31.33.1": "00:00:00:00:00:31",
            # r32
            "10.23.32.2": "00:00:00:00:00:32",
            "10.32.33.1": "00:00:00:00:00:32",
            # r33
            "10.31.33.2": "00:00:00:00:00:33",
            "10.32.33.2": "00:00:00:00:00:33",
            # host
            "101.1.1.1": "00:00:00:00:00:11",
            "103.3.3.1": "00:00:00:00:00:33",
        }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.

        """
        默认丢包
        阻止ovs接口产生的ipv6 mld、nd包
        """
        match = parser.OFPMatch()
        actions = []
        self.add_flow(datapath, 0, match, actions)

        # 1. ARP -> 控制器
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_ARP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)]
        self.add_flow(datapath, 10, match, actions)

        """
        捕获所有tcp包，并发送至控制器
        """
        macth_tcp = parser.OFPMatch(
            eth_type=ether_types.ETH_TYPE_IP, ip_proto=inet.IPPROTO_TCP
        )
        """
        1. OFPP_NORMAL: 发送至交换机的正常处理流程
        2. OFPP_CONTROLLER: 发送至控制器（而且控制器只分析，并不处理）
        """
        actions_tcp = [
            parser.OFPActionOutput(ofproto.OFPP_NORMAL, ofproto.OFPCML_NO_BUFFER),
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER),
        ]
        self.add_flow(datapath, 1, macth_tcp, actions_tcp)

        # """
        # drop ipv6 包
        # """
        # match_ipv6 = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_IPV6)
        # # actions_ipv6 = [parser.OFPActionOutput(ofproto.OFPMBT_DROP)]
        # self.add_flow(datapath, 1, match_ipv6, actions=[])
        """
        给每个switch下发默认二层流表
        """
        dpid = datapath.id
        for mac, out_port in self.mac_to_port[dpid].items():
            """
            复制一份至控制器
            """
            actions = [
                parser.OFPActionOutput(out_port),
                # parser.OFPActionOutput(ofproto.OFPP_CONTROLLER),
            ]
            match = parser.OFPMatch(eth_dst=mac)
            self.add_flow(datapath, 10, match, actions)

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

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # If you hit this you might want to increase
        # the "miss_send_length" of your switch
        print("--------------------------")
        if ev.msg.msg_len < ev.msg.total_len:
            self.logger.debug(
                "packet truncated: only %s of %s bytes",
                ev.msg.msg_len,
                ev.msg.total_len,
            )
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match["in_port"]

        pkt = packet.Packet(msg.data)

        header_list = dict(
            (p.protocol_name, p)
            for p in pkt.protocols
            if isinstance(p, packet_base.PacketBase)
        )
        if TCP in header_list:
            tcp_pkt = header_list[TCP]
            if (tcp_pkt.src_port == 179 or tcp_pkt.dst_port == 179) and not isinstance(
                pkt.protocols[-1], tcp.tcp
            ):
                # mirror the traffic
                print(pkt.protocols[-1])
                return
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        print(pkt.protocols)
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return
        dst = eth.dst
        src = eth.src
        dpid = datapath.id
        # ARP 处理：控制器代理回复
        if eth.ethertype == ether_types.ETH_TYPE_ARP:
            arp_pkt = pkt.get_protocol(arp.arp)
            src_ip = arp_pkt.src_ip
            dst_ip = arp_pkt.dst_ip
            print(f"[ARP] [{hex(dpid)}] Received ARP packet from {src_ip} to {dst_ip}")

            if arp_pkt.opcode == arp.ARP_REQUEST:
                if dst_ip in self.arp_table:
                    dst_mac = self.arp_table[dst_ip]
                    print(f"[ARP] Replying: {dst_ip} is at {dst_mac}")
                    self.send_arp_reply(datapath, src, src_ip, dst_mac, dst_ip, in_port)
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

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        datapath.send_msg(out)

    def _handle_arp():
        pass

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
