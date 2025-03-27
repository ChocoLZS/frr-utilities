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
)
d3 = net.addDocker(
    "r3",
    ip=None,
    dimage="quay.io/frrouting/frr:10.2.1",
    dcmd="/usr/lib/frr/docker-start",
    volumes=[
        f"{file_path}/configs/daemons:/etc/frr/daemons",
        f"{file_path}/configs/r3.conf:/etc/frr/frr.conf",
    ],
)
h1 = net.addHost("h1", ip="100.1.1.100/24")
h3 = net.addHost("h3", ip="100.3.3.100/24")
info("*** Adding switches\n")
s1 = net.addSwitch("s1", dpid="0000000000000011")
s2 = net.addSwitch("s2", dpid="0000000000000022")
s3 = net.addSwitch("s3", dpid="0000000000000033")
info("*** Creating links\n")
net.addLink(d1, s1, intfName1="br-ovs")
net.addLink(d2, s2, intfName1="br-ovs")
net.addLink(d3, s3, intfName1="br-ovs")
net.addLink(s1, s2, cls=TCLink, bw=1)
net.addLink(s2, s3, cls=TCLink, bw=1)
net.addLink(s3, s1, cls=TCLink, bw=1)
net.addLink(d1, h1, intfName1="eth-h1")
net.addLink(d3, h3, intfName1="eth-h2")
info("*** Starting network\n")
net.start()
info("** Enabling STP\n")
s1.cmd("ovs-vsctl set Bridge s1 stp_enable=true")
s2.cmd("ovs-vsctl set Bridge s2 stp_enable=true")
s3.cmd("ovs-vsctl set Bridge s3 stp_enable=true")
info("*** Testing connectivity\n")
# net.ping([d1, d2])
info("*** Running CLI\n")
CLI(net)
info("*** Stopping network")
net.stop()
