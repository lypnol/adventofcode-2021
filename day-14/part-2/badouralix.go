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

func rec(p string, n int, mapping map[[2]byte]string, cache map[string]map[int]map[byte]int) map[byte]int {
	if _, ok := cache[p]; !ok {
		cache[p] = make(map[int]map[byte]int)
	}

	if _, ok := cache[p][n]; ok {
		return cache[p][n]
	}

	cache[p][n] = make(map[byte]int)

	if n == 0 {
		for _, c := range p {
			cache[p][n][byte(c)]++
		}
		return cache[p][n]
	}

	if len(p) > 2 {
		for k, v := range rec(p[0:2], n, mapping, cache) {
			cache[p][n][k] += v
		}
		cache[p][n][p[1]]--
		for k, v := range rec(p[1:], n, mapping, cache) {
			cache[p][n][k] += v
		}

		return cache[p][n]
	}

	for k, v := range rec(p[0:1]+mapping[[2]byte{p[0], p[1]}], n-1, mapping, cache) {
		cache[p][n][k] += v
	}
	cache[p][n][mapping[[2]byte{p[0], p[1]}][0]]--
	for k, v := range rec(mapping[[2]byte{p[0], p[1]}]+p[1:], n-1, mapping, cache) {
		cache[p][n][k] += v
	}

	return cache[p][n]
}

func run(s string) int {
	// Your code goes here
	mapping := make(map[[2]byte]string)
	cache := make(map[string]map[int]map[byte]int)
	min, max := math.MaxInt64, 0

	split := strings.Split(s, "\n\n")

	for _, line := range strings.Split(split[1], "\n") {
		rule := strings.Split(line, " -> ")
		mapping[[2]byte{rule[0][0], rule[0][1]}] = rule[1]
	}

	for _, v := range rec(split[0], iterations, mapping, cache) {
		if v < min {
			min = v
		}
		if v > max {
			max = v
		}
	}

	return max - min
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
