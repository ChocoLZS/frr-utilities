# 拓扑

```
node-5-1 --- node-5-2 --- node-5-3 --- node-5-4 --- node-5-5 --- node-5-6 --- node-5-7 --- node-5-8 --- node-5-9 --- node-5-10
   |            |            |            |            |            |            |            |            |            |
node-4-1 --- node-4-2 --- node-4-3 --- node-4-4 --- node-4-5 --- node-4-6 --- node-4-7 --- node-4-8 --- node-4-9 --- node-4-10
   |            |            |            |            |            |            |            |            |            |
node-3-1 --- node-3-2 --- node-3-3 --- node-3-4 --- node-3-5 --- node-3-6 --- node-3-7 --- node-3-8 --- node-3-9 --- node-3-10
   |            |            |            |            |            |            |            |            |            |
node-2-1 --- node-2-2 --- node-2-3 --- node-2-4 --- node-2-5 --- node-2-6 --- node-2-7 --- node-2-8 --- node-2-9 --- node-2-10
   |            |            |            |            |            |            |            |            |            |
node-1-1 --- node-1-2 --- node-1-3 --- node-1-4 --- node-1-5 --- node-1-6 --- node-1-7 --- node-1-8 --- node-1-9 --- node-1-10
```

实际上是这样的

```
node-1-10 --- node-1-1 --- node-1-2 --- node-1-3 --- node-1-4 --- node-1-5 --- node-1-6 --- node-1-7 --- node-1-8 --- node-1-9 --- node-1-10 --- node-1-1
   |       ******|************|************|************|************|************|************|************|************|************|********    |
node-5-10 -*- node-5-1 --- node-5-2 --- node-5-3 --- node-5-4 --- node-5-5 --- node-5-6 --- node-5-7 --- node-5-8 --- node-5-9 --- node-5-10 -*- node-5-1
   |       *     |            |            |            |            |            |            |            |            |            |       *    |
node-4-10 -*- node-4-1 --- node-4-2 --- node-4-3 --- node-4-4 --- node-4-5 --- node-4-6 --- node-4-7 --- node-4-8 --- node-4-9 --- node-4-10 -*- node-4-1
   |       *     |            |            |            |            |            |            |            |            |            |       *    |
node-3-10 -*- node-3-1 --- node-3-2 --- node-3-3 --- node-3-4 --- node-3-5 --- node-3-6 --- node-3-7 --- node-3-8 --- node-3-9 --- node-3-10 -*- node-3-1
   |       *     |            |            |            |            |            |            |            |            |            |       *    |
node-2-10 -*- node-2-1 --- node-2-2 --- node-2-3 --- node-2-4 --- node-2-5 --- node-2-6 --- node-2-7 --- node-2-8 --- node-2-9 --- node-2-10 -*- node-2-1
   |       *     |            |            |            |            |            |            |            |            |            |       *    |
node-1-10 -*- node-1-1 --- node-1-2 --- node-1-3 --- node-1-4 --- node-1-5 --- node-1-6 --- node-1-7 --- node-1-8 --- node-1-9 --- node-1-10 -*- node-1-1
   |       ******|************|************|************|************|************|************|************|************|************|********    |
node-5-10 --- node-5-1 --- node-5-2 --- node-5-3 --- node-5-4 --- node-5-5 --- node-5-6 --- node-5-7 --- node-5-8 --- node-5-9 --- node-5-10 --- node-5-1
```

任意一个节点的接口布局如下

eth-t, eth-r 即上方和右方为主接口

```
          eth-t
           |
eth-l --- node-x-y --- eth-r
           |
          eth-b

```

## 如何使用

1. 分别运行`generate_conf.py`和`generate_topo.py`，生成 containerlab 的 yml 文件和 frr 的 osfp 配置文件

2. sudo clab deploy --topo grid.clab.yml 启动容器

3. 结束后使用 sudo clab destroy --topo grid.clab.yml 销毁容器
