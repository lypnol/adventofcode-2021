package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"sync"
	"time"
)

const WG_SIZE = 10

var POINTS = map[byte]int{')': 3, ']': 57, '}': 1197, '>': 25137}
var CLOSING = map[byte]byte{'(': ')', '[': ']', '{': '}', '<': '>'}

func parse(s string, c chan<- string) {
	for _, row := range strings.Split(s, "\n") {
		c <- row
	}
	close(c)
}

func process(c <-chan string, res chan<- int) {
	stack := make([]byte, 30)
	for row := range c {
		stack = nil
		for cursor := 0; cursor < len(row); cursor++ {
			b := row[cursor]
			_, ok := CLOSING[b]
			if ok {
				stack = append(stack, b)
			} else {
				l := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				exp_r := CLOSING[l]
				if b != exp_r {
					res <- POINTS[b]
				}
			}
		}
	}
}

func run(s string) int {
	// Your code goes here
	// fmt.Printf("%v", parse(s))
	c := make(chan string)
	go parse(s, c)

	var wg sync.WaitGroup

	resc := make(chan int)

	for i := 0; i < WG_SIZE; i++ {
		wg.Add(1)

		go func() {
			defer wg.Done()
			process(c, resc)
		}()
	}

	go func() {
		wg.Wait()
		close(resc)
	}()

	res := 0
	for v := range resc {
		res += v
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
