#!/usr/bin/env bash
echo "$1" | awk '
BEGIN {
    "date +%s%N" | getline startTime; close("date +%s%N");
    counter = 0; previous=0;
}
{
    if ($1 > previous) counter+=1; 
    previous = $1;
}
END {
    print counter-1;
    "date +%s%N" | getline endTime; close("date +%s%N");
    print "_duration:", (endTime - startTime) / 1000000;
}'
