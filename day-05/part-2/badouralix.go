package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) int {
	// Your code goes here
	lines := strings.Split(s, "\n")
	var board [1000][1000]int
	result := 0

	for _, line := range lines {
		ends := strings.Split(line, " -> ")
		src := strings.Split(ends[0], ",")
		dst := strings.Split(ends[1], ",")

		x1, _ := strconv.Atoi(src[0])
		y1, _ := strconv.Atoi(src[1])
		x2, _ := strconv.Atoi(dst[0])
		y2, _ := strconv.Atoi(dst[1])

		if x1 == x2 {
			if y1 > y2 {
				y1, y2 = y2, y1
			}
			for i := y1; i <= y2; i++ {
				board[i][x1]++
				if board[i][x1] == 2 {
					result++
				}
			}
		} else if y1 == y2 {
			if x1 > x2 {
				x1, x2 = x2, x1
			}
			for j := x1; j <= x2; j++ {
				board[y1][j]++
				if board[y1][j] == 2 {
					result++
				}
			}
		} else if x2-x1 == y2-y1 {
			diff := x2 - x1
			if diff >= 0 {
				for i := 0; i <= diff; i++ {
					board[y1+i][x1+i]++
					if board[y1+i][x1+i] == 2 {
						result++
					}
				}
			} else {
				for i := 0; i <= -diff; i++ {
					board[y1-i][x1-i]++
					if board[y1-i][x1-i] == 2 {
						result++
					}
				}
			}
		} else if x2-x1 == -(y2 - y1) {
			diff := x2 - x1
			if diff >= 0 {
				for i := 0; i <= diff; i++ {
					board[y1-i][x1+i]++
					if board[y1-i][x1+i] == 2 {
						result++
					}
				}
			} else {
				for i := 0; i <= -diff; i++ {
					board[y1+i][x1-i]++
					if board[y1+i][x1-i] == 2 {
						result++
					}
				}
			}
		}
	}

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
