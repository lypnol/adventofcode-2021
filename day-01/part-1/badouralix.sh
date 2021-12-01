#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1
WINDOW=1

function run() {
    # Your code goes here
    read -r -d '' -a ARRAY <<< "$INPUT"
    SHIFT=("${ARRAY[@]:$WINDOW}")

    # Return answer
    for idx in "${!SHIFT[@]}"; do [ "${SHIFT[$idx]}" -gt "${ARRAY[$idx]}" ]; echo $?; done | grep -c "0"
}

echo "$(run)"
