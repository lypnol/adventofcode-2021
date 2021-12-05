package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

const (
	maxSize          = 1000
	bitPerSideSquare = 4
	bitPerSquare     = bitPerSideSquare * bitPerSideSquare
	sideSize         = maxSize/ bitPerSideSquare
	bufferSize       = sideSize * sideSize

	one, fullRow, fullCol uint16 = 1, 0xf, 0x1111
)

func run(s []byte) int {
	var buffer, over [bufferSize]uint16
	cursor := 0
	var minID, maxID int
	var minSquare, maxSquare, square uint16
	var increment int
	for i := 0; i < 500; i++ {
		// parse values
		x1 := 0
		for s[cursor] != ',' {
			x1 = 10*x1 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor++
		y1 := 0
		for s[cursor] != ' ' {
			y1 = 10*y1 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor += 4
		x2 := 0
		for s[cursor] != ',' {
			x2 = 10*x2 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor++
		y2 := 0
		for cursor < len(s) && s[cursor] != '\n' {
			y2 = 10*y2 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor++

		//
		if x1 == x2 {
			min, max := y1, y2
			if y2 < y1 {
				min, max = y2, y1
			}

			xID := x1/bitPerSideSquare
			minID = sideSize * xID + min/bitPerSideSquare
			maxID = sideSize * xID + max/bitPerSideSquare

			rowShift := bitPerSideSquare*(x1%bitPerSideSquare)
			minShift := min%bitPerSideSquare
			maxShift := max%bitPerSideSquare

			minSquare = (fullRow ^ ((one << minShift) - 1)) << rowShift
			maxSquare = ((one << (maxShift+1)) - 1) << rowShift
			square = fullRow << rowShift
			increment = 1
		} else if y1 == y2 {
			min, max := x1, x2
			if x2 < x1 {
				min, max = x2, x1
			}

			yID := y1/bitPerSideSquare
			minID = sideSize * (min/bitPerSideSquare) + yID
			maxID = sideSize * (max/bitPerSideSquare) + yID

			colShift := y1%bitPerSideSquare
			minShift := min%bitPerSideSquare
			maxShift := max%bitPerSideSquare

			minSquare = 0
			for k := 0; k < minShift; k++ {
				minSquare <<= bitPerSideSquare
				minSquare |= 1
			}
			minSquare = (fullCol ^ minSquare) << colShift

			maxSquare = 0
			for k := 0; k < maxShift+1; k++ {
				maxSquare <<= bitPerSideSquare
				maxSquare |= 1
			}
			maxSquare = maxSquare << colShift
			square = fullCol << colShift
			increment = sideSize
		} else {
			continue
		}

		if minID == maxID {
			row := minSquare & maxSquare
			over[minID] |= buffer[minID] & row
			buffer[minID] |= row
			continue
		}

		for id := minID + increment; id < maxID; id+=increment {
			over[id] |= buffer[id] & square
			buffer[id] |= square
		}
		over[minID] |= buffer[minID] & minSquare
		buffer[minID] |= minSquare

		over[maxID] |= buffer[maxID] & maxSquare
		buffer[maxID] |= maxSquare
	}

	res := 0
	for i := 0; i < bufferSize; i++ {
		if over[i] != 0 {
			res += count(over[i])
		}
	}
	return res
}

func count(x uint16) int {
	res := 0
	p := uint16(1)
	i := 0
	for i < bitPerSquare {
		if p & x != 0 {
			res += 1
		}
		p <<= 1
		i++
	}
	return res
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
