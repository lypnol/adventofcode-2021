package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type board struct {
	// lookup contains the mapping between a number on the board and its coordinates
	lookup map[int][2]int

	// rows contains the number of marked numbers per row
	rows [5]int

	// columns contains the number of marked numbers per column
	columns [5]int

	// sum contains the sum of all unmarked numbers on the board
	sum int
}

func run(s string) int {
	lines := strings.Split(s, "\n")

	// Parse the list of drawn numbers
	raffle := make([]int, 0)
	for _, v := range strings.Split(lines[0], ",") {
		number, _ := strconv.Atoi(v)
		raffle = append(raffle, number)
	}

	// Parse the list of boards
	boards := make([]board, 0)
	index := -1 // Hack off-by-one error
	row := 0
	for _, line := range lines[1:] {
		if len(line) == 0 {
			index++
			row = 0

			boards = append(boards, board{
				lookup: make(map[int][2]int),
			})

			continue
		}

		for column, v := range strings.Fields(line) {
			number, _ := strconv.Atoi(v)

			boards[index].lookup[number] = [2]int{row, column}
			boards[index].sum += number
		}

		row++
	}

	// Run bingo
	for _, number := range raffle {
		for idx := range boards {
			if coordinates, ok := boards[idx].lookup[number]; ok {
				row, column := coordinates[0], coordinates[1]

				boards[idx].rows[row]++
				boards[idx].columns[column]++
				boards[idx].sum -= number

				if boards[idx].rows[row] == 5 {
					return boards[idx].sum * number
				}

				if boards[idx].columns[column] == 5 {
					return boards[idx].sum * number
				}
			}
		}
	}

	return 0
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
