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
const DAYS = 256

func parse(s string) [CYCLE + NEW]int {
	strs := strings.Split(s, ",")
	mem := [CYCLE + NEW]int{0}
	for _, str := range strs {
		v, err := strconv.Atoi(str)
		if err != nil {
			log.Print(err)
		}
		mem[v]++
	}
	return mem
}

func run(s string) int {
	// Your code goes here
	mem := parse(s)
	news := [NEW]int{0}
	for day := CYCLE; day < DAYS; day += CYCLE {
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
	}
	res := 0
	for idx := 0; idx < (DAYS % CYCLE); idx++ {
		res += 2 * mem[idx]
	}
	for idx := (DAYS % CYCLE); idx < CYCLE+NEW; idx++ {
		res += mem[idx]
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
