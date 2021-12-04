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

	// rows contains the status of all numbers on the board indexed by row
	rows [5][5]bool

	// columns contains the status of all numbers on the board indexed by columns
	columns [5][5]bool

	// sum contains the sum of all unmarked numbers on the board
	sum int

	// won indicates whether the board already won or not
	won bool
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
			boards[index].rows[row][column] = false
			boards[index].columns[column][row] = false
			boards[index].sum += number
		}

		row++
	}

	// Run bingo
	winners := make([]int, 0)
	for _, number := range raffle {
		for idx := range boards {
			if boards[idx].won {
				continue
			}

			if coordinates, ok := boards[idx].lookup[number]; ok {
				row, column := coordinates[0], coordinates[1]

				boards[idx].rows[row][column] = true
				boards[idx].columns[column][row] = true
				boards[idx].sum -= number

				won := true
				for _, v := range boards[idx].rows[row] {
					won = won && v
				}
				boards[idx].won = boards[idx].won || won

				won = true
				for _, v := range boards[idx].columns[column] {
					won = won && v
				}
				boards[idx].won = boards[idx].won || won

				if boards[idx].won {
					winners = append(winners, idx)
				}

				if len(winners) == len(boards) {
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
