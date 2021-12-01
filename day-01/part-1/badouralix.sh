#!/usr/bin/env bash

# Access input string with $INPUT
INPUT=$1
WINDOW=1

function run() {
    # Your code goes here
    read -r -d '' -a ARRAY <<< "$INPUT"
    BEFORE=("${ARRAY[@]:0:${#ARRAY[@]}-$WINDOW}")
    AFTER=("${ARRAY[@]:$WINDOW}")

    # Return answer
    wc -l <<< "$(for idx in "${!AFTER[@]}"; do if [ "${AFTER[$idx]}" -gt "${BEFORE[$idx]}" ]; then echo yolo; fi; done)"
}

echo "$(run)"
