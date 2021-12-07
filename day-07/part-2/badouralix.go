package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) int {
	// Your code goes here
	var positions []int
	max := 0
	result := math.MaxInt32

	for _, v := range strings.Split(s, ",") {
		position, _ := strconv.Atoi(v)
		positions = append(positions, position)

		if position > max {
			max = position
		}
	}

	for i := 0; i <= max; i++ {
		cost := 0

		for _, position := range positions {
			if position-i > 0 {
				cost += (position - i) * (position - i + 1) / 2
			} else {
				cost += (i - position) * (i - position + 1) / 2
			}
		}

		if cost < result {
			result = cost
		}
	}

	return result
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
