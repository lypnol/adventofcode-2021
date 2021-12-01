package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"
)

func run(s string) interface{} {
	// Your code goes here
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	argsWithProg := os.Args
	var input []byte
	var err error
	if len(argsWithProg) > 1 {
		input,err = ioutil.ReadFile(argsWithProg[1])
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
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
