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
from ryu.ofproto import ofproto_v1_5, inet, ether
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp

from ryu.lib.packet import tcp, packet_base

TCP = tcp.tcp.__name__

LOCAL_PORT = 4294967294


class SimpleSwitch15(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_5.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch15, self).__init__(*args, **kwargs)
        self.mac_to_port = {
            int(0x11): {
                "00:00:02:00:00:01": 22,
                "00:00:03:00:00:01": 33,
                "00:ff:01:00:00:01": 601,
                # "00:00:00:00:00:22": 22,
                # "00:00:00:00:00:33": 33,
            },
            int(0x22): {
                "00:00:01:00:00:02": 11,
                "00:00:03:00:00:02": 33,
                "00:00:21:00:00:02": 21,
                # "00:00:00:00:00:11": 11,
                # "00:00:00:00:00:33": 33,
            },
            int(0x33): {
                "00:00:01:00:00:03": 11,
                "00:00:02:00:00:03": 22,
                "00:ff:03:00:00:03": 603,
                # "00:00:00:00:00:11": 11,
                # "00:00:00:00:00:22": 22,
            },
        }
        self.self_mac = {
            int(0x11): {
                "00:00:01:00:00:02": 22,
                "00:00:01:00:00:03": 33,
                "00:ff:01:00:00:01": 601,
            },
            int(0x22): {
                "00:00:02:00:00:01": 11,
                "00:00:02:00:00:03": 33,
            },
            int(0x33): {
                "00:00:03:00:00:01": 11,
                "00:00:03:00:00:02": 22,
                "00:ff:03:00:00:03": 603,
            },
        }

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # # layer 2 flow rule
        dpid = hex(int(datapath.id))
        print("current dpid {}".format(dpid))
        if dpid == 0x11:
            # should only know the mac address of the next hop
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:00:02:00:00:01"),
                [parser.OFPActionOutput(22)],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:00:03:00:00:01"),
                [parser.OFPActionOutput(33)],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:ff:01:00:00:01"),
                [parser.OFPActionOutput(601)],
            )
            # replace the mac address of the next hop
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:11", eth_dst="00:00:02:00:00:01"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:01:00:00:02"),
                    parser.OFPActionOutput(22),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:11", eth_dst="00:00:03:00:00:01"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:01:00:00:03"),
                    parser.OFPActionOutput(33),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:11", eth_dst="00:ff:01:00:00:01"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:01:00:00:01"),
                    parser.OFPActionOutput(601),
                ],
            )
            # replace in dst mac address
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:02:00:00:01", eth_dst="00:00:01:00:00:02"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:11"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:03:00:00:01", eth_dst="00:00:01:00:00:03"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:11"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:ff:01:00:00:01", eth_dst="00:00:01:00:00:01"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:11"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
        elif dpid == 0x22:
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:00:01:00:00:02"),
                [parser.OFPActionOutput(11)],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:00:03:00:00:02"),
                [parser.OFPActionOutput(33)],
            )
            # replace the mac address of the next hop
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:22", eth_dst="00:00:01:00:00:02"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:02:00:00:01"),
                    parser.OFPActionOutput(11),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:22", eth_dst="00:00:03:00:00:02"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:02:00:00:03"),
                    parser.OFPActionOutput(33),
                ],
            )
            # replace in dst mac address
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:01:00:00:02", eth_dst="00:00:02:00:00:01"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:22"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:03:00:00:02", eth_dst="00:00:02:00:00:03"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:22"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
        elif dpid == 0x33:
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:00:01:00:00:03"),
                [parser.OFPActionOutput(11)],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:00:02:00:00:03"),
                [parser.OFPActionOutput(22)],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(eth_dst="00:ff:03:00:00:03"),
                [parser.OFPActionOutput(603)],
            )
            # replace the mac address of the next hop
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:33", eth_dst="00:00:01:00:00:03"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:03:00:00:01"),
                    parser.OFPActionOutput(11),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:33", eth_dst="00:00:02:00:00:03"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:03:00:00:02"),
                    parser.OFPActionOutput(22),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:00:00:00:33", eth_dst="00:ff:03:00:00:03"
                ),
                [
                    parser.OFPActionSetField(eth_src="00:00:03:00:00:03"),
                    parser.OFPActionOutput(603),
                ],
            )
            # replace in dst mac address
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:01:00:00:03", eth_dst="00:00:03:00:00:01"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:33"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:00:02:00:00:03", eth_dst="00:00:03:00:00:02"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:33"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )
            self.add_flow(
                datapath,
                1,
                parser.OFPMatch(
                    eth_src="00:ff:03:00:00:03", eth_dst="00:00:03:00:00:03"
                ),
                [
                    parser.OFPActionSetField(eth_dst="00:00:00:00:00:33"),
                    parser.OFPActionOutput(LOCAL_PORT),
                ],
            )

        # install table-miss flow entry
        #
        # We specify NO BUFFER to max_len of the output action due to
        # OVS bug. At this moment, if we specify a lesser number, e.g.,
        # 128, OVS will send Packet-In with invalid buffer_id and
        # truncated packet data. In that case, we cannot output packets
        # correctly.  The bug has been fixed in OVS v2.1.0.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)
        ]
        self.add_flow(datapath, 0, match, actions)

        # """
        # 捕获所有tcp包，并发送至控制器
        # """
        # macth_tcp = parser.OFPMatch(
        #     eth_type=ether_types.ETH_TYPE_IP, ip_proto=inet.IPPROTO_TCP
        # )
        # """
        # 1. OFPP_NORMAL: 发送至交换机的正常处理流程
        # 2. OFPP_CONTROLLER: 发送至控制器（而且控制器只分析，并不处理）
        # """
        # actions_tcp = [
        #     # parser.OFPActionOutput(ofproto.OFPP_NORMAL, ofproto.OFPCML_NO_BUFFER),
        #     parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER),
        # ]
        # self.add_flow(datapath, 1, macth_tcp, actions_tcp)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]

        mod = parser.OFPFlowMod(
            datapath=datapath, priority=priority, match=match, instructions=inst
        )
        datapath.send_msg(mod)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        print("----------------------")
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
                # print(self.mac_to_port)
                return

        eth = pkt.get_protocols(ethernet.ethernet)[0]

        ethertype = eth.ethertype

        if ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            return

        if ethertype == ether.ETH_TYPE_ARP:
            arp_pkt = pkt.get_protocol(arp.arp)
            print(
                f"src ip: {arp_pkt.src_ip}, mac: {arp_pkt.src_mac}\tdst ip: {arp_pkt.dst_ip}, mac: {arp_pkt.dst_mac}"
            )
            return
        dst = eth.dst
        src = eth.src

        dpid = datapath.id
        self.mac_to_port.setdefault(dpid, {})
        print(pkt.protocols)
        print(f"packet in {hex(int(dpid))}({dpid}) {src} {dst} {in_port}")
        print("----------------------")
        # learn a mac address to avoid FLOOD next time.
        # self.mac_to_port[dpid][src] = in_port

        # if dst in self.mac_to_port[dpid]:
        #     out_port = self.mac_to_port[dpid][dst]
        # elif dst in self.self_mac[dpid]:
        #     print("send to self")
        #     out_port = LOCAL_PORT
        # else:
        #     print("flooding")
        #     print(self.mac_to_port[dpid])
        #     out_port = ofproto.OFPP_FLOOD

        # actions = [parser.OFPActionOutput(out_port)]

        # # install a flow to avoid packet_in next time
        # if out_port != ofproto.OFPP_FLOOD:
        #     match = parser.OFPMatch(in_port=in_port, eth_dst=dst)
        #     self.add_flow(datapath, 1, match, actions)

        data = None
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        match = parser.OFPMatch(in_port=in_port)

        # out = parser.OFPPacketOut(
        #     datapath=datapath,
        #     buffer_id=msg.buffer_id,
        #     match=match,
        #     actions=actions,
        #     data=data,
        # )
        # datapath.send_msg(out)
