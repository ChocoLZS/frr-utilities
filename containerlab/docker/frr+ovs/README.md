# frr+ovs in one container

```text
+------------------------+
|         name           |
+------------------------+
|          frr           |
+------------------------+
|         br-ovs         |
|    (OVS Bridge   )     |
|                        |
|                        |
|              +----+----+
|              | eth-any2|
|              +---------+
+---+-----+              |
| eth-any |              |
+---------+--------------+

```

```bash
docker build -t frr-ovs .
```
reference: https://www.bilibili.com/read/cv13103320