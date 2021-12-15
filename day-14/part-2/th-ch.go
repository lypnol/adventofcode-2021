package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	lines := strings.Split(s, "\n\n")
	polymer := lines[0]
	rules := make(map[[2]byte]byte)
	currentPairs := make(map[[2]byte]int)
	for _, rule := range strings.Split(lines[1], "\n") {
		splitRule := strings.Split(rule, " -> ")
		rules[[2]byte{splitRule[0][0], splitRule[0][1]}] = splitRule[1][0]
	}

	for i := 0; i < len(polymer)-1; i++ {
		currentPairs[[2]byte{polymer[i], polymer[i+1]}]++
	}

	for step := 1; step <= 40; step++ {
		newPairs := make(map[[2]byte]int)
		for pair, nb := range currentPairs {
			newChar, ok := rules[pair]
			if !ok {
				newPairs[pair] = nb
				continue
			}

			if _, ok := newPairs[[2]byte{pair[0], newChar}]; !ok {
				newPairs[[2]byte{pair[0], newChar}] = 0
			}
			newPairs[[2]byte{pair[0], newChar}] += nb

			if _, ok := newPairs[[2]byte{newChar, pair[1]}]; !ok {
				newPairs[[2]byte{newChar, pair[1]}] = 0
			}
			newPairs[[2]byte{newChar, pair[1]}] += nb
		}

		currentPairs = newPairs
	}

	characters := map[byte]int{polymer[0]: 1, polymer[len(polymer)-1]: 1}
	if polymer[0] == polymer[len(polymer)-1] {
		characters = map[byte]int{polymer[0]: 2}
	}

	polymerLength := 1 // account for last char
	for pair, nb := range currentPairs {
		if _, ok := characters[pair[0]]; !ok {
			characters[pair[0]] = 0
		}
		characters[pair[0]] += nb

		if _, ok := characters[pair[1]]; !ok {
			characters[pair[1]] = 0
		}
		characters[pair[1]] += nb

		polymerLength += nb
	}

	minNb := polymerLength
	maxNb := 0

	for _, nb := range characters {
		nb = nb / 2 // each letter appears twice because of pairs
		if nb < minNb {
			minNb = nb
		}
		if nb > maxNb {
			maxNb = nb
		}
	}

	return maxNb - minNb
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
