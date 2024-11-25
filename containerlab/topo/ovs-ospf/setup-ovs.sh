#!/bin/bash

S12=sw12
S21=sw21
S23=sw23
S32=sw32
S34=sw34
S43=sw43
S14=sw14
S41=sw41
S24=sw24
S42=sw42

OF_VER=OpenFlow13
FAIL_MODE=standalone

echo Create switches
for BR in $S12 $S21 $S23 $S32 $S34 $S43 $S14 $S41 $S24 $S42
do
  ovs-vsctl --may-exist add-br $BR
#   ovs-vsctl set bridge $BR protocols=$OF_VER
done

echo Set MAC address
ovs-vsctl set bridge $S12 other-config:hwaddr=00:00:00:00:00:12
ovs-vsctl set bridge $S21 other-config:hwaddr=00:00:00:00:00:21
ovs-vsctl set bridge $S23 other-config:hwaddr=00:00:00:00:00:23
ovs-vsctl set bridge $S32 other-config:hwaddr=00:00:00:00:00:32
ovs-vsctl set bridge $S34 other-config:hwaddr=00:00:00:00:00:34
ovs-vsctl set bridge $S43 other-config:hwaddr=00:00:00:00:00:43
ovs-vsctl set bridge $S14 other-config:hwaddr=00:00:00:00:00:14
ovs-vsctl set bridge $S41 other-config:hwaddr=00:00:00:00:00:41
ovs-vsctl set bridge $S24 other-config:hwaddr=00:00:00:00:00:24
ovs-vsctl set bridge $S42 other-config:hwaddr=00:00:00:00:00:42

echo Connect switches
ovs-vsctl --may-exist add-port $S12 p12 -- set interface p12 type=patch options:peer=p21
ovs-vsctl --may-exist add-port $S21 p21 -- set interface p21 type=patch options:peer=p12

ovs-vsctl --may-exist add-port $S23 p23 -- set interface p23 type=patch options:peer=p32
ovs-vsctl --may-exist add-port $S32 p32 -- set interface p32 type=patch options:peer=p23

ovs-vsctl --may-exist add-port $S34 p34 -- set interface p34 type=patch options:peer=p43
ovs-vsctl --may-exist add-port $S43 p43 -- set interface p43 type=patch options:peer=p34

ovs-vsctl --may-exist add-port $S14 p14 -- set interface p14 type=patch options:peer=p41
ovs-vsctl --may-exist add-port $S41 p41 -- set interface p41 type=patch options:peer=p14

ovs-vsctl --may-exist add-port $S24 p24 -- set interface p24 type=patch options:peer=p42
ovs-vsctl --may-exist add-port $S42 p42 -- set interface p42 type=patch options:peer=p24

echo Set switch options
for BR in $S12 $S21 $S23 $S32 $S34 $S43 $S14 $S41 $S24 $S42
do
  ovs-vsctl set bridge $BR fail_mode=$FAIL_MODE
#   ovs-vsctl set bridge $BR protocols=$OF_VER
done