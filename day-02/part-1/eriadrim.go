package main

import (
"fmt"
"io/ioutil"
"os"
"time"
)

func run(b []byte) int {
	cursor := 0
	pos, depth := 0, 0
	for cursor < len(b) {
		switch b[cursor] {
		case 'f':
			pos += int(b[cursor + 8]-'0')
			cursor += 10
		case 'u':
			depth -= int(b[cursor + 3]-'0')
			cursor += 5
		case 'd':
			depth += int(b[cursor + 5]-'0')
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
