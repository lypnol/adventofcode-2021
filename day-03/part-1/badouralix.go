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
	lines := strings.Split(s, "\n")
	counters := make([]int, len(lines[0]))

	for _, line := range lines {
		for idx, c := range line {
			if c == '1' {
				counters[idx]++
			}
		}
	}

	gamma, epsilon := 0, 0
	for _, counter := range counters {
		if float64(counter) >= float64(len(lines))/2 {
			gamma += 1
		} else {
			epsilon += 1
		}
		gamma *= 2
		epsilon *= 2
	}

	return gamma * epsilon / 4
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
