package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) (result int) {
	// Your code goes here
	ssplit := strings.Split(s[15:], ", y=")
	xsplit := strings.Split(ssplit[0], "..")
	x0, _ := strconv.Atoi(xsplit[0])
	x1, _ := strconv.Atoi(xsplit[1])
	ysplit := strings.Split(ssplit[1], "..")
	y0, _ := strconv.Atoi(ysplit[0])
	y1, _ := strconv.Atoi(ysplit[1])

	// Trying to be smart
	// All points px == vx in target area and py == vy in target area are valid velocities
	// All velocities leading to vx == 0 and px in target area and py == vy in target area are valid velocities
	// Some valid velocities have vx != px and vx != 0
	// Some valid velocities have vy != py, either starting with vy > 0 or vy < 0

	// Not trying to be smart and run the simulation for literally all initial velocities
	for i := 0; i <= x1; i++ {
		if i*(i+1)/2 < x0 {
			continue
		}

		for j := y0; j <= -y0; j++ {
			px, py := i, j
			vx, vy := i, j

			for px <= x1 && py >= y0 {
				if px >= x0 && py <= y1 {
					result++
					break
				}

				// Assume x0 and x1 are always strictly positive
				if vx != 0 {
					vx--
				}

				// Assume y0 and y1 are always strictly negative
				vy--

				px, py = px+vx, py+vy
			}
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
