package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const MaxScore = 21
const MaxSpace = 10

// The cache is an array so that we do not have to write code to initialize it
// Passing the cache as a parameter probably passes it by value, making the memoization ineffective
// So handmade memoization with a global variable it is
var cache = [11][11][21][21][2][2]int64{}

func rec(spaces [2]int64, scores [2]int64, player int) [2]int64 {
	if cache[spaces[0]][spaces[1]][scores[0]][scores[1]][player][0] != 0 || cache[spaces[0]][spaces[1]][scores[0]][scores[1]][player][1] != 0 {
		return cache[spaces[0]][spaces[1]][scores[0]][scores[1]][player]
	}

	counters := [2]int64{}

	// Magic map giving the number of occurrences of each value of the sum of three dice rolls
	for dice, copies := range map[int64]int64{3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1} {
		newspace := (spaces[player]+dice-1)%MaxSpace + 1

		if scores[player]+newspace >= MaxScore {
			counters[player] += copies
		} else {
			newspaces := [2]int64{}
			newspaces[player] = newspace
			newspaces[1-player] = spaces[1-player]

			newscores := [2]int64{}
			newscores[player] = scores[player] + newspace
			newscores[1-player] = scores[1-player]

			c := rec(newspaces, newscores, 1-player)
			counters[0] += copies * c[0]
			counters[1] += copies * c[1]
		}
	}

	cache[spaces[0]][spaces[1]][scores[0]][scores[1]][player] = counters

	return counters
}

func run(s string) int64 {
	// Your code goes here
	spaces := [2]int64{}

	for idx, line := range strings.Split(s, "\n") {
		if len(line) == 29 {
			spaces[idx] = int64(line[28] - '0')
		} else {
			spaces[idx] = 10
		}
	}

	c := rec(spaces, [2]int64{0, 0}, 0)

	if c[0] < c[1] {
		return c[1]
	}
	return c[0]
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
