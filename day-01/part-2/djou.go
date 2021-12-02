package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

func run(s string) interface{} {
	var ts = strings.Split(s, "\n")
	l := len(ts)
	ti := make([]int, l)
	for i, t := range ts {
		ti[i], _ = strconv.Atoi(t)
	}

	count := 0
	for i := 3; i < l; i++ {
		if ti[i - 3] < ti[i] {
			count ++
		}
	}

	return count
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

	// Read input from stdin
	input, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}

	// Start resolution
	start := time.Now()
	result := run(string(input))

	// Print result
	fmt.Printf("_duration:%f\n", time.Since(start).Seconds()*1000)
	fmt.Println(result)
}
