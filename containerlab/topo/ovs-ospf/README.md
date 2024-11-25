# topology

openvswitch: standalone 模式，只模拟二层交换机功能

```
R1 --- R2
|     / |
|   /   |
| /     |
R4 --- R3
```

```
R1 -S12---S21- R2
|             / |
|          S24 S23
S14       /     |
|       /       |
|     /         |
S41 S42        S32
|  /            |
R4 -S43---S34- R3
```
