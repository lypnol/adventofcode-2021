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
	heightMap [][]int
	inBassin [][]bool
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
	var inBassin [][]bool
	for _, line := range strings.Split(inputStr, "\n") {
		if len(line) > 0 {
			var heightLine []int
			for _, col := range strings.Split(line, "") {
				val, _ := strconv.Atoi(col)
				heightLine = append(heightLine, val)
			}
			heightMap = append(heightMap, heightLine)
			inBassinLine := make([]bool, len(heightLine))
			inBassin = append(inBassin, inBassinLine)
		}
	}
	return Puzzle{
		heightMap: heightMap,
		height: len(heightMap),
		width: len(heightMap[0]),
		inBassin: inBassin,
	}
}

func (p *Puzzle) exploreBassin(line int, col int) int {
	if p.inBassin[line][col] {
		return 0
	} else {
		p.inBassin[line][col] = true
	}
	value := p.heightMap[line][col]
	if value == 9 {
		return 0
	}
	count := 1
	if (col > 0) && p.heightMap[line][col-1] > value {
		count += p.exploreBassin(line, col-1)
	}
	if (col < p.width-1) && p.heightMap[line][col+1] > value {
		count += p.exploreBassin(line, col+1)
	}
	if (line > 0) && p.heightMap[line-1][col] > value {
		count += p.exploreBassin(line-1, col)
	}
	if (line < p.height-1) && p.heightMap[line+1][col] > value {
		count += p.exploreBassin(line+1, col)
	}
	return count
}


func puzzle(puzzle Puzzle) int {
	var bassinSize []int
	for i := 0; i < puzzle.height; i++ {
		for j := 0; j < puzzle.width; j++ {
			if val := puzzle.isLowPoint(i, j); val > 0 {
				size := puzzle.exploreBassin(i, j)
				//fmt.Printf("Bassin of size %d from [%d, %d]\n", size, i, j)
				bassinSize = append(bassinSize, size)
			}
		}
	}
	sort.Ints(bassinSize)
	l := len(bassinSize)
	return bassinSize[l-1] * bassinSize[l-2] * bassinSize[l-3]
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
