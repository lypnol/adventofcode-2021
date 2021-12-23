package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const NumberOfBeaconsSharedBetweenNeighbors = 12

type Position uint64

func NewPositionFromCoordinates(x, y, z int16) Position {
	return Position(uint64(uint16(x))<<32 + uint64(uint16(y))<<16 + uint64(uint16(z)))
}

func NewPositionFromQuaternion(q Quaternion) Position {
	if q.W != 0 {
		panic("tried to convert non-vector quaternion to position")
	}

	return NewPositionFromCoordinates(int16(q.X), int16(q.Y), int16(q.Z))
}

func (p Position) GetX() int16 {
	return int16(p >> 32)
}

func (p Position) GetY() int16 {
	return int16(p >> 16)
}

func (p Position) GetZ() int16 {
	return int16(p)
}

func (p Position) Norm1() (norm int) {
	x := int(p.GetX())
	if x >= 0 {
		norm += x
	} else {
		norm -= x
	}

	y := int(p.GetY())
	if y >= 0 {
		norm += y
	} else {
		norm -= y
	}

	z := int(p.GetZ())
	if z >= 0 {
		norm += z
	} else {
		norm -= z
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
	return NewPositionFromCoordinates(p.GetX()+t.GetX(), p.GetY()+t.GetY(), p.GetZ()+t.GetZ())
}

func (p Position) String() string {
	return fmt.Sprintf("%d,%d,%d", p.GetX(), p.GetY(), p.GetZ())
}

func SubstractPositions(p1, p2 Position) Position {
	return NewPositionFromCoordinates(p1.GetX()-p2.GetX(), p1.GetY()-p2.GetY(), p1.GetZ()-p2.GetZ())
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
	return Quaternion{0, float64(p.GetX()), float64(p.GetY()), float64(p.GetZ())}
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
	// BeaconsRelativePosition contains the positions of the beacons relative to the current scanner
	// along any rotation possible, including the identity rotation
	BeaconsRelativePosition map[Quaternion][]Position

	Identified  bool
	Orientation Quaternion
	Position    Position
	Size        int
}

func NewScanner() Scanner {
	return Scanner{
		BeaconsAbsolutePosition: make(map[Position]struct{}),
		BeaconsRelativePosition: map[Quaternion][]Position{NewQuaternionFromCoordinates(1, 0, 0, 0): make([]Position, 0)},

		Identified:  false,
		Orientation: NewQuaternionFromCoordinates(1, 0, 0, 0),
		Position:    NewPositionFromCoordinates(0, 0, 0),
		Size:        0,
	}
}

func (sc *Scanner) AddBeacon(x, y, z int16) {
	beacon := NewPositionFromCoordinates(x, y, z)

	sc.BeaconsAbsolutePosition[beacon] = struct{}{}
	sc.BeaconsRelativePosition[sc.Orientation] = append(sc.BeaconsRelativePosition[sc.Orientation], beacon)
	sc.Size++
}

// UpdateOrientationAndPositionWithFailFast rotates sc by q, and translates it by p
// If target is not nil, it returns as soon as we know sc has not enough beacons in common with it
func (sc *Scanner) UpdateOrientationAndPositionWithFailFast(q Quaternion, p Position, target *map[Position]struct{}) bool {
	sc.Orientation = q
	sc.Position = p

	// Cache computation of rotations
	if _, ok := sc.BeaconsRelativePosition[sc.Orientation]; !ok {
		sc.BeaconsRelativePosition[sc.Orientation] = make([]Position, sc.Size)
		for idx, beacon := range sc.BeaconsRelativePosition[NewQuaternionFromCoordinates(1, 0, 0, 0)] {
			sc.BeaconsRelativePosition[sc.Orientation][idx] = beacon.Rotate(sc.Orientation)
		}
	}

	countCommonBeacons := 0
	sc.BeaconsAbsolutePosition = make(map[Position]struct{}, sc.Size)
	for idx, beacon := range sc.BeaconsRelativePosition[sc.Orientation] {
		translated := beacon.Translate(sc.Position)
		sc.BeaconsAbsolutePosition[translated] = struct{}{}

		if target != nil {
			if _, ok := (*target)[translated]; ok {
				countCommonBeacons++
			}

			// Careful we cannot return true yet even if countCommonBeacons >= 12
			// because in this case sc.BeaconsAbsolutePosition needs to hold all beacons
			if sc.Size-idx-1+countCommonBeacons < NumberOfBeaconsSharedBetweenNeighbors {
				return false
			}
		}
	}

	return true
}

func IdentifyScanners(s string) []*Scanner {
	scanners := make([]*Scanner, 0)
	for _, lines := range strings.Split(s, "\n\n") {
		scanner := NewScanner()
		for _, line := range strings.Split(lines, "\n")[1:] {
			split := strings.Split(line, ",")
			x, _ := strconv.ParseInt(split[0], 10, 16)
			y, _ := strconv.ParseInt(split[1], 10, 16)
			z, _ := strconv.ParseInt(split[2], 10, 16)
			scanner.AddBeacon(int16(x), int16(y), int16(z))
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
					scanner.UpdateOrientationAndPositionWithFailFast(rotation, NewPositionFromCoordinates(0, 0, 0), nil)

					// Bruteforce all possible translations from one scanner to the other with at least one common beacon
					for _, source := range scanner.BeaconsRelativePosition[scanner.Orientation] {
						for destination := range identifiedScanner.BeaconsAbsolutePosition {
							translation := SubstractPositions(destination, source)
							if scanner.UpdateOrientationAndPositionWithFailFast(rotation, translation, &identifiedScanner.BeaconsAbsolutePosition) {
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

	result := 0
	for _, sc1 := range scanners {
		for _, sc2 := range scanners {
			distance := SubstractPositions(sc1.Position, sc2.Position).Norm1()
			if distance > result {
				result = distance
			}
		}
	}

	return result
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	// defer profile.Start(profile.CPUProfile).Stop()
	// defer profile.Start(profile.GoroutineProfile).Stop()
	// defer profile.Start(profile.BlockProfile).Stop()
	// defer profile.Start(profile.ThreadcreationProfile).Stop()
	// defer profile.Start(profile.MemProfileHeap).Stop()
	// defer profile.Start(profile.MemProfileAllocs).Stop()
	// defer profile.Start(profile.MutexProfile).Stop()

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
