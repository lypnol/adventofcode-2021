#!/usr/bin/env bash
echo "$1" | awk '
BEGIN { 
    counter = 0;
}
{
}
END {
    print counter;
}
