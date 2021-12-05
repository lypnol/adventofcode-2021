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
	cursor := 0
	for j := 0; j < 1000; j++ {
		if tab[j] & 0x800 != 0 {
			tab[j], tab[cursor] = tab[cursor], tab[j]
			cursor++
		}
	}
	firstG, lastG := 0, 1000
	firstE, lastE := 0, 1000
	if cursor >= 500 {
		lastG = cursor
		firstE = cursor
	} else {
		lastE = cursor
		firstG = cursor
	}

	first, last := firstG, lastG
	var p = uint16(0x400)
	for i := 1; i < 12; i++ {
		if last - first < 2 {
			gamma = tab[first]
			break
		}
		n := last-first
		m := 0
		newCursor := first
		for j := first; j < last; j++ {
			x := tab[j]
			if x & p != 0 {
				tab[newCursor], tab[j] = tab[j], tab[newCursor]
				newCursor++
				m++
			}
		}

		if m * 2 >= n {
			last = newCursor
		} else {
			first = newCursor
		}
		p >>= 1
	}
	if gamma == 0 {
		gamma = tab[first]
	}

	first, last = firstE, lastE
	p = uint16(0x400)
	for i := 1; i < 12; i++ {
		if last - first < 2 {
			epsilon = tab[first]
			break
		}
		n := last-first
		m := 0
		newCursor := first
		for j := first; j < last; j++ {
			x := tab[j]
			if x & p != 0 {
				tab[newCursor], tab[j] = tab[j], tab[newCursor]
				newCursor++
				m++
			}
		}

		if m * 2 >= n {
			first = newCursor
		} else {
			last = newCursor
		}
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
