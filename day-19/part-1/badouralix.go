package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Position struct {
	X int
	Y int
	Z int
}

func NewPositionFromCoordinates(x, y, z int) Position {
	return Position{x, y, z}
}

func NewPositionFromQuaternion(q Quaternion) Position {
	if q.W != 0 {
		panic("tried to convert non-vector quaternion to position")
	}

	return Position{int(q.X), int(q.Y), int(q.Z)}
}

func (p Position) Norm1() (norm int) {
	if p.X >= 0 {
		norm += p.X
	} else {
		norm -= p.X
	}

	if p.Y >= 0 {
		norm += p.Y
	} else {
		norm -= p.Y
	}

	if p.Z >= 0 {
		norm += p.Z
	} else {
		norm -= p.Z
	}

	return norm
}

func (p Position) Rotate(q Quaternion) Position {
	return NewPositionFromQuaternion(
		MultiplyQuaternions(
			q,
			MultiplyQuaternions(
				NewQuaternionFromPosition(p),
				q.Reciprocal(),
			),
		),
	)
}

func (p Position) Translate(t Position) Position {
	return NewPositionFromCoordinates(p.X+t.X, p.Y+t.Y, p.Z+t.Z)
}

func (p Position) String() string {
	return fmt.Sprintf("%d,%d,%d", p.X, p.Y, p.Z)
}

func SubstractPositions(p1, p2 Position) Position {
	return NewPositionFromCoordinates(p1.X-p2.X, p1.Y-p2.Y, p1.Z-p2.Z)
}

type Quaternion struct {
	W float64
	X float64
	Y float64
	Z float64
}

func NewQuaternionFromCoordinates(w, x, y, z float64) Quaternion {
	return Quaternion{w, x, y, z}
}

func NewQuaternionFromPosition(p Position) Quaternion {
	return Quaternion{0, float64(p.X), float64(p.Y), float64(p.Z)}
}

func (q Quaternion) Conjugate() Quaternion {
	return NewQuaternionFromCoordinates(q.W, -q.X, -q.Y, -q.Z)
}

func (q Quaternion) Norm2() float64 {
	return q.W*q.W + q.X*q.X + q.Y*q.Y + q.Z*q.Z
}

func (q Quaternion) Reciprocal() Quaternion {
	conj := q.Conjugate()
	norm := q.Norm2()

	if norm == 0 {
		panic("tried to get reciprocal of 0")
	}

	return NewQuaternionFromCoordinates(conj.W/norm, conj.X/norm, conj.Y/norm, conj.Z/norm)
}

func MultiplyQuaternions(q1, q2 Quaternion) Quaternion {
	w := q1.W*q2.W - q1.X*q2.X - q1.Y*q2.Y - q1.Z*q2.Z
	x := q1.W*q2.X + q1.X*q2.W + q1.Y*q2.Z - q1.Z*q2.Y
	y := q1.W*q2.Y - q1.X*q2.Z + q1.Y*q2.W + q1.Z*q2.X
	z := q1.W*q2.Z + q1.X*q2.Y - q1.Y*q2.X + q1.Z*q2.W

	return NewQuaternionFromCoordinates(w, x, y, z)
}

type Scanner struct {
	// BeaconsAbsolutePosition contains the positions of the beacons relative to scanner `0`
	BeaconsAbsolutePosition map[Position]struct{}
	// BeaconsRelativePositionWithRotation contains the positions of the beacons relative to the current scanner
	// with the rotation applied to the scanner, but without the translation applied
	BeaconsRelativePositionWithRotation []Position
	// BeaconsRelativePositionWithRotation contains the positions of the beacons relative to the current scanner
	// without the rotation applied to the scanner : the positions are essentially what is written in the input file
	BeaconsRelativePositionWithoutRotation []Position

	Identified  bool
	Orientation Quaternion
	Position    Position
}

func NewScanner() Scanner {
	return Scanner{
		BeaconsAbsolutePosition:                make(map[Position]struct{}),
		BeaconsRelativePositionWithRotation:    make([]Position, 0),
		BeaconsRelativePositionWithoutRotation: make([]Position, 0),

		Identified:  false,
		Orientation: NewQuaternionFromCoordinates(1, 0, 0, 0),
		Position:    NewPositionFromCoordinates(0, 0, 0),
	}
}

func (sc *Scanner) AddBeacon(x, y, z int) {
	beacon := NewPositionFromCoordinates(x, y, z)

	sc.BeaconsAbsolutePosition[beacon] = struct{}{}
	sc.BeaconsRelativePositionWithRotation = append(sc.BeaconsRelativePositionWithRotation, beacon)
	sc.BeaconsRelativePositionWithoutRotation = append(sc.BeaconsRelativePositionWithoutRotation, beacon)
}

