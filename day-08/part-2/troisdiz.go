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

func (t *Translator) translate(s SegmentSet) SegmentSet {
	var result SegmentSet
	for i := 0; i < 7; i++ {
		if s.isSet(Segment(i)) {
			result.set(t.trans[i])
		}
	}
	return result
}

func (t *Translator) setTranslation(from Segment, to Segment) {
	t.trans[from] = to
}

func (sSet SegmentSet) String() string {
	//return fmt.Sprintf("[A: %v, B: %v, C: %v, D: %v, E: %v, F: %v, G: %v]", sSet.isSet(A), sSet.isSet(B), sSet.isSet(C), sSet.isSet(D), sSet.isSet(E), sSet.isSet(F), sSet.isSet(G))
	return fmt.Sprintf("[%d%d%d%d%d%d%d]", sSet.get(A), sSet.get(B), sSet.get(C), sSet.get(D), sSet.get(E), sSet.get(F), sSet.get(G))
}

func (sSet *SegmentSet) set(s Segment) *SegmentSet {
	sSet.val |= 1 << s
	return sSet
}

func (sSet *SegmentSet) isSet(s Segment) bool {
	return int((sSet.val & (1 << s)) >> s) == 1
}

func (sSet *SegmentSet) get(s Segment) int {
	return int((sSet.val & (1 << s)) >> s)
}

func (sSet *SegmentSet) getSegments() []Segment {
	var result []Segment
	for i := 0; i < 7; i++ {
		if sSet.isSet(Segment(i)) {
			result = append(result, Segment(i))
		}
	}
	return result
}

func (sSet *SegmentSet) getSingle() Segment {
	segments := sSet.getSegments()
	if len(segments) == 1 {
		return segments[0]
	} else {
		fmt.Printf("Cannot return single element of %v\n", *sSet)
		return -1
	}
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

func displaySegmentSet(label string, ss SegmentSet) {
	/*
	fmt.Printf("%7s = %v", label, ss)
	if len(ss.getSegments()) == 1{
		fmt.Printf(" -> %d", ss.getSingle())
	}
	fmt.Println()
	 */
}

func solveOneDisplay(d *Display) int {
	var translator Translator

	cfSegS := d.input2
	displaySegmentSet("cf", cfSegS)
	acfSegS := d.input3
	bcdfSegS := d.input4

	// a with the 7 and the 1
	aSegS := acfSegS.minus(cfSegS)
	translator.setTranslation(aSegS.getSingle(), A)

	// a, d g common in 2, 4, 5
	adgSegS := d.input5[0].intersectWith(d.input5[1])
	adgSegS = adgSegS.intersectWith(d.input5[2])

	dgSegS := adgSegS.minus(aSegS)
	displaySegmentSet("adg", adgSegS)
	displaySegmentSet("a", aSegS)
	displaySegmentSet("dg", dgSegS)
	gSegS := dgSegS.minus(bcdfSegS)
	displaySegmentSet("g", gSegS)
	translator.setTranslation(gSegS.getSingle(), G)

	dSegS := dgSegS.minus(gSegS)
	displaySegmentSet("d", dSegS)
	translator.setTranslation(dSegS.getSingle(), D)

	// isSet the b from the 4
	bdSegS := bcdfSegS.minus(cfSegS)
	bSegS := bdSegS.minus(dSegS)
	displaySegmentSet("bcdf", bcdfSegS)
	displaySegmentSet("bd", bdSegS)
	displaySegmentSet("b", bSegS)
	translator.setTranslation(bSegS.getSingle(), B)

	// among 2, 3, 5: only 5 has b => deduce f
	var nb5SegS SegmentSet
	if d.input5[0].isSet(bSegS.getSingle()) {
		nb5SegS = d.input5[0]
	} else if d.input5[1].isSet(bSegS.getSingle()) {
		nb5SegS = d.input5[1]
	} else if d.input5[2].isSet(bSegS.getSingle()) {
		nb5SegS = d.input5[2]
	} else {
		fmt.Printf("nb5 not found in :\n  - %v\n  - %v\n  - %v\n", d.input5[0], d.input5[1], d.input5[2])
	}
	displaySegmentSet("5[0]", d.input5[0])
	displaySegmentSet("5[1]", d.input5[1])
	displaySegmentSet("5[2]", d.input5[2])
	displaySegmentSet("nb5", nb5SegS)
	bfSegS := nb5SegS.minus(adgSegS)
	displaySegmentSet("bf", bfSegS)
	displaySegmentSet("b", bSegS)
	fSegS := bfSegS.minus(bSegS)
	translator.setTranslation(fSegS.getSingle(), F)

	// deduce c from 1
	cSegS := cfSegS.minus(fSegS)
	translator.setTranslation(cSegS.getSingle(), C)

	aegSegS := d.input7.minus(bcdfSegS)
	eSegS := aegSegS.minus(adgSegS)
	translator.setTranslation(eSegS.getSingle(), E)
	digit1 := translator.translate(d.outputs[0])
	digit2 := translator.translate(d.outputs[1])
	digit3 := translator.translate(d.outputs[2])
	digit4 := translator.translate(d.outputs[3])
	return 1000 * digit1.asDisplayed() + 100 * digit2.asDisplayed() + 10 * digit3.asDisplayed() + digit4.asDisplayed()
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
