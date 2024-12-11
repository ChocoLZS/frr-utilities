#!/bin/bash

declare -A HOST_INTERFACES 

CLAB_NAME="iperf"

HOST_INTERFACES["r1"]="eth-r2"

OUTPUT_DIR="/tmp/bgp-tcpdump/iperfs"
mkdir -p "$OUTPUT_DIR"

PIDS=()

ID="$(date +%H%M)"

echo "[$ID] Start program"

cleanup() {
    echo "Stoping capturing processes..."
    for pid in "${PIDS[@]}"; do
        kill "$pid" 2>/dev/null
    done
    echo "[$ID] All processes have been stopped"
    exit 0
}

trap cleanup SIGINT

for host in "${!HOST_INTERFACES[@]}"; do
    interfaces=${HOST_INTERFACES[$host]}
    for iface in $interfaces; do
        output_file="$OUTPUT_DIR/$(date +%H%M)_${host}_${iface}.pcap"
        echo "Capture the packets for $iface of $host"
        ip netns exec "clab-$CLAB_NAME-$host" tcpdump -i "$iface" 'tcp port 179 or icmp' -w "$output_file" &
        PIDS+=("$!")
    done
done

wait