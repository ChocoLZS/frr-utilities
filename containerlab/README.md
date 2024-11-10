# containerlab

> https://containerlab.dev/

With the growing number of containerized Network Operating Systems grows the demand to easily run them in the user-defined, versatile lab topologies.

Unfortunately, container orchestration tools like **docker-compose are not** a good fit for that purpose, as they do not allow a user to easily create connections between the containers which define a topology.

**Containerlab** provides a CLI for orchestrating and managing container-based networking labs. It starts the containers, builds a virtual wiring between them to create lab topologies of users choice and manages labs lifecycle.

## 链路参数设置

[设置链路参数](https://containerlab.dev/cmd/tools/netem/set/#setting-link-impairments)

**NetEm**（Network Emulator 的简称）是 Linux 内核中的一种网络排队学科（Queuing Discipline），用于在网络设备上模拟各种网络特性，包括延迟（Delay）、抖动（Jitter）、丢包（Packet Loss）、重复（Duplication）和乱序（Reordering）等。通过使用 NetEm，您可以在本地网络环境中模拟真实网络中的不稳定因素，以测试和验证网络应用程序在不同网络条件下的性能和可靠性。

NetEm 通常与 `tc`（Traffic Control）的命令行工具配合使用，`tc` 是 Linux 提供的网络流量控制工具。

**常用功能和示例：**

1. **模拟网络延迟：**

   增加固定的网络延迟：

   ```bash
   sudo tc qdisc add dev eth0 root netem delay 100ms
   ```

   增加带有抖动的网络延迟：

   ```bash
   sudo tc qdisc add dev eth0 root netem delay 100ms 20ms
   ```

2. **模拟丢包率：**

   设置固定的丢包率：

   ```bash
   sudo tc qdisc add dev eth0 root netem loss 1%
   ```

3. **模拟数据包重复：**

   设置一定比例的数据包重复：

   ```bash
   sudo tc qdisc add dev eth0 root netem duplicate 1%
   ```

4. **模拟数据包乱序：**

   设置一定概率的数据包乱序：

   ```bash
   sudo tc qdisc add dev eth0 root netem delay 10ms reorder 25% 50%
   ```

5. **移除 NetEm 设置：**

   ```bash
   sudo tc qdisc del dev eth0 root
   ```

**注意事项：**

- **权限要求：**需要以超级用户（root）权限执行上述命令，可以使用 `sudo` 提升权限。
- **影响范围：**上述命令会影响指定网络接口（例如 `eth0`）上的所有出站流量。
- **测试环境：**在生产环境中请谨慎使用，以免影响正常网络通信，建议在测试环境下使用。

**应用场景：**

- **网络应用测试：**模拟不同的网络条件，测试应用程序的性能和稳定性。
- **性能调优：**在受控的网络条件下，调试和优化程序的网络性能。
- **教学和研究：**用于网络教学、协议研究和实验验证。

**参考资料：**

- [Linux Manual: tc-netem](https://man7.org/linux/man-pages/man8/tc-netem.8.html)
- [NetEm 官方文档](https://www.linux.org/docs/man8/tc-netem.html)
- [网络流量控制（Traffic Control）指南](https://wiki.linuxfoundation.org/networking/netem)

通过使用 NetEm，您可以在受控的环境下模拟各种复杂的网络状况，帮助开发和测试更健壮的网络应用程序。
