#!/bin/bash

declare -A HOST_INTERFACES 

CLAB_NAME="bgp-v6"

HOST_INTERFACES["h1"]="eth-r11"
HOST_INTERFACES["r11"]="eth-r12 eth-h1"
HOST_INTERFACES["r12"]="eth-r11 eth-r21 eth-r22"
HOST_INTERFACES["r21"]="eth-r12 eth-r23"
HOST_INTERFACES["r22"]="eth-r12 eth-r23"
HOST_INTERFACES["r23"]="eth-r21 eth-r22 eth-r31 eth-r32"
HOST_INTERFACES["r31"]="eth-r23 eth-r33"
HOST_INTERFACES["r32"]="eth-r23 eth-r33"
HOST_INTERFACES["r33"]="eth-r31 eth-r32 eth-h3"
HOST_INTERFACES["h3"]="eth-r33"

OUTPUT_DIR="/tmp/bgp-tcpdump/$CLAB_NAME"
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

trap cleanup SIGINT SIGTERM

for host in "${!HOST_INTERFACES[@]}"; do
    interfaces=${HOST_INTERFACES[$host]}
    for iface in $interfaces; do
        output_file="$OUTPUT_DIR/$(date +%H%M)_${host}_${iface}.pcap"
        echo "Capture the packets clab-$CLAB_NAME-$host for $iface of $host"
        ip netns exec "clab-$CLAB_NAME-$host" tcpdump -i "$iface" 'tcp port 179 or icmp or udp port 3784 or udp port 4784' -w "$output_file" &
        PIDS+=("$!")
    done
done

wait