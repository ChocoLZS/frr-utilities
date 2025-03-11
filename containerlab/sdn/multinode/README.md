# 不同lab跨机器（vm）通信

> 参考：https://containerlab.dev/lab-examples/multinode/

之前的实验都是在同一台主机上使用命令 `clab depoy -t *.clab.yaml` 启动的lab。

此lab允许你在多台主机上对多个lab进行拓扑搭建。

## 实验步骤

- 主机1：
    - ip：192.168.114.10

- 主机2
    - ip：192.168.114.20

1. 分别在两个主机启动lab

主机1：`clab dep -t host1.clab.yml`
主机2：`clab dep -t host2.clab.yml`

2. 分别在两个主机建立vxlan连接

主机1：`clab tools vxlan create --remote 192.168.114.20 --id 114 --link vxlan`
主机2：`clab tools vxlan create --remote 192.168.114.10 --id 114 --link vxlan`

3. 分别进入两个主机的frr节点进行bgp验证
