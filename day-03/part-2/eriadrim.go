package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(b []byte) interface{} {
	tab := [1000]uint16{}
	for i := 0; i < 1000; i++ {
		tab[i] = convertToInt(b[13*i:13*i+12])
	}

	var gamma, epsilon uint16 = 0, 0

	// first iter
	m := 0
	for j := 0; j < 1000; j++ {
		if b[13*j] == '1' {
			m++
		}
	}
	if m >= 500 {
		gamma = 0x800
	} else {
		epsilon = 0x800
	}

	var p, mask uint16 = 0x400, 0x800
	var lastG uint16
	for i := 1; i < 12; i++ {
		mG, nG := 0, 0
		for j := 0; j < 1000; j++ {
			x := tab[j]
			c := b[13*j+i]
			if gamma ^ (x & mask) != 0 {
				continue
			}

			nG++
			if c == '1' {
				mG++
			}
			lastG = x
		}
		if nG == 1 {
			gamma = lastG
			break
		}
		if mG * 2 >= nG {
			gamma |= p
		}
		mask |= p
		p >>= 1
	}

	p, mask = 0x400, 0x800
	var lastE uint16
	for i := 1; i < 12; i++ {
		mE, nE := 0, 0
		for j := 0; j < 1000; j++ {
			x := tab[j]
			c := b[13*j+i]
			if epsilon ^ (x & mask) != 0 {
				continue
			}

			nE++
			if c == '1' {
				mE++
			}
			lastE = x
		}
		if nE == 1 {
			epsilon = lastE
			break
		}
		if mE * 2 < nE {
			epsilon |= p
		}
		mask |= p
		p >>= 1
	}

	return int(epsilon) * int(gamma)
}

func convertToInt(b []byte) uint16 {
	p := uint16(1)
	res := uint16(0)
	for i := 11; i >= 0; i-- {
		if b[i] == '1' {
			res |= p
		}
		p <<=1
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
