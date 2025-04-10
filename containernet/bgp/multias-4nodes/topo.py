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
r41 = net.addDocker(
    "r41",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r41.conf:/etc/frr/frr.conf",
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
s21 = net.addSwitch("s21", dpid="0000000000000021")
s31 = net.addSwitch("s31", dpid="0000000000000031")
s41 = net.addSwitch("s41", dpid="0000000000000041")
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
    r21,
    s21,
    intfName1="br-ovs",
    intfName2="eth-s21-r21",
    addr1="00:00:00:00:00:21",
    addr2="00:99:99:00:00:21",
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
    r41,
    s41,
    intfName1="br-ovs",
    intfName2="eth-s41-r41",
    addr1="00:00:00:00:00:41",
    addr2="00:99:99:00:00:41",
    port2=1,
)
net.addLink(
    s11,
    s21,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s11-eth-r21",
    intfName2="s21-eth-r11",
    port1=21,
    port2=11,
    addr1="00:00:11:00:00:21",
    addr2="00:00:21:00:00:11",
)
net.addLink(
    s11,
    s31,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s11-eth-r31",
    intfName2="s31-eth-r11",
    port1=31,
    port2=11,
    addr1="00:00:11:00:00:31",
    addr2="00:00:31:00:00:11",
)
net.addLink(
    s21,
    s41,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s21-eth-r41",
    intfName2="s41-eth-r21",
    port1=41,
    port2=21,
    addr1="00:00:21:00:00:41",
    addr2="00:00:41:00:00:21",
)
net.addLink(
    s31,
    s41,
    # cls=TCLink,
    # # delay="100ms",
    # bw=1,
    intfName1="s31-eth-r41",
    intfName2="s41-eth-r31",
    port1=41,
    port2=31,
    addr1="00:00:31:00:00:41",
    addr2="00:00:41:00:00:31",
)

info("*** Starting network\n")
net.start()
info("*** Testing connectivity\n")
# net.ping([d1, d2])
info("*** Running CLI\n")
CLI(net)
info("*** Stopping network")
net.stop()
