package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(b []byte) interface{} {
	p := 1
	gamma := 0
	for i := 11; i >= 0; i-- {
		m := 0
		for cursor := i; cursor < len(b); cursor += 13 {
			if b[cursor] == '1' {
				m++
			}
		}
		if m > 500 {
			gamma |= p
		}
		p <<= 1
	}

	epsilon := 0xfff ^ gamma
	return epsilon * gamma
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
