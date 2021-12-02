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

	pos, depth, aim := 0, 0, 0
	for scanner.Scan() {
		line := scanner.Bytes()
		switch line[0] {
		case 'f':
			x := int(line[8]-'0')
			pos += x
			depth += aim*x
		case 'u':
			aim -= int(line[3]-'0')
		case 'd':
			aim += int(line[5]-'0')
		}
	}

	return depth*pos
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
