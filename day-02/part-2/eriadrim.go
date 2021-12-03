package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(b []byte) int {
	cursor := 0
	pos, depth, aim := 0, 0, 0
	for cursor < len(b) {
		switch b[cursor] {
		case 'f':
			x := int(b[cursor + 8]-'0')
			cursor += 10
			pos += x
			depth += aim*x
		case 'u':
			aim -= int(b[cursor + 3]-'0')
			cursor += 5
		case 'd':
			aim += int(b[cursor + 5]-'0')
			cursor += 7
		}
	}

	return depth*pos
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	b, _ := ioutil.ReadAll(os.Stdin)

	// Start resolution
	start := time.Now()
	result := run(b)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
