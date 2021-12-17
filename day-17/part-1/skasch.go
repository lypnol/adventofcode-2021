package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"regexp"
	"sort"
	"strconv"
	"time"
)

var REGEX = regexp.MustCompile("target area: x=([-0-9]+)..([-0-9]+), y=([-0-9]+)..([-0-9]+)")

func build_x_targets(x1, x2 int) []int {
	var mx int
	if -x1 > x2 {
		mx = -x1
	} else {
		mx = x2
	}
	x_targets := make([]int, mx+1)
	for n := 0; n <= mx; n++ {
		x_targets[n] = n * (n + 1) / 2
	}
	return x_targets
}

func find_vx(x1, x2 int, x_targets []int) int {
	if x1 <= 0 && 0 <= x2 {
		return 0
	}
	var m int
	if x2 < 0 {
		m = -1
		x1, x2 = -x2, x1
	} else {
		m = 1
	}
	idx1 := sort.Search(len(x_targets), func(i int) bool { return x_targets[i] >= x1 })
	idx2 := sort.Search(len(x_targets), func(i int) bool { return x_targets[i] >= x2 })
	if x_targets[idx1] == x1 {
		return m * idx1
	}
	if x_targets[idx2] == x2 {
		return m * idx1
	}
	if idx1 == idx2 {
		panic("Impossible to handle")
	}
	return m * idx1
}

func find_vy(y1, y2 int) (int, bool) {
	var vy1, vy2 int
	if y1 >= 0 {
		vy1 = y1
	} else {
		vy1 = -y1 - 1
	}
	if y2 >= 0 {
		vy2 = y2
	} else {
		vy2 = -y2 - 1
	}
	if vy1 > vy2 {
		return vy1, y1 >= 0
	} else {
		return vy2, y2 >= 0
	}
}

func parse(s string) (int, int, int, int) {
	submatch := REGEX.FindStringSubmatch(s)
	x1, err := strconv.Atoi(submatch[1])
	if err != nil {
		panic(err)
	}
	x2, err := strconv.Atoi(submatch[2])
	if err != nil {
		panic(err)
	}
	y1, err := strconv.Atoi(submatch[3])
	if err != nil {
		panic(err)
	}
	y2, err := strconv.Atoi(submatch[4])
	if err != nil {
		panic(err)
	}
	return x1, x2, y1, y2
}

func run(s string) int {
	// Your code goes here
	x1, x2, y1, y2 := parse(s)
	x_targets := build_x_targets(x1, x2)
	vx := find_vx(x1, x2, x_targets)
	vy, pos := find_vy(y1, y2)
	delta := 1
	if pos {
		delta = -1
	}
	if vx > vy+delta {
		panic("Cannot handle")
	}
	return vy * (vy + 1) / 2
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
