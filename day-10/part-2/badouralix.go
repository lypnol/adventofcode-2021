package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
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
		'(': 1,
		'[': 2,
		'{': 3,
		'<': 4,
	}
)

func run(s string) int {
	// Your code goes here
	scores := make([]int, 0)

	for _, line := range strings.Split(s, "\n") {
		idx := 0
		score := 0
		stack := make([]rune, len(line))
		valid := true

	loop:
		for _, char := range line {
			switch char {
			case ')', ']', '}', '>':
				idx--
				if idx < 0 || stack[idx] != expected[char] {
					valid = false
					break loop
				}
			default:
				stack[idx] = char
				idx++
			}
		}

		if !valid {
			continue
		}

		for i := idx - 1; i >= 0; i-- {
			score *= 5
			score += values[stack[i]]
		}
		scores = append(scores, score)
	}

	sort.Ints(scores)
	return scores[len(scores)/2]
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
