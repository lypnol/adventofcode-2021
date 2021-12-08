package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"sort"
	"strings"
	"time"
)

type DigitSet map[rune]struct{}

// NewDigitSet creates a new set from a string
func NewDigitSet(digitstr string) DigitSet {
	digitset := make(DigitSet, 7)
	for _, l := range digitstr {
		digitset.Add(l)
	}
	return digitset
}

// Add adds a element to the set and returns it
func (ds DigitSet) Add(l rune) DigitSet {
	ds[l] = struct{}{}
	return ds
}

// Len returns the size of the set
func (ds DigitSet) Len() int {
	return len(ds)
}

// Includes returns true if and only if all elements of dss exist in ds
func (ds DigitSet) Includes(dss DigitSet) bool {
	for k := range dss {
		if _, ok := ds[k]; !ok {
			return false
		}
	}
	return true
}

// String returns a string representation of the set
// This is useful to get comparison operators on sets and use them as map keys
// See https://go.dev/ref/spec#Comparison_operators
// This may or may not be deterministic
// See https://go-review.googlesource.com/c/go/+/142737
func (ds DigitSet) String() string {
	keys := make([]string, ds.Len())
	for k := range ds {
		keys = append(keys, string(k))
	}
	sort.Strings(keys)
	return strings.Join(keys, "")
}

func run(s string) interface{} {
	// Your code goes here
	result := 0

	for _, line := range strings.Split(s, "\n") {
		digitstrtoactualdigit := make(map[string]int, 10)
		actualdigittodigitset := make(map[int]DigitSet, 10)

		digitstrs := make(map[string]bool)

		split := strings.Split(line, " | ")
		signal := strings.Split(split[0], " ")
		output := strings.Split(split[1], " ")

		for _, digitstr := range signal {
			digitset := NewDigitSet(digitstr)

			switch digitset.Len() {
			case 2:
				digitstrtoactualdigit[digitset.String()] = 1
				actualdigittodigitset[1] = digitset
			case 3:
				digitstrtoactualdigit[digitset.String()] = 7
				actualdigittodigitset[7] = digitset
			case 4:
				digitstrtoactualdigit[digitset.String()] = 4
				actualdigittodigitset[4] = digitset
			case 7:
				digitstrtoactualdigit[digitset.String()] = 8
				actualdigittodigitset[8] = digitset
			default:
				digitstrs[digitset.String()] = false
			}
		}

		for digitstr, identified := range digitstrs {
			if identified {
				continue
			}
			digitset := NewDigitSet(digitstr)
			if digitset.Len() == 5 && digitset.Includes(actualdigittodigitset[1]) {
				digitstrtoactualdigit[digitset.String()] = 3
				actualdigittodigitset[3] = digitset
				digitstrs[digitstr] = true
			} else if digitset.Len() == 6 && !digitset.Includes(actualdigittodigitset[7]) {
				digitstrtoactualdigit[digitset.String()] = 6
				actualdigittodigitset[6] = digitset
				digitstrs[digitstr] = true
			}
		}

		for digitstr, identified := range digitstrs {
			if identified {
				continue
			}
			digitset := NewDigitSet(digitstr)
			if digitset.Len() == 6 && digitset.Includes(actualdigittodigitset[3]) {
				digitstrtoactualdigit[digitset.String()] = 9
				actualdigittodigitset[9] = digitset
				digitstrs[digitstr] = true
			} else if digitset.Len() == 6 && !digitset.Includes(actualdigittodigitset[3]) {
				digitstrtoactualdigit[digitset.String()] = 0
				actualdigittodigitset[0] = digitset
				digitstrs[digitstr] = true
			}
		}

		for digitstr, identified := range digitstrs {
			if identified {
				continue
			}
			digitset := NewDigitSet(digitstr)
			if digitset.Len() == 5 && actualdigittodigitset[6].Includes(digitset) {
				digitstrtoactualdigit[digitset.String()] = 5
				actualdigittodigitset[5] = digitset
				digitstrs[digitstr] = true
			} else if digitset.Len() == 5 && !actualdigittodigitset[6].Includes(digitset) {
				digitstrtoactualdigit[digitset.String()] = 2
				actualdigittodigitset[2] = digitset
				digitstrs[digitstr] = true
			}
		}

		value := 0
		for _, digitstr := range output {
			digitset := NewDigitSet(digitstr)

			value *= 10
			value += digitstrtoactualdigit[digitset.String()]
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
