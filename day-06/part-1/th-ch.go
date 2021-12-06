package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
	fishes := [9]int{0, 0, 0, 0, 0, 0, 0, 0, 0} // index = timer, value = nb fishes
	split := strings.Split(s, ",")
	for _, timerStr := range split {
		timer, _ := strconv.Atoi(timerStr)
		fishes[timer]++
	}

	for day := 1; day <= 80; day++ {
		nbCreatedFishes := fishes[0]                   // new fishes
		newFishes := [9]int{0, 0, 0, 0, 0, 0, 0, 0, 0} // index = timer, value = nb fishes

		for timer, nbFishes := range fishes[:8] {
			newFishes[(timer+6)%7] += nbFishes
		}

		newFishes[7] = fishes[8]
		newFishes[8] += nbCreatedFishes
		fishes = newFishes
	}

	nbFishes := 0
	for _, nbFish := range fishes {
		nbFishes += nbFish
	}

	return nbFishes
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