func (sc *Scanner) UpdateOrientationAndPosition(q Quaternion, p Position) {
	sc.Orientation = q
	sc.Position = p

	sc.BeaconsAbsolutePosition = make(map[Position]struct{}, len(sc.BeaconsRelativePositionWithoutRotation))
	sc.BeaconsRelativePositionWithRotation = make([]Position, len(sc.BeaconsRelativePositionWithoutRotation))
	for idx, beacon := range sc.BeaconsRelativePositionWithoutRotation {
		beaconWithoutTranslation := beacon.Rotate(sc.Orientation)
		beaconWithTranslation := beaconWithoutTranslation.Translate(sc.Position)

		sc.BeaconsAbsolutePosition[beaconWithTranslation] = struct{}{}
		sc.BeaconsRelativePositionWithRotation[idx] = beaconWithoutTranslation
	}
}

func CountCommonBeacons(b1, b2 map[Position]struct{}) (count int) {
	for beacon := range b1 {
		if _, ok := b2[beacon]; ok {
			count++
		}
	}
	return count
}

func IdentifyScanners(s string) []*Scanner {
	scanners := make([]*Scanner, 0)
	for _, lines := range strings.Split(s, "\n\n") {
		scanner := NewScanner()
		for _, line := range strings.Split(lines, "\n")[1:] {
			split := strings.Split(line, ",")
			x, _ := strconv.Atoi(split[0])
			y, _ := strconv.Atoi(split[1])
			z, _ := strconv.Atoi(split[2])
			scanner.AddBeacon(x, y, z)
		}
		scanners = append(scanners, &scanner)
	}

	// Do not ask why this generates all possible rotations
	rotations := make([]Quaternion, 0, 24)
	for _, r1 := range []Quaternion{
		NewQuaternionFromCoordinates(1, 0, 0, 0),
		NewQuaternionFromCoordinates(1, 1, 0, 0),
		NewQuaternionFromCoordinates(0, 1, 0, 0),
		NewQuaternionFromCoordinates(-1, 1, 0, 0),
		NewQuaternionFromCoordinates(1, 0, 1, 0),
		NewQuaternionFromCoordinates(-1, 0, 1, 0),
	} {
		for _, r2 := range []Quaternion{
			NewQuaternionFromCoordinates(1, 0, 0, 0),
			NewQuaternionFromCoordinates(1, 0, 0, 1),
			NewQuaternionFromCoordinates(0, 0, 0, 1),
			NewQuaternionFromCoordinates(-1, 0, 0, 1),
		} {
			rotation := MultiplyQuaternions(r1, r2)
			rotations = append(rotations, rotation)
		}
	}

	identifiedScanners := make([]*Scanner, 0, len(scanners))
	identifiedScanners = append(identifiedScanners, scanners[0])
	scanners[0].Identified = true
	negativeCache := make(map[*Scanner]map[*Scanner]struct{}, len(scanners))
	for len(identifiedScanners) != len(scanners) {
	loop:
		for _, scanner := range scanners[1:] {
			if scanner.Identified {
				continue
			}

			if _, ok := negativeCache[scanner]; !ok {
				negativeCache[scanner] = make(map[*Scanner]struct{}, len(scanners))
			}

			// Loop over all identified scanners and try to find a neighbor with at least 12 beacons in common
			for _, identifiedScanner := range identifiedScanners {
				if _, ok := negativeCache[scanner][identifiedScanner]; ok {
					continue
				}

				// Try all rotations and all translations
				for _, rotation := range rotations {
					// Update scanner.BeaconsRelativePositionWithRotation to match the current rotation
					scanner.UpdateOrientationAndPosition(rotation, NewPositionFromCoordinates(0, 0, 0))

					// Bruteforce all possible translations from one scanner to the other with at least one common beacon
					for _, source := range scanner.BeaconsRelativePositionWithRotation {
						for destination := range identifiedScanner.BeaconsAbsolutePosition {
							translation := SubstractPositions(destination, source)
							scanner.UpdateOrientationAndPosition(rotation, translation)

							if CountCommonBeacons(scanner.BeaconsAbsolutePosition, identifiedScanner.BeaconsAbsolutePosition) >= 12 {
								scanner.Identified = true
								identifiedScanners = append(identifiedScanners, scanner)
								break loop
							}
						}
					}
				}

				// Remember that scanner and identifiedScanner are not neighbors
				negativeCache[scanner][identifiedScanner] = struct{}{}
			}
		}
	}

	return scanners
}

func run(s string) int {
	// Your code goes here
	scanners := IdentifyScanners(s)

	beacons := make(map[Position]struct{})
	for _, scanner := range scanners {
		for beacon := range scanner.BeaconsAbsolutePosition {
			beacons[beacon] = struct{}{}
		}
	}

	return len(beacons)
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
