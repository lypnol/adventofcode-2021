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

func parseData(input string) []Move {

	var data []Move

	for _, line := range strings.Split(input, "\n") {
		if len(line) > 0 {
			moveSplit := strings.Split(line, " ")
			parsedCount, _ := strconv.Atoi(moveSplit[1])
			direction := 0
			count := 0
			switch moveSplit[0] {
			case "forward":
				direction = 0
				count = parsedCount
			case "down":
				direction = 1
				count = parsedCount
			case "up":
				direction = 1
				count = -parsedCount
			}
			move := Move{
				direction: direction,
				count:     count,
			}
			data = append(data, move)
		}
	}

	return data
}

func puzzle(input []Move) int {
	aim := 0
	hp := 0
	depth := 0
	for _, move := range input {
		if move.direction == 1 {
			aim += move.count
		} else if move.direction == 0 {
			hp += move.count
			depth += aim * move.count
		}
	}
	return hp * depth
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
