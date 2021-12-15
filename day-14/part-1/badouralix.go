package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) int {
	// Your code goes here
	split := strings.Split(s, "\n\n")
	pattern := split[0]
	mapping := make(map[string]string)
	counters := make(map[rune]int)
	min, max := 0, 0

	for _, line := range strings.Split(split[1], "\n") {
		rule := strings.Split(line, " -> ")
		mapping[rule[0]] = rule[1]
	}

	for i := 0; i < 10; i++ {
		new := ""

		for c := 0; c < len(pattern)-1; c++ {
			new += string(pattern[c])
			if v, ok := mapping[pattern[c:c+2]]; ok {
				new += v
			}
		}

		pattern = new + string(pattern[len(pattern)-1])
	}

	for _, v := range pattern {
		if _, ok := counters[v]; !ok {
			counters[v] = 0
		}
		counters[v]++
		min = counters[v]
	}

	for _, v := range counters {
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}

	return max - min
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	var input []byte
	var err error
	if len(os.Args) > 1 {
		// Read input from file for local debugging
		input, err = ioutil.ReadFile(os.Args[1])
		if err != nil {
			panic(err)
		}
		// Remove extra newline
		input = input[:len(input)-1]
	} else {
		// Read input from stdin
		input, err = ioutil.ReadAll(os.Stdin)
		if err != nil {
			panic(err)
		}
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
