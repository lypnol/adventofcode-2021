package main

import (
	"encoding/hex"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"time"
)

// evaluatePacket parses the packet starting at position p. The result is either
// the literal value, or the result of the operation after evaluating all
// sub-packets. It also returns the position of the next packet.
func evaluatePacket(b []byte, p int) (result, next int) {
	// Skip packet version and read type ID
	typeID, p := readNBitsAtPosition(b, p+3, 3)
	switch typeID {
	case 0:
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
				subresult, p = evaluatePacket(b, p)
				result += subresult
			}
		case 1:
			// Find the number of sub-packets and read them recursively
			var numberOfSubPackets int
			numberOfSubPackets, p = readNBitsAtPosition(b, p, 11)
			for i := 0; i < numberOfSubPackets; i++ {
				var subresult int
				subresult, p = evaluatePacket(b, p)
				result += subresult
			}
		}
	case 1:
		result = 1

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
				subresult, p = evaluatePacket(b, p)
				result *= subresult
			}
		case 1:
			// Find the number of sub-packets and read them recursively
			var numberOfSubPackets int
			numberOfSubPackets, p = readNBitsAtPosition(b, p, 11)
			for i := 0; i < numberOfSubPackets; i++ {
				var subresult int
				subresult, p = evaluatePacket(b, p)
				result *= subresult
			}
		}
	case 2:
		result = math.MaxInt

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
				subresult, p = evaluatePacket(b, p)
				if subresult < result {
					result = subresult
				}
			}
		case 1:
			// Find the number of sub-packets and read them recursively
			var numberOfSubPackets int
			numberOfSubPackets, p = readNBitsAtPosition(b, p, 11)
			for i := 0; i < numberOfSubPackets; i++ {
				var subresult int
				subresult, p = evaluatePacket(b, p)
				if subresult < result {
					result = subresult
				}
			}
		}
	case 3:
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
				subresult, p = evaluatePacket(b, p)
				if subresult > result {
					result = subresult
				}
			}
		case 1:
			// Find the number of sub-packets and read them recursively
			var numberOfSubPackets int
			numberOfSubPackets, p = readNBitsAtPosition(b, p, 11)
			for i := 0; i < numberOfSubPackets; i++ {
				var subresult int
				subresult, p = evaluatePacket(b, p)
				if subresult > result {
					result = subresult
				}
			}
		}
	case 4:
		// Build literal value by chunk of four bits
		var flag int
		for flag, p = readNBitsAtPosition(b, p, 1); flag == 1; flag, p = readNBitsAtPosition(b, p, 1) {
			var subresult int
			subresult, p = readNBitsAtPosition(b, p, 4)
			result <<= 4
			result += subresult
		}
		var subresult int
		subresult, p = readNBitsAtPosition(b, p, 4)
		result <<= 4
		result += subresult
	case 5:
		// Skip length bits as we know there are exactly two sub-packets
		var lengthTypeID int
		lengthTypeID, p = readNBitsAtPosition(b, p, 1)
		switch lengthTypeID {
		case 0:
			p += 15
		case 1:
			p += 11
		}

		// Evaluate sub-packets recursively
		var first, second int
		first, p = evaluatePacket(b, p)
		second, p = evaluatePacket(b, p)

		if first > second {
			result = 1
		}
	case 6:
		// Skip length bits as we know there are exactly two sub-packets
		var lengthTypeID int
		lengthTypeID, p = readNBitsAtPosition(b, p, 1)
		switch lengthTypeID {
		case 0:
			p += 15
		case 1:
			p += 11
		}

		// Evaluate sub-packets recursively
		var first, second int
		first, p = evaluatePacket(b, p)
		second, p = evaluatePacket(b, p)

		if first < second {
			result = 1
		}
	case 7:
		// Skip length bits as we know there are exactly two sub-packets
		var lengthTypeID int
		lengthTypeID, p = readNBitsAtPosition(b, p, 1)
		switch lengthTypeID {
		case 0:
			p += 15
		case 1:
			p += 11
		}

		// Evaluate sub-packets recursively
		var first, second int
		first, p = evaluatePacket(b, p)
		second, p = evaluatePacket(b, p)

		if first == second {
			result = 1
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
	result, _ := evaluatePacket(b, 0)
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
