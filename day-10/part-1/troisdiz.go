package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type CodeLine string

type Puzzle struct {
	lines []CodeLine
}

func (cl *CodeLine) findFirstIllegalCharacter() (rune, bool) {
	var rStack []rune
	for _, r := range *cl {
		switch r {
		case rune('<'):
			rStack = append(rStack, r)
		case rune('('):
			rStack = append(rStack, r)
		case rune('{'):
			rStack = append(rStack, r)
		case rune('['):
			rStack = append(rStack, r)
		case rune('>'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('<') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return rune('>'), true
			}
		case rune(')'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('(') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return rune(')'), true
			}
		case rune('}'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('{') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return rune('}'), true
			}
		case rune(']'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('[') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return rune(']'), true
			}
		}
	}
	if len(rStack) == 0 {
		return 0, false
	} else {
		return 0, true
	}
}

func getScore(r rune) int {
	switch r {
	case rune(')'):
		return 3
	case rune(']'):
		return 57
	case rune('}'):
		return 1197
	case rune('>'):
		return 25137
	}
	return 0
}

func parseData(inputStr string) Puzzle {
	var lines []CodeLine
	for _, line := range strings.Split(inputStr, "\n") {
		if len(line) > 0 {
			lines = append(lines, CodeLine(line))
		}
	}
	return Puzzle{
		lines: lines,
	}
}

func puzzle(puzzle Puzzle) int {
	var count int
	for _, l := range puzzle.lines {
		r, isCorrect := l.findFirstIllegalCharacter()
		if isCorrect {
			count += getScore(r)
		}
	}
	return count
}

func run(s string) interface{} {
	// Your code goes here
	data := parseData(s)
	// fmt.Printf("%v\n", data)
	result := puzzle(data)
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
