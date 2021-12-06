#!/usr/bin/env bash
echo "$1" | awk '
BEGIN { 
    "date +%s%N" | getline startTime; close("date +%s%N");
    counter = 0;
    v0 = 0; 
    v1 = 0; 
    v2 = 0;
}
{
    if ($1 > v0) counter+=1;
    v0 = v1;
    v1 = v2;
    v2 = $1;
}
END {
    print counter-3;
    "date +%s%N" | getline endTime; close("date +%s%N");
    print "_duration:", (endTime - startTime) / 1000000;
}
'