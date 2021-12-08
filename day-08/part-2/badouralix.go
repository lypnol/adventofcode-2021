package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type DigitSet struct {
	// length is the total number of segments turned on
	length int

	// segments is the status of each segments
	// a is at index 1, b is at index 2, c is at index 3, etc.
	// true means it is turned on, false means it is turned off
	segments [7]bool
}

// NewDigitSet creates a new set from a string
func NewDigitSet(digitstr string) DigitSet {
	digitset := DigitSet{}
	for _, l := range digitstr {
		digitset.Add(l)
	}
	return digitset
}

// Add adds a element to the set and returns it
func (ds *DigitSet) Add(l rune) DigitSet {
	idx := int(l - 'a')
	if !ds.segments[idx] {
		ds.length++
		ds.segments[idx] = true
	}
	return *ds
}

// Len returns the size of the set
func (ds DigitSet) Len() int {
	return ds.length
}

// Includes returns true if and only if all elements of subds exist in ds
func (ds DigitSet) Includes(subds DigitSet) bool {
	for idx := range subds.segments {
		if subds.segments[idx] && !ds.segments[idx] {
			return false
		}
	}
	return true
}

func run(s string) interface{} {
	// Your code goes here
	result := 0

	for _, line := range strings.Split(s, "\n") {
		digitsettoactualdigit := make(map[DigitSet]int, 10)
		actualdigittodigitset := make(map[int]DigitSet, 10)

		digitsets := make(map[DigitSet]struct{}, 6)

		split := strings.Split(line, " | ")
		signal := strings.Split(split[0], " ")
		output := strings.Split(split[1], " ")

		for _, digitstr := range signal {
			digitset := NewDigitSet(digitstr)

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
				digitsets[digitset] = struct{}{}
			}
		}

		// Apply some magic to identify all signal patterns
		for digitset := range digitsets {
			if digitset.Len() == 5 && digitset.Includes(actualdigittodigitset[1]) {
				digitsettoactualdigit[digitset] = 3
				actualdigittodigitset[3] = digitset
				delete(digitsets, digitset)
			} else if digitset.Len() == 6 && !digitset.Includes(actualdigittodigitset[7]) {
				digitsettoactualdigit[digitset] = 6
				actualdigittodigitset[6] = digitset
				delete(digitsets, digitset)
			} else if digitset.Len() == 6 && digitset.Includes(actualdigittodigitset[4]) {
				digitsettoactualdigit[digitset] = 9
				actualdigittodigitset[9] = digitset
				delete(digitsets, digitset)
			} else if digitset.Len() == 6 {
				digitsettoactualdigit[digitset] = 0
				actualdigittodigitset[0] = digitset
				delete(digitsets, digitset)
			}
		}

		for digitset := range digitsets {
			if actualdigittodigitset[6].Includes(digitset) {
				digitsettoactualdigit[digitset] = 5
				actualdigittodigitset[5] = digitset
			} else {
				digitsettoactualdigit[digitset] = 2
				actualdigittodigitset[2] = digitset
			}
		}

		value := 0
		for _, digitstr := range output {
			digitset := NewDigitSet(digitstr)

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
