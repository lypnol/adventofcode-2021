package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"time"
)

const (
	BoardSize  = 10
	iterations = 100
)

type Game struct {
	Board      [][]int
	FlashCount int
}

func NewGame(s string) Game {
	board := make([][]int, BoardSize)
	for i := 0; i < BoardSize; i++ {
		board[i] = make([]int, BoardSize)

		for j := 0; j < BoardSize; j++ {
			board[i][j] = int(s[i*(BoardSize+1)+j] - '0')
		}
	}

	return Game{Board: board, FlashCount: 0}
}

func (g *Game) Step() {
	stack := NewStack()

	for i := 0; i < BoardSize; i++ {
		for j := 0; j < BoardSize; j++ {
			if g.Board[i][j] == 9 {
				stack.Push(i, j)
				continue
			}

			g.Board[i][j]++
		}
	}

	for stack.Len() != 0 {
		i, j := stack.Pop()

		if g.Board[i][j] == 0 {
			continue
		}

		g.Board[i][j]++

		if g.Board[i][j] > 9 {
			g.Board[i][j] = 0
			g.FlashCount++

			for di := -1; di <= 1; di++ {
				if i+di < 0 || i+di >= BoardSize {
					continue
				}

				for dj := -1; dj <= 1; dj++ {
					if j+dj < 0 || j+dj >= BoardSize {
						continue
					}

					if di == 0 && dj == 0 {
						continue
					}

					stack.Push(i+di, j+dj)
				}
			}
		}
	}
}

func (g Game) String() string {
	output := "+-"
	for j := 0; j < BoardSize; j++ {
		output += "-"
	}
	output += "-+\n"

	for i := 0; i < BoardSize; i++ {
		output += "| "
		for j := 0; j < BoardSize; j++ {
			output += strconv.Itoa(g.Board[i][j])
		}
		output += " |\n"
	}

	output += "+-"
	for j := 0; j < BoardSize; j++ {
		output += "-"
	}
	output += "-+"

	return output
}

type Stack struct {
	index int
	store [][2]int
}

func NewStack() Stack {
	store := make([][2]int, 8*BoardSize*BoardSize)
	return Stack{index: 0, store: store}
}

func (s Stack) Len() int {
	return s.index
}

func (s *Stack) Pop() (int, int) {
	if s.index <= 0 {
		panic("tried to pop from empty stack")
	}

	s.index--
	return s.store[s.index][0], s.store[s.index][1]
}

func (s *Stack) Push(i, j int) {
	s.store[s.index] = [2]int{i, j}
	s.index++
}

func run(s string) int {
	// Your code goes here
	game := NewGame(s)
	for i := 0; i < iterations; i++ {
		game.Step()
	}
	return game.FlashCount
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
