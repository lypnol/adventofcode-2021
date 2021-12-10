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
	lines := strings.Split(s, "\n")
	height := len(lines)
	width := len(lines[0])
	result := 0

	for i := 0; i < height; i++ {
		for j := 0; j < width; j++ {
			if i != 0 && s[i*(width+1)+j] >= s[(i-1)*(width+1)+j] {
				continue
			}
			if i != height-1 && s[i*(width+1)+j] >= s[(i+1)*(width+1)+j] {
				continue
			}
			if j != 0 && s[i*(width+1)+j] >= s[i*(width+1)+(j-1)] {
				continue
			}
			if j != width-1 && s[i*(width+1)+j] >= s[i*(width+1)+(j+1)] {
				continue
			}

			result += int(s[i*(width+1)+j]-'0') + 1
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
