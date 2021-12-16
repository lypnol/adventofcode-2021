package main

import (
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

// addUpAllOfTheVersionNumbers reads the version number of the packet starting
// at position p and the version numbers of all subsequent packets. It returns
// the sum of all these version numbers, along with the position of the next
// packet.
func addUpAllOfTheVersionNumbers(b []byte, p int) (result, next int) {
	version, p := readNBitsAtPosition(b, p, 3)
	result += version

	typeID, p := readNBitsAtPosition(b, p, 3)
	switch typeID {
	case 4:
		// Skip all bits of the literal value
		var flag int
		for flag, p = readNBitsAtPosition(b, p, 1); flag == 1; flag, p = readNBitsAtPosition(b, p, 1) {
			p += 4
		}
		p += 4
	default:
		var lengthTypeID int
		lengthTypeID, p = readNBitsAtPosition(b, p, 1)

		switch lengthTypeID {
		case 0:
			// Find the total length of sub-packets and read them recursively
			var totalLength int
			totalLength, p = readNBitsAtPosition(b, p, 15)
			maxPosition := p + totalLength
			for p < maxPosition {
				var subresult int
				subresult, p = addUpAllOfTheVersionNumbers(b, p)
				result += subresult
			}
		case 1:
			// Find the number of sub-packets and read them recursively
			var numberOfSubPackets int
			numberOfSubPackets, p = readNBitsAtPosition(b, p, 11)
			for i := 0; i < numberOfSubPackets; i++ {
				var subresult int
				subresult, p = addUpAllOfTheVersionNumbers(b, p)
				result += subresult
			}
		}
	}

	// No need to move the position after the trailing 0s
	// p += 8 - p%8

	// fmt.Println(result, p)
	return result, p
}

// readNBitsAtPosition returns the int representation of n bits of b starting at
// position p, along with the new position after reading n bits.
func readNBitsAtPosition(b []byte, p int, n int) (int, int) {
	idx := p / 8
	offset := p % 8
	result := int(b[idx] & (1<<(8-offset) - 1))
	size := 1
	for 8*size-offset < n {
		result <<= 8
		result += int(b[idx+size])
		size++
	}
	result >>= (8*size - offset - n)
	// fmt.Println(b, p, n, result, p+n)
	return result, p + n
}

func run(s string) int {
	// Your code goes here
	b, _ := hex.DecodeString(s)
	// for _, c := range b {
	// 	fmt.Printf("%08b", c)
	// }
	// fmt.Println()
	result, _ := addUpAllOfTheVersionNumbers(b, 0)
	return result
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
