package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type Segment int

const (
	A Segment = 0
	B Segment = 1
	C Segment = 2
	D Segment = 3
	E Segment = 4
	F Segment = 5
	G Segment = 6
)

type SegmentSet struct {
	val byte
}

type Translator struct {
	trans [7]Segment
}

func (t *Translator) translater(s SegmentSet) SegmentSet {
	var result SegmentSet
	for i := 0; i < 7; i++ {
		if s.get(Segment(i)) {
			result.set(t.trans[i])
		}
	}
	return result
}


func (sSet SegmentSet) String() string {
	return fmt.Sprintf("[A: %v, B: %v, C: %v, D: %v, E: %v, F: %v, G: %v]", sSet.get(A), sSet.get(B), sSet.get(C), sSet.get(D), sSet.get(E), sSet.get(F), sSet.get(G))
}

func (sSet *SegmentSet) set(s Segment) *SegmentSet {
	sSet.val |= 1 << s
	return sSet
}

func (sSet *SegmentSet) get(s Segment) bool {
	return int((sSet.val & (1 << s)) >> s) == 1
}

func (sSet *SegmentSet) getSegments() []Segment {
	var result []Segment
	for i := 0; i < 7; i++ {
		if sSet.get(Segment(i)) {
			result = append(result, Segment(i))
		}
	}
	return result
}

func (sSet *SegmentSet) intersectWith(other SegmentSet) SegmentSet {
	return SegmentSet{
		val: sSet.val & other.val,
	}
}

func (sSet *SegmentSet) minus(other SegmentSet) SegmentSet {
	return SegmentSet{val: sSet.val & (sSet.val ^ other.val)}
}

func (sSet *SegmentSet) asDisplayed() int {
	switch sSet.val {
	case byte(0b01110111):
		return 0
	case byte(0b00100100):
		return 1
	case byte(0b01011101):
		return 2
	case byte(0b01101101):
		return 3
	case byte(0b00101110):
		return 4
	case byte(0b01101011):
		return 5
	case byte(0b01111011):
		return 6
	case byte(0b00100101):
		return 7
	case byte(0b01111111):
		return 8
	case byte(0b01101111):
		return 9
	}
	return -1
}

func runeToSegment(r rune) Segment {
	switch r {
	case rune('a'):
		return A
	case rune('b'):
		return B
	case rune('c'):
		return C
	case rune('d'):
		return D
	case rune('e'):
		return E
	case rune('f'):
		return F
	case rune('g'):
		return G
	}
	fmt.Printf("Cannot read %v => return -1\n", r)
	return -1
}

type Display struct {
	input2 SegmentSet
	input3 SegmentSet
	input4 SegmentSet
	input5 []SegmentSet
	input6 []SegmentSet
	input7 SegmentSet
	outputs []SegmentSet
}

type Puzzle struct {
	displays []Display
}

func parseData(wholeInputStr string) Puzzle {
	var displays []Display
	for _, line := range strings.Split(wholeInputStr, "\n") {
		if len(line) > 0 {
			inputOutput := strings.Split(line, " | ")
			displays = append(displays, sequenceToSegmentSlice(inputOutput[0], inputOutput[1]))
		}
	}
	return Puzzle{displays: displays}
}

func sequenceToSegmentSlice(listOfInputSignals string, listOfOutputSignals string) Display {
	var display Display
	for _, inputStr := range strings.Split(listOfInputSignals, " ") {
		var input SegmentSet
		for _, r := range inputStr {
			input.set(runeToSegment(r))
		}
		switch len(inputStr) {
		case 2:
			display.input2 = input
		case 3:
			display.input3 = input
		case 4:
			display.input4 = input
		case 5:
			display.input5 = append(display.input5, input)
		case 6:
			display.input6 = append(display.input6, input)
		case 7:
			display.input7 = input
		}
	}

	for _, outputStr := range strings.Split(listOfOutputSignals, " ") {
		var output SegmentSet
		for _, r := range outputStr {
			output.set(runeToSegment(r))
		}
		display.outputs = append(display.outputs, output)
	}
	return display
}

func solveOneDisplay(d *Display) int {
	var translator Translator

	// a with the 7 and the 1
	onlySegA := d.input3.minus(d.input2)
	translator.trans[onlySegA.getSegments()[0]] = 0

	l5Common := d.input5[0].intersectWith(d.input5[1])
	l5Common = l5Common.intersectWith(d.input5[2])

	return 0
}

func puzzle(puzzle Puzzle) int {
	var count int
	for _, val := range puzzle.displays {
		count += solveOneDisplay(&val)
	}
	return count
}

func run(s string) interface{} {
	// Your code goes here
	data := parseData(s)
	result := puzzle(data)

	/*
	s1 := SegmentSet{}
	s1.set(A)
	s1.set(D)
	fmt.Printf("%v\n", s1)
	s2 := SegmentSet{}
	s2.set(D)
	s2.set(E)
	fmt.Printf("%v\n", s1.minus(s2))

	s0 := SegmentSet{}
	s0.set(A).set(B).set(C).set(E).set(F).set(G)
	fmt.Printf("0: %d\n", s0.asDisplayed())
	*/
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
