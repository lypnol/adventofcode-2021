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
	heightMap [][]int
	height int
	width int
}

func (p *Puzzle) isLowPoint(line int, col int) int {
	value := p.heightMap[line][col]
	if (col > 0) && p.heightMap[line][col-1] <= value {
		return 0
	}
	if (col < p.width-1) && p.heightMap[line][col+1] <= value {
		return 0
	}
	if (line > 0) && p.heightMap[line-1][col] <= value {
		return 0
	}
	if (line < p.height-1) && p.heightMap[line+1][col] <= value {
		return 0
	}
	// fmt.Printf("Low point at [%d, %d] = %d\n", line, col, value)
	return value + 1
}


func parseData(inputStr string) Puzzle {
	var heightMap [][]int
	for _, line := range strings.Split(inputStr, "\n") {
		if len(line) > 0 {
			var heightLine []int
			for _, col := range strings.Split(line, "") {
				val, _ := strconv.Atoi(col)
				heightLine = append(heightLine, val)
			}
			heightMap = append(heightMap, heightLine)
		}
	}
	return Puzzle{
		heightMap: heightMap,
		height: len(heightMap),
		width: len(heightMap[0]),
	}
}

func puzzle(puzzle Puzzle) int {
	var count int
	for i := 0; i < puzzle.height; i++ {
		for j := 0; j < puzzle.width; j++ {
			if val := puzzle.isLowPoint(i, j); val > 0 {
				count += val
				// fmt.Printf("Low point at [%d, %d] = %d => count = %d\n", i, j, val, count)
			}
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
