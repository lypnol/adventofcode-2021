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

func computeCost2(puzzle *Puzzle, tPos int) int {
	var cost int
	for _, hPos := range puzzle.positions {
		delta := hPos - tPos
		if delta < 0 {
			delta = -delta
		}
		cost += delta * (delta + 1) / 2
	}
	return cost
}

func puzzle(puzzle Puzzle) int {
	//fmt.Printf("Horizontal positions : %v\n", puzzle.positions)
	sort.Ints(puzzle.positions)
	//fmt.Printf("Horizontal positions : %v\n", puzzle.positions)

	sum := 0
	for _, v := range puzzle.positions {
		sum += v
	}
	average := sum / len(puzzle.positions)

	cost1 := computeCost2(&puzzle, average)
	cost2 := computeCost2(&puzzle, average+1)
	var cost int
	if cost1 > cost2 {
		cost = cost2
	} else {
		cost = cost1
	}
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
