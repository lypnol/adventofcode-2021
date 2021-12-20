package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Cell struct {
	value int
	marked bool

}

type Puzzle struct {
	numbersToDraw []int
	grids [][5][5]Cell
}

func parseData(input string) Puzzle {

	lines := strings.Split(input, "\n")
	var numbersToDraw []int
	for _, nbAsStr := range strings.Split(lines[0], ",") {
		parsedNb, _ := strconv.Atoi(nbAsStr)
		numbersToDraw = append(numbersToDraw, parsedNb)
	}

	var grids [][5][5]Cell

	unInitCell := Cell{
		value:  0,
		marked: false,
	}
	var currentGrid [5][5]Cell = [5][5]Cell {
		{unInitCell, unInitCell, unInitCell, unInitCell, unInitCell},
		{unInitCell, unInitCell, unInitCell, unInitCell, unInitCell},
		{unInitCell, unInitCell, unInitCell, unInitCell, unInitCell},
		{unInitCell, unInitCell, unInitCell, unInitCell, unInitCell},
		{unInitCell, unInitCell, unInitCell, unInitCell, unInitCell},
	}
	var currentLineGrid int = -1

	for _, line := range lines[1:] {
		//fmt.Printf("currentLine grid = %d\n", currentLineGrid)
		if currentLineGrid == -1 {
			currentLineGrid++
			continue
		}
		//fmt.Printf("Line %d : %v (current grid line : %d)\n", idx, line, currentLineGrid)
		var currentColNb int = 0
		for _, nbAsStr := range strings.Split(line, " ") {
			if len(nbAsStr) > 0 {
				parsedNb, _ := strconv.Atoi(nbAsStr)
				//fmt.Printf("Parse[%d][%d] \"%s \"-> %d\n", currentLineGrid, colNb, nbAsStr, parsedNb)
				currentGrid[currentLineGrid][currentColNb].value = parsedNb
				currentColNb++
			}
		}
		currentLineGrid++
		if currentLineGrid == 5 {
			grids = append(grids, currentGrid)
			currentLineGrid = -1
			//fmt.Printf("Grid finished on line %d, : %v\n", idx+2, currentGrid)
		}
	}
	return Puzzle{
		numbersToDraw: numbersToDraw,
		grids: grids,
	}
}

func printPuzzle(puzzle *Puzzle) {
	fmt.Printf("%v\n", puzzle.numbersToDraw)
	for _, grid := range puzzle.grids {
		fmt.Println()
		for _, line := range grid {
			fmt.Printf("%v\n", line)
		}
	}
}

func isWinningGrid(grid [5][5]Cell) bool {
	for lineIdx := 0; lineIdx < 5; lineIdx++ {
		countMarked := 0
		for colIdx := 0; colIdx < 5; colIdx++ {
			if grid[lineIdx][colIdx].marked {
				countMarked++
			}
		}
		if countMarked == 5 {
			return true
		}
	}
	for colIdx := 0; colIdx < 5; colIdx++ {
		countMarked := 0
		for lineIdx := 0; lineIdx < 5; lineIdx++ {
			if grid[lineIdx][colIdx].marked {
				countMarked++
			}
		}
		if countMarked == 5 {
			return true
		}
	}
	return false
}

func sumUnmarked(grid [5][5]Cell) int {
	sum := 0
	for _, line := range grid {
		for _, cell := range line {
			if !cell.marked {
				sum += cell.value
			}
		}
	}
	return sum
}

func markGrids(grids *[][5][5]Cell, value int) {
	for gridIdx := 0; gridIdx < len(*grids); gridIdx++ {
		for lineIdx := 0; lineIdx < 5; lineIdx++ {
			for colIdx := 0; colIdx < 5; colIdx++ {
				if (*grids)[gridIdx][lineIdx][colIdx].value == value {
					(*grids)[gridIdx][lineIdx][colIdx].marked = true
				}
			}
		}
	}
}

func puzzle(puzzle Puzzle) int {
	//printPuzzle(&puzzle)
	for _, value := range puzzle.numbersToDraw {
		markGrids(&(puzzle.grids), value)
		for gridIx := 0; gridIx < len(puzzle.grids); gridIx++ {
			if isWinningGrid(puzzle.grids[gridIx]) {
				sum := sumUnmarked(puzzle.grids[gridIx])
				result := value * sum
				// fmt.Printf("grid sum=%d, result=%d\n", sum, result)
				return result
			}

		}

	}
	return 0
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
