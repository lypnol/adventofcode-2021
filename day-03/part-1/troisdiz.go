package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Move struct {
	direction int
	count int
}

func parseData(input string) [][]int {

	var data [][]int

	for _, line := range strings.Split(input, "\n") {
		if len(line) > 0 {
			var bitLine []int
			for _, bit := range strings.Split(line, "") {
				parsedBit, _ := strconv.Atoi(bit)
				bitLine = append(bitLine, parsedBit)
			}
			data = append(data, bitLine)
		}
	}
	return data
}

func puzzle(input [][]int) int {

	nbLines := len(input)
	nbCols := len(input[0])

	gammaRate := 0
	epsilonRate := 0
	for colIdx := 0; colIdx < nbCols; colIdx++ {
		var oneCount int
		for lineIdx := 0; lineIdx < nbLines; lineIdx++ {
			if input[lineIdx][colIdx] == 1 {
				oneCount++
			}
		}
		// fmt.Printf("Col[%d] -> %d ones\n", colIdx, oneCount)
		if oneCount > (nbLines/2) {
			// fmt.Printf("Col[%d] -> gamma=1, epsilon=0\n", colIdx)
			gammaRate += 1 << (nbCols- colIdx-1)
		} else {
			// fmt.Printf("Col[%d] -> gamma=0, epsilon=1\n", colIdx)
			epsilonRate += 1 << (nbCols- colIdx-1)
		}
	}
	// fmt.Printf("gamma = %d, epsilon = %d\n", gammaRate, epsilonRate)
	return gammaRate * epsilonRate
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
