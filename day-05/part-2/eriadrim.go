package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

const (
	maxSize          = 1000
	bitPerSideSquare = 4
	bitPerSquare     = bitPerSideSquare * bitPerSideSquare
	sideSize         = maxSize/ bitPerSideSquare
	bufferSize       = sideSize * sideSize

	zero, one, fullRow, fullCol, fullDiag, fullDiagRev uint16 = 0, 1, 0xf, 0x1111, 0x8421, 0x1248
)

func run(s []byte) int {
	var buffer, over [bufferSize]uint16
	cursor := 0
	for i := 0; i < 500; i++ {
		// parse values
		x1 := 0
		for s[cursor] != ',' {
			x1 = 10*x1 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor++
		y1 := 0
		for s[cursor] != ' ' {
			y1 = 10*y1 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor += 4
		x2 := 0
		for s[cursor] != ',' {
			x2 = 10*x2 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor++
		y2 := 0
		for cursor < len(s) && s[cursor] != '\n' {
			y2 = 10*y2 + int(s[cursor] & 0xf)
			cursor++
		}
		cursor++

		//
		if x1 == x2 {
			if y2 < y1 {
				y1, y2 = y2, y1
			}

			xID := x1/bitPerSideSquare
			minID := sideSize * xID + y1/bitPerSideSquare
			maxID := sideSize * xID + y2/bitPerSideSquare

			rowShift := bitPerSideSquare*(x1%bitPerSideSquare)
			minShift := y1%bitPerSideSquare
			maxShift := y2%bitPerSideSquare

			minSquare := (fullRow ^ ((one << minShift) - 1)) << rowShift
			maxSquare := ((one << (maxShift+1)) - 1) << rowShift
			if minID == maxID {
				row := minSquare & maxSquare
				over[minID] |= buffer[minID] & row
				buffer[minID] |= row
				continue
			}

			square := fullRow << rowShift
			for id := minID + 1; id < maxID; id+=1 {
				over[id] |= buffer[id] & square
				buffer[id] |= square
			}
			over[minID] |= buffer[minID] & minSquare
			buffer[minID] |= minSquare

			over[maxID] |= buffer[maxID] & maxSquare
			buffer[maxID] |= maxSquare
		} else if y1 == y2 {
			if x2 < x1 {
				x1, x2 = x2, x1
			}

			yID := y1/bitPerSideSquare
			minID := sideSize * (x1/bitPerSideSquare) + yID
			maxID := sideSize * (x2/bitPerSideSquare) + yID

			colShift := y1%bitPerSideSquare
			minShift := x1%bitPerSideSquare
			maxShift := x2%bitPerSideSquare

			minSquare := zero
			for k := 0; k < minShift; k++ {
				minSquare <<= bitPerSideSquare
				minSquare |= one
			}
			minSquare = (fullCol ^ minSquare) << colShift

			maxSquare := zero
			for k := 0; k < maxShift+1; k++ {
				maxSquare <<= bitPerSideSquare
				maxSquare |= one
			}
			maxSquare = maxSquare << colShift

			if minID == maxID {
				row := minSquare & maxSquare
				over[minID] |= buffer[minID] & row
				buffer[minID] |= row
				continue
			}

			square := fullCol << colShift

			for id := minID + sideSize; id < maxID; id+=sideSize {
				over[id] |= buffer[id] & square
				buffer[id] |= square
			}
			over[minID] |= buffer[minID] & minSquare
			buffer[minID] |= minSquare

			over[maxID] |= buffer[maxID] & maxSquare
			buffer[maxID] |= maxSquare
		} else if (y1-y2)*(x1-x2) > 0 {
			if x2 < x1 {
				x1, x2 = x2, x1
				y1, y2 = y2, y1
			}

			relX1 := x1%bitPerSideSquare
			relY1 := y1%bitPerSideSquare
			relX2 := x2%bitPerSideSquare
			relY2 := y2%bitPerSideSquare

			diag := relX1 == relY1
			top := relY1 > relX1

			minID := sideSize * (x1/bitPerSideSquare) + (y1/bitPerSideSquare)
			maxID := sideSize * (x2/bitPerSideSquare) + (y2/bitPerSideSquare)

			minIter := bitPerSideSquare - relX1
			if relX1 < relY1 {
				minIter = bitPerSideSquare - relY1
			}
			token := one << (bitPerSideSquare*relX1 + relY1)
			minSquare := token
			for k := 1; k < minIter; k++{
				minSquare <<= bitPerSideSquare + 1
				minSquare |= token
			}

			maxIter := relX2+1
			if relX2 > relY2 {
				maxIter = relY2+1
			}
			token = one << (bitPerSideSquare*relX2 + relY2)
			maxSquare := token
			for k := 1; k < maxIter; k++{
				maxSquare >>= bitPerSideSquare + 1
				maxSquare |= token
			}

			if minID == maxID {
				row := minSquare & maxSquare
				over[minID] |= buffer[minID] & row
				buffer[minID] |= row
				continue
			}

			id := minID
			if diag {
				id += sideSize+1
			} else if top {
				id += 1
				top = false
			} else {
				id += sideSize
				top = true
			}

			shiftTop := ((relY1 - relX1)+bitPerSideSquare)%bitPerSideSquare
			shiftBottom := bitPerSideSquare-shiftTop
			squareTop := fullDiag >> (shiftTop * bitPerSideSquare)
			squareBottom := (fullDiag >> (shiftBottom * bitPerSideSquare)) << (shiftBottom * (bitPerSideSquare-1))
			for id < maxID {
				if diag {
					over[id] |= buffer[id] & fullDiag
					buffer[id] |= fullDiag
					id += sideSize+1
				} else if top {
					over[id] |= buffer[id] & squareTop
					buffer[id] |= squareTop
					id += 1
					top = false
				} else {
					over[id] |= buffer[id] & squareBottom
					buffer[id] |= squareBottom
					id += sideSize
					top = true
				}
			}

			over[minID] |= buffer[minID] & minSquare
			buffer[minID] |= minSquare

			over[maxID] |= buffer[maxID] & maxSquare
			buffer[maxID] |= maxSquare
		} else if (y1-y2)*(x1-x2) < 0 {
			if x2 < x1 {
				x1, x2 = x2, x1
				y1, y2 = y2, y1
			}

			relX1 := x1%bitPerSideSquare
			relY1 := y1%bitPerSideSquare
			relX2 := x2%bitPerSideSquare
			relY2 := y2%bitPerSideSquare

			diag := relX1 + relY1 == bitPerSideSquare-1
			top := relX1 + relY1 < bitPerSideSquare-1

			minID := sideSize * (x1/bitPerSideSquare) + (y1/bitPerSideSquare)
			maxID := sideSize * (x2/bitPerSideSquare) + (y2/bitPerSideSquare)

			minIter := bitPerSideSquare - relX1
			if minIter > relY1 + 1 {
				minIter = relY1 + 1
			}
			token := one << (bitPerSideSquare*relX1 + relY1)
			minSquare := token
			for k := 1; k < minIter; k++{
				minSquare <<= bitPerSideSquare - 1
				minSquare |= token
			}

			maxIter := bitPerSideSquare - relY2
			if maxIter > relX2 + 1 {
				maxIter = relX2 + 1
			}
			token = one << (bitPerSideSquare*relX2 + relY2)
			maxSquare := token
			for k := 1; k < maxIter; k++{
				maxSquare >>= bitPerSideSquare - 1
				maxSquare |= token
			}

			if minID == maxID {
				row := minSquare & maxSquare
				over[minID] |= buffer[minID] & row
				buffer[minID] |= row
				continue
			}

			id := minID
			if diag {
				id += sideSize-1
			} else if top {
				id -= 1
				top = false
			} else {
				id += sideSize
				top = true
			}

			shiftTop := (2*bitPerSideSquare - (relX1 + relY1+1))%bitPerSideSquare
			shiftBottom := bitPerSideSquare-shiftTop
			squareTop := fullDiagRev >> (shiftTop * bitPerSideSquare)
			squareBottom := (fullDiagRev >> (shiftBottom * bitPerSideSquare)) << (shiftBottom * (bitPerSideSquare+1))
			for id != maxID {
				if diag {
					over[id] |= buffer[id] & fullDiagRev
					buffer[id] |= fullDiagRev
					id += sideSize-1
				} else if top {
					over[id] |= buffer[id] & squareTop
					buffer[id] |= squareTop
					id -= 1
					top = false
				} else {
					over[id] |= buffer[id] & squareBottom
					buffer[id] |= squareBottom
					id += sideSize
					top = true
				}
			}

			over[minID] |= buffer[minID] & minSquare
			buffer[minID] |= minSquare

			over[maxID] |= buffer[maxID] & maxSquare
			buffer[maxID] |= maxSquare
		}
	}

	res := 0
	for i := 0; i < bufferSize; i++ {
		if over[i] != 0 {
			res += count(over[i])
		}
	}
	return res
}

func count(x uint16) int {
	res := 0
	p := uint16(1)
	i := 0
	for i < bitPerSquare {
		if p & x != 0 {
			res += 1
		}
		p <<= 1
		i++
	}
	return res
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
	result := run(input)

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}


