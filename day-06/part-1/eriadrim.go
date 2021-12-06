package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

const(
	p1 int = 1401
	p2 int = 1191
	p3 int = 1154
	p4 int = 1034
	p5 int = 950
)

func run(s []byte) int {
	var char byte
	var q1, q2, q3, q4, q5 byte = 0, 0, 0, 0, 0
	for cursor := 0; cursor < len(s); cursor+=2 {
		char = s[cursor]
		if char == '1' {
			q1++
		} else if char == '2' {
			q2++
		} else if char == '3' {
			q3++
		} else if char == '4' {
			q4++
		} else if char == '5' {
			q5++
		}
	}

	return p1*int(q1) + p2*int(q2) + p3*int(q3) + p4*int(q4) + p5*int(q5)
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
