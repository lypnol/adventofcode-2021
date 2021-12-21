package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)
type Puzzle struct {
	initialList []int
}

func parseData(input string) Puzzle {
	var initialList []int
	for _, line := range strings.Split(input, "\n") {
		if len(line) > 0 {
			values := strings.Split(line, ",")
			for _, valueStr := range values {
				value, _ := strconv.Atoi(valueStr)
				initialList = append(initialList, value)
			}
		}
	}
	return Puzzle{initialList: initialList}
}

func computeNextState(state [9]int) [9]int {
	var newState [9]int
	// all none zero aged lanternfish decrease its age
	for i := 1; i <= 8; i++ {
		newState[i-1] = state[i]
	}
	newState[6] += state[0]
	newState[8] += state[0]
	return newState
}

func countFishes(state [9]int) int {
	var sum int
	for i := 0; i < 9; i++ {
		sum += state[i]
	}
	return sum
}

func puzzle(puzzle Puzzle) int {
	var state [9]int
	for _, value := range puzzle.initialList {
		state[value] += 1
	}
	//fmt.Printf("Initial state (%d): %v\n", countFishes(state), state)
	for d := 1; d <= 256; d++ {
		state = computeNextState(state)
		//fmt.Printf("Day[%d] (%d): %v\n", d, countFishes(state), state)
	}
	return countFishes(state)
}

func run(s string) interface{} {
	// Your code goes here
	data := parseData(s)
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
