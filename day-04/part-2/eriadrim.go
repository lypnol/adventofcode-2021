package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(s []byte) int {
	cursor := 0
	pos := [100]byte{}
	var current byte
	for i := byte(0); i < 99; i++ {
		current = s[cursor] & 0xf
		cursor++
		if s[cursor] != ',' {
			current = current*10 + (s[cursor] & 0xf)
			cursor++
		}
		pos[current] = i
		cursor++
	}
	current = s[cursor] & 0xf
	cursor++
	if s[cursor] != '\n' {
		current = current*10 + (s[cursor] & 0xf)
		cursor ++
	}
	pos[current] = 99
	cursor += 2

	var bufferGrid [25]byte
	var bufferScore, bufferPos byte
	var col, row [5]byte
	var minPos byte = 0
	var last byte
	score := 0
	for i := 0; i < 100; i++ {
		for j := 0; j < 5; j++ {
			col[j] = 0
			row[j] = 0
		}

		// parse grid and winning ?
		for j := 0; j < 25; j++ {
			current = s[cursor+1] & 0xf
			if s[cursor] != ' '{
				current += 10*(s[cursor] & 0xf)
			}
			cursor += 3
			bufferGrid[j] = current

			if col[j%5] < pos[current] {
				col[j%5] = pos[current]
			}
			if row[j/5] < pos[current] {
				row[j/5] = pos[current]
			}
		}
		cursor++

		// winning ?
		bufferPos = 100
		for j := 0; j < 5; j++ {
			if col[j] < bufferPos {
				bufferPos = col[j]
			}
			if row[j] < bufferPos {
				bufferPos = row[j]
			}
		}
		if bufferPos <= minPos {
			continue
		}
		minPos = bufferPos

		// score ?
		score = 0
		for j := 0; j < 25; j++ {
			bufferScore = bufferGrid[j]
			if pos[bufferScore] > minPos {
				score += int(bufferScore)
				continue
			}
			if pos[bufferScore] == minPos {
				last = bufferScore
			}
		}
	}

	return score * int(last)
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
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
