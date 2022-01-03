package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

func run(s string) int {
	// Your code goes here
	dice := 6
	player := 0
	scores := [2]int{0, 0}
	spaces := [2]int{}
	rolls := 0

	for _, line := range strings.Split(s, "\n") {
		if len(line) == 29 {
			spaces[player] = int(line[28] - '0')
		} else {
			spaces[player] = 10
		}

		player = 1 - player
	}

	for {
		spaces[player] += dice
		if spaces[player] > 10 {
			spaces[player] -= 10
		}
		scores[player] += spaces[player]

		// A bit of magic, the deterministic dice always rolls one less than the previous roll
		dice--
		if dice < 0 {
			dice = 9
		}
		rolls++

		if scores[player] >= 1000 {
			player = 1 - player
			break
		}

		player = 1 - player
	}

	// Fix off-by-factor-3 error due to counting a single roll for each loop instead of 3
	return 3 * scores[player] * rolls
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
