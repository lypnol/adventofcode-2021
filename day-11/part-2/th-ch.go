package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const size = 10

func getNeighbors(i int) []int {
	x := i % size
	y := i / size

	neighbors := [][2]int{
		[2]int{x - 1, y - 1},
		[2]int{x - 1, y},
		[2]int{x - 1, y + 1},
		[2]int{x, y - 1},
		[2]int{x, y + 1},
		[2]int{x + 1, y - 1},
		[2]int{x + 1, y},
		[2]int{x + 1, y + 1},
	}

	computedNeighbors := make([]int, 0)
	for _, neighbor := range neighbors {
		if neighbor[0] < 0 || neighbor[0] >= size || neighbor[1] < 0 || neighbor[1] >= size {
			continue
		}

		computedNeighbor := neighbor[1]*size + neighbor[0]
		computedNeighbors = append(computedNeighbors, computedNeighbor)
	}

	return computedNeighbors
}

func run(s string) interface{} {
	// Your code goes here
	s = strings.ReplaceAll(s, "\n", "")
	octopuses := make([]int, len(s))
	for i := 0; i < len(s); i++ {
		nb, _ := strconv.Atoi(string(s[i]))
		octopuses[i] = nb
	}

	queue := make([]int, 0)

	for step := 1; step >= 1; step++ {
		for i := 0; i < len(octopuses); i++ {
			octopuses[i]++
			if octopuses[i] > 9 {
				queue = append(queue, i)
			}
		}

		flashed := make([]int, 0)

		for len(queue) > 0 {
			i := queue[0]
			queue = queue[1:]

			hasAlreadyFlashed := false
			for _, j := range flashed {
				if j == i {
					hasAlreadyFlashed = true
					break
				}
			}
			if hasAlreadyFlashed {
				continue
			}

			flashed = append(flashed, i)

			neighbors := getNeighbors(i)
			for _, neighbor := range neighbors {
				octopuses[neighbor]++
				if octopuses[neighbor] == 10 {
					queue = append(queue, neighbor)
				}
			}
		}

		for i := 0; i < len(octopuses); i++ {
			if octopuses[i] > 9 {
				octopuses[i] = 0
			}
		}

		if len(flashed) == len(octopuses) {
			// All flashed!
			return step
		}
	}

	return -1
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
