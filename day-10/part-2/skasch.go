package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"sync"
	"time"
)

const WG_SIZE = 10

var POINTS = map[byte]int{')': 1, ']': 2, '}': 3, '>': 4}
var CLOSING = map[byte]byte{'(': ')', '[': ']', '{': '}', '<': '>'}

type Bounds struct {
	left, right int
}

func parse(s string, c chan<- Bounds) {
	left := 0
	for right := 0; right < len(s); right++ {
		if s[right] == '\n' {
			c <- Bounds{left, right}
			left = right + 1
		}
	}
	c <- Bounds{left, len(s)}
	close(c)
}

func process(s string, c <-chan Bounds, res chan<- int) {
	stack := make([]byte, 30)
	for bounds := range c {
		idx := 0
	loop:
		for cursor := bounds.left; cursor < bounds.right; cursor++ {
			b := s[cursor]
			switch b {
			case '(', '[', '{', '<':
				stack[idx] = b
				idx++
			default:
				idx--
				l := stack[idx]
				exp_r := CLOSING[l]
				if b != exp_r {
					idx = 0
					break loop
				}
			}
		}
		if idx == 0 {
			continue
		}
		result := 0
		for idx > 0 {
			idx--
			result = 5*result + POINTS[CLOSING[stack[idx]]]
		}
		res <- result
	}
}

func run(s string) int {
	// Your code goes here
	// fmt.Printf("%v", parse(s))
	c := make(chan Bounds)
	go parse(s, c)

	var wg sync.WaitGroup

	res_chan := make(chan int)

	for i := 0; i < WG_SIZE; i++ {
		wg.Add(1)

		go func() {
			defer wg.Done()
			process(s, c, res_chan)
		}()
	}

	go func() {
		wg.Wait()
		close(res_chan)
	}()

	res := make([]int, 0)
	for v := range res_chan {
		res = append(res, v)
	}
	sort.Ints(res)

	return res[len(res)/2]
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
