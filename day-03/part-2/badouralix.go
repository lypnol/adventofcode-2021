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
	backup := lines
	size := len(lines[0])
	generator, scrubber := 0, 0

	for i := 0; i < size; i++ {
		lines0 := make([]string, 0)
		lines1 := make([]string, 0)
		counter := 0

		for _, line := range lines {
			if line[i] == '1' {
				counter++
				lines1 = append(lines1, line)
			} else {
				lines0 = append(lines0, line)
			}
		}

		if len(lines0) <= len(lines1) {
			generator += 1
			lines = lines1
		} else {
			lines = lines0
		}

		generator *= 2
	}

	lines = backup

	for i := 0; i < size; i++ {
		lines0 := make([]string, 0)
		lines1 := make([]string, 0)
		counter := 0

		for _, line := range lines {
			if line[i] == '1' {
				counter++
				lines1 = append(lines1, line)
			} else {
				lines0 = append(lines0, line)
			}
		}

		if len(lines1) == 0 || (len(lines0) <= len(lines1) && len(lines0) != 0) {
			lines = lines0
		} else {
			scrubber += 1
			lines = lines1
		}

		scrubber *= 2
	}

	return generator * scrubber / 4
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
