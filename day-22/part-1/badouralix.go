package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Cube uint

func NewCube(x, y, z int) Cube {
	return Cube(uint(uint8(x))<<16 + uint(uint8(y))<<8 + uint(uint8(z)))
}

func run(s string) int {
	// Your code goes here
	reactor := make(map[Cube]struct{}, 101*101*101)

	for _, line := range strings.Split(s, "\n") {
		ssplit := strings.Split(line, " ")
		nsplit := strings.Split(ssplit[1], ",")

		xsplit := strings.Split(nsplit[0][2:], "..")
		xmin, _ := strconv.Atoi(xsplit[0])
		if xmin < -50 {
			xmin = -50
		}
		xmax, _ := strconv.Atoi(xsplit[1])
		if xmax > 50 {
			xmax = 50
		}

		ysplit := strings.Split(nsplit[1][2:], "..")
		ymin, _ := strconv.Atoi(ysplit[0])
		if ymin < -50 {
			ymin = -50
		}
		ymax, _ := strconv.Atoi(ysplit[1])
		if ymax > 50 {
			ymax = 50
		}

		zsplit := strings.Split(nsplit[2][2:], "..")
		zmin, _ := strconv.Atoi(zsplit[0])
		if zmin < -50 {
			zmin = -50
		}
		zmax, _ := strconv.Atoi(zsplit[1])
		if zmax > 50 {
			zmax = 50
		}

		for x := xmin; x <= xmax; x++ {
			for y := ymin; y <= ymax; y++ {
				for z := zmin; z <= zmax; z++ {
					switch ssplit[0] {
					case "on":
						reactor[NewCube(x, y, z)] = struct{}{}
					case "off":
						delete(reactor, NewCube(x, y, z))
					}
				}
			}
		}

	}

	return len(reactor)
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
