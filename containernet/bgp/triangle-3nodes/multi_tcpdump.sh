#!/bin/bash

declare -A HOST_INTERFACES 

CLAB_NAME="tri"

HOST_INTERFACES["r11"]="eth-r12 eth-r13"
HOST_INTERFACES["r22"]="eth-r21"
HOST_INTERFACES["r33"]="eth-r31"

OUTPUT_DIR="./tcpdump"
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
        echo "Capture the packets for $iface of $host"
        ip netns exec "clab-$CLAB_NAME-$host" tcpdump -i "$iface" -w "$output_file" &
        PIDS+=("$!")
    done
done

wait