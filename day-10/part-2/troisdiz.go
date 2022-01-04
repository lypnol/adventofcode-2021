package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
	"time"
)
type CodeLine string

type Puzzle struct {
	lines []CodeLine
}

// returns isIllegal, isComplete, unC
func (cl *CodeLine) detectComplianceAndComputeScore() (bool, bool, int) {
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
				return true, false, 0
			}
		case rune(')'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('(') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return true, false, 0
			}
		case rune('}'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('{') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return true, false, 0
			}
		case rune(']'):
			lastR := rStack[len(rStack)-1]
			if lastR == rune('[') {
				rStack = rStack[:len(rStack)-1]
			} else {
				return true, false, 0
			}
		}
	}
	if len(rStack) == 0 {
		return false, true, 0
	} else {
		score := 0
		for i := len(rStack)-1; i >=0; i-- {
			charScore := 0
			switch rStack[i] {
			case rune('('):
				charScore = 1
			case rune('['):
				charScore = 2
			case rune('{'):
				charScore = 3
			case rune('<'):
				charScore = 4
			}
			score = score * 5 + charScore
		}
		return false, false, score
	}
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
	var scores []int
	for _, l := range puzzle.lines {
		isIllegal, isComplete, score := l.detectComplianceAndComputeScore()
		if !isIllegal && !isComplete {
			scores = append(scores, score)
		}
	}
	sort.Ints(scores)
	return scores[len(scores)/2]
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
