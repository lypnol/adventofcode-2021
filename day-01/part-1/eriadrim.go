package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(input []byte) int {
	var previous, actual int
	var result int

	cursor := 0
	previous, cursor = bytesToInt(input, cursor)
	for i := 1; i < 2000; i++ {
		actual, cursor = bytesToInt(input, cursor)
		if actual > previous {
			result++
		}
		previous = actual
	}

	return result
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	input, _ := ioutil.ReadAll(os.Stdin)

	// Start resolution
	start := time.Now()
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}

func bytesToInt(s []byte, cursor int) (int, int) {
	res := 0
	for cursor < len(s) && s[cursor] != '\n' {
		res = res*10 + int(s[cursor] - '0')
		cursor++
	}
	cursor++
	return res, cursor
}
