package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

const CYCLE = 7
const NEW = 2
const DAYS = 80

func parse(s string) []int {
	strs := strings.Split(s, ",")
	res := make([]int, 0, len(strs))
	for _, str := range strs {
		v, err := strconv.Atoi(str)
		if err != nil {
			log.Print(err)
		}
		res = append(res, v)
	}
	return res
}

func run(s string) int {
	// Your code goes here
	vals := parse(s)
	mem := make([]int, CYCLE+NEW)
	for _, val := range vals {
		mem[val] += 1
	}
	day := DAYS
	news := make([]int, NEW)
	for day >= CYCLE {
		for i := 0; i < NEW; i++ {
			news[i] = mem[i+CYCLE]
			mem[i+CYCLE] = 0
		}
		for i := CYCLE - 1; i >= 0; i-- {
			mem[i+2] += mem[i]
		}
		for i := 0; i < NEW; i++ {
			mem[i] += news[i]
		}
		day -= CYCLE
	}
	res := 0
	for val, cnt := range mem {
		if val >= day {
			res += cnt
		} else {
			res += 2 * cnt
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
