package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

// DigitSet is array containing the status of each segments
// a is at index 1, b is at index 2, c is at index 3, etc.
// true means it is turned on, false means it is turned off
type DigitSet [7]bool

// NewDigitSetFromString creates a new set from a string
func NewDigitSetFromString(digitstr string) DigitSet {
	digitset := DigitSet{}
	for _, l := range digitstr {
		idx := int(l - 'a')
		digitset[idx] = true
	}
	return digitset
}

// NewDigitSetFromXor creates a new set as the xor of two sets
func NewDigitSetFromXor(ds1, ds2 DigitSet) DigitSet {
	digitset := DigitSet{}
	for idx := 0; idx < 7; idx++ {
		if ds1[idx] != ds2[idx] {
			digitset[idx] = true
		}
	}
	return digitset
}

// Includes returns true if and only if all elements of subds exist in ds
func (ds DigitSet) Includes(subds DigitSet) bool {
	for idx := range subds {
		if subds[idx] && !ds[idx] {
			return false
		}
	}
	return true
}

// Len returns the size of the set
func (ds DigitSet) Len() int {
	length := 0
	for _, v := range ds {
		if v {
			length++
		}
	}
	return length
}

func run(s string) interface{} {
	// Your code goes here
	result := 0

	for _, line := range strings.Split(s, "\n") {
		digitsettoactualdigit := make(map[DigitSet]int, 10)
		actualdigittodigitset := make(map[int]DigitSet, 10)

		digitsets := make([]DigitSet, 6)

		split := strings.Split(line, " | ")
		signal := strings.Split(split[0], " ")
		output := strings.Split(split[1], " ")

		for _, digitstr := range signal {
			digitset := NewDigitSetFromString(digitstr)

			switch digitset.Len() {
			case 2:
				digitsettoactualdigit[digitset] = 1
				actualdigittodigitset[1] = digitset
			case 3:
				digitsettoactualdigit[digitset] = 7
				actualdigittodigitset[7] = digitset
			case 4:
				digitsettoactualdigit[digitset] = 4
				actualdigittodigitset[4] = digitset
			case 7:
				digitsettoactualdigit[digitset] = 8
				actualdigittodigitset[8] = digitset
			default:
				digitsets = append(digitsets, digitset)
			}
		}

		// Apply some magic to identify all signal patterns
		for _, digitset := range digitsets {
			switch digitset.Len() {
			case 5:
				if digitset.Includes(actualdigittodigitset[1]) {
					digitsettoactualdigit[digitset] = 3
					actualdigittodigitset[3] = digitset
				} else if digitset.Includes(NewDigitSetFromXor(actualdigittodigitset[4], actualdigittodigitset[7])) {
					digitsettoactualdigit[digitset] = 5
					actualdigittodigitset[5] = digitset
				} else {
					digitsettoactualdigit[digitset] = 2
					actualdigittodigitset[2] = digitset
				}
			case 6:
				if digitset.Includes(actualdigittodigitset[4]) {
					digitsettoactualdigit[digitset] = 9
					actualdigittodigitset[9] = digitset
				} else if !digitset.Includes(actualdigittodigitset[7]) {
					digitsettoactualdigit[digitset] = 6
					actualdigittodigitset[6] = digitset
				} else {
					digitsettoactualdigit[digitset] = 0
					actualdigittodigitset[0] = digitset
				}
			}
		}

		value := 0
		for _, digitstr := range output {
			digitset := NewDigitSetFromString(digitstr)

			value *= 10
			value += digitsettoactualdigit[digitset]
		}
		result += value
	}

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
