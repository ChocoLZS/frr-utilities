#!/usr/bin/python
"""
This is the most simple example to showcase Containernet.
"""
from mininet.net import Containernet
from mininet.node import OVSKernelSwitch, RemoteController, Controller
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

setLogLevel("info")

import os

file_path = os.path.dirname(os.path.realpath(__file__))
net = Containernet(
    controller=RemoteController,
    switch=OVSKernelSwitch,
)
info("*** Adding controller\n")
net.addController("c0")
info("*** Adding docker containers\n")
r11 = net.addDocker(
    "r11",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r11.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r12 = net.addDocker(
    "r12",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r12.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r21 = net.addDocker(
    "r21",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r21.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r22 = net.addDocker(
    "r22",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r22.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r23 = net.addDocker(
    "r23",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r23.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r31 = net.addDocker(
    "r31",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r31.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r32 = net.addDocker(
    "r32",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r32.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
r33 = net.addDocker(
    "r33",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r33.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
# h1 = net.addHost("h1", ip="100.1.1.100/24")
# h3 = net.addHost("h3", ip="103.3.3.100/24")
info("*** Adding switches\n")
s11 = net.addSwitch("s11", dpid="0000000000000011")
s12 = net.addSwitch("s12", dpid="0000000000000012")
s21 = net.addSwitch("s21", dpid="0000000000000021")
s22 = net.addSwitch("s22", dpid="0000000000000022")
s23 = net.addSwitch("s23", dpid="0000000000000023")
s31 = net.addSwitch("s31", dpid="0000000000000031")
s32 = net.addSwitch("s32", dpid="0000000000000032")
s33 = net.addSwitch("s33", dpid="0000000000000033")
info("*** Creating links\n")
net.addLink(
    r11,
    s11,
    intfName1="br-ovs",
    intfName2="eth-s11-r11",
    addr1="00:00:00:00:00:11",
    addr2="00:99:99:00:00:11",
    port2=1,
)
net.addLink(
    r12,
    s12,
    intfName1="br-ovs",
    intfName2="eth-s12-r12",
    addr1="00:00:00:00:00:12",
    addr2="00:99:99:00:00:12",
    port2=1,
)
net.addLink(
    r21,
    s21,
    intfName1="br-ovs",
    intfName2="eth-s21-r21",
    addr1="00:00:00:00:00:21",
    addr2="00:99:99:00:00:21",
    port2=1,
)
net.addLink(
    r22,
    s22,
    intfName1="br-ovs",
    intfName2="eth-s22-r22",
    addr1="00:00:00:00:00:22",
    addr2="00:99:99:00:00:22",
    port2=1,
)
net.addLink(
    r23,
    s23,
    intfName1="br-ovs",
    intfName2="eth-s23-r23",
    addr1="00:00:00:00:00:23",
    addr2="00:99:99:00:00:23",
    port2=1,
)
net.addLink(
    r31,
    s31,
    intfName1="br-ovs",
    intfName2="eth-s31-r31",
    addr1="00:00:00:00:00:31",
    addr2="00:99:99:00:00:31",
    port2=1,
)
net.addLink(
    r32,
    s32,
    intfName1="br-ovs",
    intfName2="eth-s32-r32",
    addr1="00:00:00:00:00:32",
    addr2="00:99:99:00:00:32",
    port2=1,
)
net.addLink(
    r33,
    s33,
    intfName1="br-ovs",
    intfName2="eth-s33-r33",
    addr1="00:00:00:00:00:33",
    addr2="00:99:99:00:00:33",
    port2=1,
)
net.addLink(
    s11,
    s12,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s11-eth-r12",
    intfName2="s12-eth-r11",
    port1=12,
    port2=11,
    addr1="00:00:11:00:00:12",
    addr2="00:00:12:00:00:11",
)
net.addLink(
    s12,
    s21,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s12-eth-r21",
    intfName2="s21-eth-r12",
    port1=21,
    port2=12,
    addr1="00:00:12:00:00:21",
    addr2="00:00:21:00:00:12",
)
net.addLink(
    s12,
    s22,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s12-eth-r22",
    intfName2="s22-eth-r12",
    port1=22,
    port2=12,
    addr1="00:00:12:00:00:22",
    addr2="00:00:22:00:00:12",
)
net.addLink(
    s21,
    s23,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s21-eth-r23",
    intfName2="s23-eth-r21",
    port1=23,
    port2=21,
    addr1="00:00:21:00:00:23",
    addr2="00:00:23:00:00:21",
)
net.addLink(
    s22,
    s23,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s22-eth-r23",
    intfName2="s23-eth-r22",
    port1=23,
    port2=22,
    addr1="00:00:22:00:00:23",
    addr2="00:00:23:00:00:22",
)
net.addLink(
    s23,
    s31,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s23-eth-r31",
    intfName2="s31-eth-r23",
    port1=31,
    port2=23,
    addr1="00:00:23:00:00:31",
    addr2="00:00:31:00:00:23",
)
net.addLink(
    s23,
    s32,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s23-eth-r32",
    intfName2="s32-eth-r23",
    port1=32,
    port2=23,
    addr1="00:00:23:00:00:32",
    addr2="00:00:32:00:00:23",
)
net.addLink(
    s31,
    s33,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s31-eth-r33",
    intfName2="s33-eth-r31",
    port1=33,
    port2=31,
    addr1="00:00:31:00:00:33",
    addr2="00:00:33:00:00:31",
)
net.addLink(
    s32,
    s33,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s32-eth-r33",
    intfName2="s33-eth-r32",
    port1=33,
    port2=32,
    addr1="00:00:32:00:00:33",
    addr2="00:00:33:00:00:32",
)

info("*** Starting network\n")
net.start()
info("*** Testing connectivity\n")
# net.ping([d1, d2])
info("*** Running CLI\n")
CLI(net)
info("*** Stopping network")
net.stop()
