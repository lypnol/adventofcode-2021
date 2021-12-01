package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const (
	window = 3
)

func run(s string) int {
	measurements := strings.Split(s, "\n")
	increases := 0

	for idx := range measurements[:len(measurements)-window] {
		previous, _ := strconv.Atoi(measurements[idx])
		current, _ := strconv.Atoi(measurements[idx+window])
		if previous < current {
			increases++
		}
		previous = current
	}

	return increases
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	// Read input from stdin
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
