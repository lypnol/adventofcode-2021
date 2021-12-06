package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(b []byte) int {
	// Your code goes here
	timers := [9]int{0}
	result := 0

	for cursor := 0; cursor < len(b); cursor++ {
		switch b[cursor] {
		case ',':
			continue
		default:
			timer := int(b[cursor] - '0')
			timers[timer]++
			result++
		}
	}

	for day := 1; day <= 80; day++ {
		newfishes := timers[0]
		result += newfishes

		timers[0] = timers[1]
		timers[1] = timers[2]
		timers[2] = timers[3]
		timers[3] = timers[4]
		timers[4] = timers[5]
		timers[5] = timers[6]
		timers[6] = timers[7] + newfishes
		timers[7] = timers[8]
		timers[8] = newfishes
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
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
