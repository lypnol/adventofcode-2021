package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) int {
	// Your code goes here
	horizontal, depth := 0, 0
	instructions := strings.Split(s, "\n")

	for _, instruction := range instructions {
		n, _ := strconv.Atoi(strings.Split(instruction, " ")[1])

		switch instruction[0] {
		case 'f':
			horizontal += n
		case 'd':
			depth += n
		case 'u':
			depth -= n
		}
	}

	return horizontal * depth
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
