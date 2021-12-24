package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const iterations = 2

type Point int

func NewPoint(i, j int) Point {
	return Point(i*1_000 + j)
}

func run(s string) int {
	// Your code goes here
	algorithm := make([]bool, 512)
	image := make(map[Point]struct{}, 100*100)

	split := strings.Split(s, "\n\n")
	for idx, pixel := range split[0] {
		if pixel == '#' {
			algorithm[idx] = true
		}
	}
	for i, line := range strings.Split(split[1], "\n") {
		for j, pixel := range line {
			if pixel == '#' {
				image[NewPoint(i, j)] = struct{}{}
			}
		}
	}

	needToImplementAHackBecauseTheInputImageIsInfiniteAndTheFirstPixelOfTheAlgorithmIsLight := false
	if algorithm[0] {
		needToImplementAHackBecauseTheInputImageIsInfiniteAndTheFirstPixelOfTheAlgorithmIsLight = true
	}

	for k := 1; k <= iterations; k++ {
		new := make(map[Point]struct{}, 100*100)

		// On each iteration, the grid size is increased by two layers in all directions
		// This allows the hack for the infinite input image to work without much trouble
		// The inner layer is required to expand the input image border normally
		// The outer layer is useful to keep a lit border every other iteration
		for i := 0; i < 100+2*(k+1); i++ {
			for j := 0; j < 100+2*(k+1); j++ {
				value := 0
				for di := -1; di <= 1; di++ {
					for dj := -1; dj <= 1; dj++ {
						value *= 2

						if _, ok := image[NewPoint(i-1+di, j-1+dj)]; ok {
							value += 1
							continue
						}

						// When the algorithm turns on pixels with a value of 0, and when k is even, all pixels outside
						// the current window are lit, and should increase the value of the current pixel accordingly
						if !needToImplementAHackBecauseTheInputImageIsInfiniteAndTheFirstPixelOfTheAlgorithmIsLight {
							continue
						}

						if k%2 == 1 {
							continue
						}

						if 0 <= i-1+di && i-1+di < 100+2*k-1 && 0 <= j-1+dj && j-1+dj < 100+2*k-1 {
							continue
						}

						value += 1
					}
				}

				if algorithm[value] {
					new[NewPoint(i, j)] = struct{}{}
				}
			}
		}

		image = new
	}

	return len(image)
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
