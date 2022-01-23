#!/usr/bin/env bash
echo "$1" | awk '
BEGIN { 
    "date +%s%N" | getline startTime; close("date +%s%N");
    counter = 0;
}
{
}
END {
    print counter;
    "date +%s%N" | getline endTime; close("date +%s%N");
    print "_duration:", (endTime - startTime) / 1000000;
}
