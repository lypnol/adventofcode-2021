package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"
)

type Puzzle struct {
	positions []int
}

func parseData(input string) Puzzle {
	var positions []int
	for _, line := range strings.Split(input, "\n") {
		if len(line) > 0 {
			values := strings.Split(line, ",")
			for _, valueStr := range values {
				value, _ := strconv.Atoi(valueStr)
				positions = append(positions, value)
			}
		}
	}
	return Puzzle{positions: positions}
}

func computeCost(puzzle *Puzzle, tPos int) int {
	var cost int
	for _, hPos := range puzzle.positions {
		delta := hPos - tPos
		if delta >= 0 {
			cost += delta
		} else {
			// delta is negative
			cost -= delta
		}
	}
	return cost
}

func puzzle(puzzle Puzzle) int {
	//fmt.Printf("Horizontal positions : %v\n", puzzle.positions)
	sort.Ints(puzzle.positions)
	//fmt.Printf("Horizontal positions : %v\n", puzzle.positions)
	count := len(puzzle.positions)
	middle := count / 2
	var cost int
	if middle*2 == count {
		cost = computeCost(&puzzle, puzzle.positions[middle])
	} else {
		cost = computeCost(&puzzle, puzzle.positions[middle])
		if candidate := computeCost(&puzzle, puzzle.positions[middle+1]); candidate < cost {
			middle = middle + 1
			cost = candidate
		}
	}
	// fmt.Printf("Target pos : %d at cost %d\n", puzzle.positions[middle], cost)
	return cost
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
