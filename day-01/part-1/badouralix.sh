#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1
WINDOW=2

function run() {
    # Your code goes here
    read -ra BEFORE <<< "$(echo "$INPUT" | tr '\n' ' ' | rev | cut -d' ' -f$WINDOW- | rev)"
    read -ra AFTER <<< "$(echo "$INPUT" | tr '\n' ' ' | cut -d' ' -f$WINDOW-)"

    # Return answer
    wc -l <<< "$(for idx in "${!AFTER[@]}"; do if [ "${AFTER[$idx]}" -gt "${BEFORE[$idx]}" ]; then echo yolo; fi; done)"
    echo
}

echo "$(run)"
