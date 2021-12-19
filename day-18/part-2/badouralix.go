package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type SnailfishNumber struct {
	Value *int

	Left  *SnailfishNumber
	Right *SnailfishNumber
}

// NewSnailfishNumberFromAdd returns a SnailfishNumber representing sn1 + sn2
// without side-effect on sn1 nor on sn2
func NewSnailfishNumberFromAdd(sn1, sn2 SnailfishNumber) SnailfishNumber {
	sn := SnailfishNumber{Left: sn1.Copy(), Right: sn2.Copy()}
	sn.Reduce()
	return sn
}

// NewSnailfishNumberFromInt returns a SnailfishNumber with the given value as regular number
func NewSnailfishNumberFromInt(value int) *SnailfishNumber {
	return &SnailfishNumber{Value: &value}
}

// NewSnailfishNumberFromLine returns a SnailfishNumber represented by the bracket expression line
// and the index of the last parsed char in line
func NewSnailfishNumberFromLine(line string, p int) (SnailfishNumber, int) {
	var left, right SnailfishNumber

	// Start parsing at position p
	for i := p; i < len(line); i++ {
		char := line[i]

		switch char {
		case '[':
			left, i = NewSnailfishNumberFromLine(line, i+1)
		case ']':
			return SnailfishNumber{Left: &left, Right: &right}, i
		case ',':
			right, i = NewSnailfishNumberFromLine(line, i+1)
		default:
			return *NewSnailfishNumberFromInt(int(char - '0')), i
		}
	}

	// If line is a well-formed bracket expression, this point is unreachable
	return SnailfishNumber{}, len(line) - 1
}

// AddValueLeft adds v to the node on the very left of sn
func (sn *SnailfishNumber) AddValueLeft(v int) bool {
	if sn == nil {
		return false
	}

	if sn.Value == nil {
		return sn.Left.AddValueLeft(v)
	}

	value := *sn.Value + v
	sn.Value = &value
	return true
}

// AddValueRight adds v to the node on the very right of sn
func (sn *SnailfishNumber) AddValueRight(v int) bool {
	if sn == nil {
		return false
	}

	if sn.Value == nil {
		return sn.Right.AddValueRight(v)
	}

	value := *sn.Value + v
	sn.Value = &value
	return true
}

// Copy returns a complete copy of sn without any shared memory between the two structs
func (sn *SnailfishNumber) Copy() *SnailfishNumber {
	if sn == nil {
		return nil
	}

	if sn.Value == nil {
		return &SnailfishNumber{Left: sn.Left.Copy(), Right: sn.Right.Copy()}
	}

	value := sn.Value
	return &SnailfishNumber{Value: value}
}

// Magnitude returns the magnitude of sn
func (sn SnailfishNumber) Magnitude() int {
	if sn.Value == nil {
		return 3*sn.Left.Magnitude() + 2*sn.Right.Magnitude()
	}

	return *sn.Value
}

// RecExplode recursively explodes sn, and returns true if an explosion happened downstream
// It also returns a value to add to the first regular number of the left/right upstream if necessary
func (sn *SnailfishNumber) RecExplode(depth int) (bool, *int, *int) {
	if sn == nil {
		return false, nil, nil
	}

	if depth > 4 && sn.Value == nil && sn.Left.Value != nil && sn.Right.Value != nil {
		value := 0
		leftValue := *sn.Left.Value
		rightValue := *sn.Right.Value

		sn.Value = &value
		sn.Left = nil
		sn.Right = nil

		return true, &leftValue, &rightValue
	}

	if exploded, leftValue, rightValue := sn.Left.RecExplode(depth + 1); exploded {
		// Try to add the right value to the first regular number of the right
		if rightValue != nil && sn.Right.AddValueLeft(*rightValue) {
			return true, leftValue, nil
		}
		return true, leftValue, rightValue
	}

	if exploded, leftValue, rightValue := sn.Right.RecExplode(depth + 1); exploded {
		// Try to add the left value to the first regular number of the left
		if leftValue != nil && sn.Left.AddValueRight(*leftValue) {
			return true, nil, rightValue
		}
		return true, leftValue, rightValue
	}

	return false, nil, nil
}

// RecSplit recursively split sn and stops as soon as one snailfish number was split
// It returns a boolean whether a split occurred somewhere or not at all
func (sn *SnailfishNumber) RecSplit() bool {
	if sn.Value == nil {
		if sn.Left.RecSplit() {
			return true
		} else if sn.Right.RecSplit() {
			return true
		} else {
			return false
		}
	}

	if *sn.Value < 10 {
		return false
	}

	sn.Left = NewSnailfishNumberFromInt(*sn.Value / 2)
	sn.Right = NewSnailfishNumberFromInt((*sn.Value + 1) / 2)
	sn.Value = nil

	return true
}

// Reduce reduces sn as much as possible
func (sn *SnailfishNumber) Reduce() {
	for {
		// Try to explode sn and if something happened, reduce again
		if exploded, _, _ := sn.RecExplode(1); exploded {
			continue
		}

		// Try to split sn and if something happened, reduce again
		if sn.RecSplit() {
			continue
		}

		// If nothing happened during this loop, sn is fully reduced
		return
	}
}

// String implements fmt.Stringer interface for SnailfishNumber
func (sn SnailfishNumber) String() string {
	if sn.Value == nil {
		return fmt.Sprintf("[%s,%s]", sn.Left, sn.Right)
	}

	return fmt.Sprint(*sn.Value)
}

func run(s string) int {
	// Your code goes here
	lines := strings.Split(s, "\n")
	sns := make([]SnailfishNumber, 0, len(lines))
	result := 0

	for _, line := range lines {
		sn, _ := NewSnailfishNumberFromLine(line, 0)
		sns = append(sns, sn)
	}

	for i, sn1 := range sns {
		for _, sn2 := range sns[i+1:] {
			if magnitude := NewSnailfishNumberFromAdd(sn1, sn2).Magnitude(); magnitude > result {
				result = magnitude
			}

			if magnitude := NewSnailfishNumberFromAdd(sn2, sn1).Magnitude(); magnitude > result {
				result = magnitude
			}
		}
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
