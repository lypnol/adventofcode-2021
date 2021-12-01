package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)


func parseData(input string) []int {

	var data []int

	for _, line := range strings.Split(input, "\n") {
		parsed, _ := strconv.Atoi(line)
		data = append(data, parsed)
	}

	return data
}

func puzzle(input []int) int {
	var count int = 0
	for i := 3; i < len(input); i++ {
		sum_prev := input[i-3] + input[i-2] + input[i-1]
		sum_cur := 	input[i-2] + input[i-1] + input[i]

		if sum_cur > sum_prev {
			count++
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

	argsWithProg := os.Args
	var input []byte
	var err error
	if len(argsWithProg) > 1 {
		input,err = ioutil.ReadFile(argsWithProg[1])
		if err != nil {
			panic(err)
		}
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
	fmt.Printf("_duration:%f\n", time.Now().Sub(start).Seconds()*1000)
	fmt.Println(result)
}
