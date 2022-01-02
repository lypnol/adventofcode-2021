package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type Display struct {
	inputs  []string
	outputs []string
}

type Puzzle struct {
	displays []Display
}

func parseData(inputStr string) Puzzle {
	var displays []Display
	for _, line := range strings.Split(inputStr, "\n") {
		if len(line) > 0 {
			inputOutput := strings.Split(line, " | ")
			input := strings.Split(inputOutput[0], " ")
			output := strings.Split(inputOutput[1], " ")

			displays = append(displays, Display{
				inputs:  input,
				outputs: output,
			})
		}
	}
	return Puzzle{displays: displays}
}

func puzzle(puzzle Puzzle) int {
	var count int
	for _, display := range puzzle.displays {
		for _, output := range display.outputs {
			switch len(output) {
			case 2:
				//fmt.Printf("%s -> %d\n", output, len(output))
				count++
			case 3:
				//fmt.Printf("%s -> %d\n", output, len(output))
				count++
			case 4:
				//fmt.Printf("%s -> %d\n", output, len(output))
				count++
			case 7:
				//fmt.Printf("%s -> %d\n", output, len(output))
				count++
			}
		}
	}
	return count
}

func run(s string) interface{} {
	// Your code goes here
	data := parseData(s)
	result := puzzle(data)
	return result
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	var input []byte
	var err error
	if len(os.Args) > 1 {
		// Read inputs from file for local debugging
		input, err = ioutil.ReadFile(os.Args[1])
		if err != nil {
			panic(err)
		}
		// Remove extra newline
		input = input[:len(input)-1]
	} else {
		// Read inputs from stdin
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
