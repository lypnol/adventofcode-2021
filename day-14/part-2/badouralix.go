package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
	"time"
)

const iterations = 40

type Pair [2]byte

func rec(p Pair, n int, mapping map[Pair][2]Pair, cache map[Pair]map[int]map[Pair]int) map[Pair]int {
	if _, ok := cache[p]; !ok {
		cache[p] = make(map[int]map[Pair]int)
	}

	if _, ok := cache[p][n]; ok {
		return cache[p][n]
	}

	cache[p][n] = make(map[Pair]int)

	if n == 0 {
		cache[p][n][p]++
		return cache[p][n]
	}

	for k, v := range rec(mapping[p][0], n-1, mapping, cache) {
		cache[p][n][k] += v
	}
	for k, v := range rec(mapping[p][1], n-1, mapping, cache) {
		cache[p][n][k] += v
	}

	return cache[p][n]
}

func run(s string) int {
	// Your code goes here
	mapping := make(map[Pair][2]Pair)
	cache := make(map[Pair]map[int]map[Pair]int)
	min, max := math.MaxInt64, 0

	split := strings.Split(s, "\n\n")
	pattern := split[0]

	for _, line := range strings.Split(split[1], "\n") {
		rule := strings.Split(line, " -> ")
		mapping[Pair{rule[0][0], rule[0][1]}] = [2]Pair{Pair{rule[0][0], rule[1][0]}, Pair{rule[1][0], rule[0][1]}}
	}

	occurences := make(map[byte]int)
	occurences[pattern[0]]++
	occurences[pattern[len(pattern)-1]]++

	for i := 0; i < len(pattern)-1; i++ {
		for p, v := range rec(Pair{pattern[i], pattern[i+1]}, iterations, mapping, cache) {
			occurences[p[0]] += v
			occurences[p[1]] += v
		}
	}

	for _, v := range occurences {
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}

	return (max - min) / 2
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
