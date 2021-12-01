#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1
WINDOW=1

function run() {
    # Your code goes here
    read -r -d '' -a ARRAY <<< "$INPUT"
    SHIFT=("${ARRAY[@]:$WINDOW}")

    # Return answer
    wc -l <<< "$(for idx in "${!SHIFT[@]}"; do if [ "${SHIFT[$idx]}" -gt "${ARRAY[$idx]}" ]; then echo yolo; fi; done)"
}

echo "$(run)"
