package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const NROWS = 10
const NCOLS = 10
const NCYCLES = 100

type Pos struct {
	row, col int
}

func (pos Pos) neighbors(nrows, ncols int) []Pos {
	left_space := pos.col > 0
	right_space := pos.col+1 < ncols
	res := make([]Pos, 0, 4)
	if pos.row > 0 {
		if left_space {
			res = append(res, Pos{pos.row - 1, pos.col - 1})
		}
		res = append(res, Pos{pos.row - 1, pos.col})
		if right_space {
			res = append(res, Pos{pos.row - 1, pos.col + 1})
		}
	}
	if left_space {
		res = append(res, Pos{pos.row, pos.col - 1})
	}
	if right_space {
		res = append(res, Pos{pos.row, pos.col + 1})
	}
	if pos.row+1 < nrows {
		if left_space {
			res = append(res, Pos{pos.row + 1, pos.col - 1})
		}
		res = append(res, Pos{pos.row + 1, pos.col})
		if right_space {
			res = append(res, Pos{pos.row + 1, pos.col + 1})
		}
	}
	return res
}

func (pos Pos) flash(board [][]int) []Pos {
	res := make([]Pos, 0)
	if board[pos.row][pos.col] < 9 {
		return res
	}
	nrows := len(board)
	ncols := len(board[0])
	for _, neighbor := range pos.neighbors(nrows, ncols) {
		if board[neighbor.row][neighbor.col] > 9 {
			continue
		}
		board[neighbor.row][neighbor.col] += 1
		if board[neighbor.row][neighbor.col] > 9 {
			res = append(res, neighbor)
		}
	}
	return res
}

func parse(s string) [][]int {
	res := make([][]int, 0, NROWS)
	for _, row := range strings.Split(s, "\n") {
		r := make([]int, 0, NCOLS)
		for cursor := 0; cursor < len(row); cursor++ {
			r = append(r, int(row[cursor]-'0'))
		}
		res = append(res, r)
	}
	return res
}

func reset(board [][]int) int {
	res := 0
	for r, row := range board {
		for c, v := range row {
			if v > 9 {
				board[r][c] = 0
				res += 1
			}
		}
	}
	return res
}

func run(s string) int {
	// Your code goes here
	board := parse(s)
	nrows := len(board)
	ncols := len(board[0])
	res := 0
	for cycle := 0; cycle < NCYCLES; cycle++ {
		flashes := make([]Pos, 0)
		for r := 0; r < nrows; r++ {
			for c := 0; c < ncols; c++ {
				board[r][c] += 1
				if board[r][c] > 9 {
					flashes = append(flashes, Pos{r, c})
				}
			}
		}
		for len(flashes) > 0 {
			pos := flashes[len(flashes)-1]
			flashes = flashes[:len(flashes)-1]
			for _, new := range pos.flash(board) {
				flashes = append(flashes, new)
			}
		}
		res += reset(board)
	}
	return res
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
