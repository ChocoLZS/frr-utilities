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
d1 = net.addDocker(
    "r1",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r1.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
d2 = net.addDocker(
    "r2",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r2.conf:/etc/frr/frr.conf",
    ],
    sysctls={
        "net.ipv6.conf.all.disable_ipv6": 1,
        "net.ipv6.conf.default.disable_ipv6": 1,
    },
)
# h1 = net.addHost("h1", ip="100.1.1.100/24")
# h2 = net.addHost("h2", ip="102.2.2.100/24")
info("*** Adding switches\n")
s1 = net.addSwitch("s1", dpid="0000000000000011")
s2 = net.addSwitch("s2", dpid="0000000000000022")
info("*** Creating links\n")
net.addLink(
    d1,
    s1,
    intfName1="eth-r2",
    intfName2="eth-s1-r1",
    addr1="00:00:00:00:00:11",
    addr2="00:99:99:00:00:11",
    port2=6611,
)
net.addLink(
    s1,
    s2,
    cls=TCLink,
    # delay="100ms",
    bw=1,
    port2=22,
    port1=11,
    addr1="00:00:01:00:00:02",
    addr2="00:00:02:00:00:01",
)
net.addLink(
    d2,
    s2,
    intfName1="eth-r1",
    intfName2="eth-s2-r2",
    addr1="00:00:00:00:00:22",
    addr2="00:99:99:00:00:22",
    port2=6611,
)
# net.addLink(d1, h1, intfName1="eth-h1")
# net.addLink(d2, h2, intfName1="eth-h2")
info("*** Starting network\n")
net.start()
info("*** Testing connectivity\n")
# net.ping([d1, d2])
info("*** Running CLI\n")
CLI(net)
info("*** Stopping network")
net.stop()
