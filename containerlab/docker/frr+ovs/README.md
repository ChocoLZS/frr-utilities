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

ovs configuration:

- https://docs.openvswitch.org/en/latest/faq/issues/
- https://docs.openvswitch.org/en/latest/intro/install/userspace/
- https://docs.openvswitch.org/en/latest/howto/userspace-tunneling/