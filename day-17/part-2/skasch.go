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

func build_x_targets(mx int) []int {
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

func find_vy(y1, y2 int) int {
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
		return vy1
	} else {
		return vy2
	}
}

func reach_range_vx(ax1, ax2, vx int, x_targets []int) (int, int) {
	x_final := vx * (vx + 1) / 2
	if x_final < ax1 || vx > ax2 {
		return -1, -1
	}
	min_t := vx + 1 - sort.Search(
		len(x_targets),
		func(i int) bool { return x_targets[i] > x_final-ax1 },
	)
	if x_final <= ax2 {
		return min_t, -1
	}
	max_t := vx - sort.Search(
		len(x_targets),
		func(i int) bool { return x_targets[i] >= x_final-ax2 },
	)
	if max_t < min_t {
		return -1, -1
	}
	return min_t, max_t
}

func floordiv(num, den int) int {
	rem := num % den
	if rem >= 0 {
		return num / den
	} else {
		return num/den - 1
	}
}

func reach_range_y_in(y1, y2, steps int) (int, int) {
	min_vy := floordiv(y1+steps*(steps+1)/2-1, steps)
	max_vy := floordiv(y2+steps*(steps-1)/2, steps)
	return min_vy, max_vy
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
	if x1*x2 < 0 {
		panic("Failed to handle")
	}
	if x2 <= 0 {
		x1, x2 = -x2, -x1
	}
	x_targets := build_x_targets(x2)
	res := 0
	min_vx := find_vx(x1, x2, x_targets)
	for vx := min_vx; vx <= x2; vx++ {
		min_steps, max_steps := reach_range_vx(
			x1, x2, vx, x_targets,
		)
		if min_steps == -1 {
			continue
		}
		if max_steps == -1 {
			max_vy := find_vy(y1, y2)
			max_steps = max_vy*2 + 2
		}
		vys := make(map[int]interface{})
		for steps := min_steps; steps <= max_steps; steps++ {
			min_vy, max_vy := reach_range_y_in(y1, y2, steps)
			for nvy := min_vy; nvy <= max_vy; nvy++ {
				if _, ok := vys[nvy]; !ok {
					vys[nvy] = struct{}{}
					res += 1
				}
			}
		}
	}
	return res
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
