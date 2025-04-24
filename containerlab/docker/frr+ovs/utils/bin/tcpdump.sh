#!/bin/bash

hostname=$(hostname)

tcpdump -i br-ovs -w /tmp/tcpdump/${hostname}-br-ovs.pcap &