package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(input []byte) int16 {
	var previous1, previous2, previous3, actual int16
	var result int16

	n := len(input)

	cursor := 0
	for input[cursor] != '\n' {
		previous1 = previous1*10 + int16(input[cursor] & 0xf)
		cursor++
	}
	cursor++
	for input[cursor] != '\n' {
		previous2 = previous2*10 + int16(input[cursor] & 0xf)
		cursor++
	}
	cursor++
	for input[cursor] != '\n' {
		previous3 = previous3*10 + int16(input[cursor] & 0xf)
		cursor++
	}
	cursor++
	for i := 3; i < 1999; i++ {
		actual = 0
		for input[cursor] != '\n' {
			actual = actual*10 + int16(input[cursor] & 0xf)
			cursor++
		}
		cursor++
		if actual > previous1 {
			result++
		}
		previous1 = previous2
		previous2 = previous3
		previous3 = actual
	}
	actual = 0
	for cursor < n && input[cursor] != '\n' {
		actual = actual*10 + int16(input[cursor] & 0xf)
		cursor++
	}
	if actual > previous1 {
		result++
	}

	return result
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	input, _ := ioutil.ReadAll(os.Stdin)

	// Start resolution
	start := time.Now()
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
