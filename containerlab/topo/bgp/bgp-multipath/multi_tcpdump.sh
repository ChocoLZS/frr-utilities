#!/bin/bash

declare -A HOST_INTERFACES 

HOST_INTERFACES["h1"]="eth-r11"
HOST_INTERFACES["r11"]="eth-r12"
HOST_INTERFACES["r12"]="eth-r21 eth-r22"
HOST_INTERFACES["r21"]="eth-r23"
HOST_INTERFACES["r22"]="eth-r23"
HOST_INTERFACES["r23"]="eth-r31 eth-r32"
HOST_INTERFACES["r31"]="eth-r33"
HOST_INTERFACES["r32"]="eth-r33"
HOST_INTERFACES["r33"]="eth-h3"

OUTPUT_DIR="/tmp/bgp-tcpdump"
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
        ip netns exec "clab-bgp-$host" tcpdump -i "$iface" -w "$output_file" &
        PIDS+=("$!")
    done
done

wait