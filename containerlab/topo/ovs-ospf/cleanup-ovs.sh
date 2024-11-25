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

echo Remove all switches
for BR in $S12 $S21 $S23 $S32 $S34 $S43 $S14 $S41 $S24 $S42
do
  ovs-vsctl --if-exists del-br $BR
#   ovs-vsctl set bridge $BR protocols=$OF_VER
done