package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

var (
	expected = map[rune]rune{
		')': '(',
		']': '[',
		'}': '{',
		'>': '<',
	}
	values = map[rune]int{
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137,
	}
)

func run(s string) int {
	// Your code goes here
	result := 0

	for _, line := range strings.Split(s, "\n") {
		idx := 0
		stack := make([]rune, len(line))

	loop:
		for _, char := range line {
			switch char {
			case ')', ']', '}', '>':
				idx--
				if idx < 0 || stack[idx] != expected[char] {
					result += values[char]
					break loop
				}
			default:
				stack[idx] = char
				idx++
			}
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
