package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

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

func findZeroAndOneFrequency(input [][]int, colNb int, linesToWatch []int) [2][]int {
	// fmt.Printf("Find Zeros for %d in lines %v\n", colNb, linesToWatch)
	var result [2][]int = [2][]int{  }
	for _, lineNb := range linesToWatch {
		bitValue := input[lineNb][colNb]
		result[bitValue] = append(result[bitValue], lineNb)
	}
	// fmt.Printf("Find Zeros for %d in lines %v -> %v\n", colNb, linesToWatch, result)
	return result
}

func initLines(n int) []int {
	var result []int = make([]int, n)
	for i := range result {
		result[i] = i
	}
	return result
}

func computeRate(input [][]int, lineNb int) int {
	var result int
	nbCols := len(input[lineNb])
	for colIdx := 0; colIdx < nbCols; colIdx++ {
		if input[lineNb][colIdx] == 1 {
			result += 1 << (nbCols- colIdx-1)
		}
	}
	// fmt.Printf("Cpmpute rate %v -> %d\n", input[lineNb], result)
	return result
}

func findRate(input [][]int, bit_to_take_fn func(int, int) int) int {
	nbLines := len(input)
	nbCols := len(input[0])

	var linesForRate []int = initLines(nbLines)

	for colIdx := 0; colIdx < nbCols; colIdx++ {
		bitLines := findZeroAndOneFrequency(input, colIdx, linesForRate)
		nbZeros := len(bitLines[0])
		nbOnes := len(bitLines[1])

		linesForRate = bitLines[bit_to_take_fn(nbZeros, nbOnes)]

		if len(linesForRate) == 1 {
			return computeRate(input, linesForRate[0])
		}
	}
	return 0
}

func puzzle(input [][]int) int {

	oxygenRate := findRate(input, func(nbZeros int, nbOnes int) int {
		if nbZeros > nbOnes {
			return 0
		} else {
			return 1
		}
	})
	co2Rate := findRate(input, func(nbZeros int, nbOnes int) int {
		if nbZeros > nbOnes {
			return 1
		} else {
			return 0
		}
	})
	return oxygenRate * co2Rate
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
