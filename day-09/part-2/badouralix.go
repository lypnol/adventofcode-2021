package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
	"time"
)

func run(s string) int {
	// Your code goes here
	lines := strings.Split(s, "\n")
	height := len(lines)
	width := len(lines[0])

	// `coloring` maps a location to a color represented as an int
	coloring := make([]int, height*(width+1))
	// `current` holds the current color, different from 0 to distinguish it from default values in coloring
	current := 1
	// `aliases` is a map merging colors from the same basin
	aliases := map[int]int{1: 1}
	// `occurrences` is the map of color to number of occurrences in coloring
	occurrences := map[int]int{}

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {
			// Skip locations of hight 9
			if s[i*(width+1)+j] == '9' {
				continue
			}

			if j != 0 && coloring[i*(width+1)+(j-1)] != 0 {
				// Pick the color from the left location
				coloring[i*(width+1)+j] = coloring[i*(width+1)+(j-1)]

				if i != 0 && coloring[(i-1)*(width+1)+j] != 0 {
					// Update aliases while ensuring the tree structure of the aliases
					// The color of the left location is guaranteed not to be aliased
					// There is no guarantee on the color of the top location
					// Given that this could override an existing alias, I have no idea why this works
					aliases[coloring[(i-1)*(width+1)+j]] = coloring[i*(width+1)+j]
				}
			} else if j != 0 && i != 0 && coloring[(i-1)*(width+1)+j] != 0 {
				// Pick the color from the top location
				coloring[i*(width+1)+j] = coloring[(i-1)*(width+1)+j]
			} else {
				// Pick a new color
				coloring[i*(width+1)+j] = current
				aliases[current] = current
				current++
			}

			// Update occurrences
			if _, ok := occurrences[coloring[i*(width+1)+j]]; !ok {
				occurrences[coloring[i*(width+1)+j]] = 0
			}
			occurrences[coloring[i*(width+1)+j]]++
		}
	}

	// Normalize aliases to ensure each color is aliased to the default basin color
	for color, alias := range aliases {
		for alias != aliases[alias] {
			alias = aliases[alias]
		}
		aliases[color] = alias
	}

	// `sizes` is the map of color to number of occurrences in coloring after applying aliases
	sizes := make([]int, current)
	for color, occurrence := range occurrences {
		sizes[aliases[color]] += occurrence
	}

	sort.Sort(sort.Reverse(sort.IntSlice(sizes)))
	return sizes[0] * sizes[1] * sizes[2]
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
