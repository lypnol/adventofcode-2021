package main

import (
	"bufio"
	"fmt"
	"io"
	"os"
	"time"
)

func run(r io.Reader) int {
	scanner := bufio.NewScanner(r)
	var previous, actual int
	var result int

	scanner.Scan()
	previous = bytesToInt(scanner.Bytes())
	for scanner.Scan() {
		actual = bytesToInt(scanner.Bytes())
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

	// Start resolution
	start := time.Now()
	result := run(os.Stdin)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}

func bytesToInt(s []byte) int {
	n := 0
	for _, ch := range s {
		ch -= '0'
		n = n*10 + int(ch)
	}
	return n
}
