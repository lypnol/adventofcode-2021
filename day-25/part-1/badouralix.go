package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

type SeaFloor struct {
	// MaxI contains the number of rows of the puzzle
	MaxI int
	// MaxJ contains the number of columns of the puzzle
	MaxJ int
	// State contains both the previous and current sea cumcumber for each location of the puzzle
	State [][][2]rune
	// StateID is the id of the current active state
	StateID int
}

func NewSeaFloor(s string) SeaFloor {
	lines := strings.Split(s, "\n")
	state := make([][][2]rune, 0, len(lines))

	for _, line := range lines {
		row := make([][2]rune, 0, len(line))
		for _, location := range line {
			row = append(row, [2]rune{location, '.'})
		}
		state = append(state, row)
	}

	return SeaFloor{
		MaxI:    len(lines),
		MaxJ:    len(lines[0]),
		State:   state,
		StateID: 0,
	}
}

func (sf *SeaFloor) Step() bool {
	counter := 0

	// Clear state to hold the new one
	for i := 0; i < sf.MaxI; i++ {
		for j := 0; j < sf.MaxJ; j++ {
			sf.State[i][j][1-sf.StateID] = '.'
		}
	}

	// Move all sea cumcumbers that move east
	for i := 0; i < sf.MaxI; i++ {
		for j := 0; j < sf.MaxJ; j++ {
			if sf.State[i][j][sf.StateID] == '>' {
				nextj := j + 1
				if nextj == sf.MaxJ {
					nextj = 0
				}

				if sf.State[i][nextj][sf.StateID] == '.' {
					sf.State[i][j][1-sf.StateID] = '.'
					sf.State[i][nextj][1-sf.StateID] = '>'
					counter++
				} else {
					sf.State[i][j][1-sf.StateID] = '>'
				}
			}
		}
	}

	// Move all sea cumcumbers that move south
	for i := 0; i < sf.MaxI; i++ {
		for j := 0; j < sf.MaxJ; j++ {
			if sf.State[i][j][sf.StateID] == 'v' {
				nexti := i + 1
				if nexti == sf.MaxI {
					nexti = 0
				}

				if sf.State[nexti][j][sf.StateID] != 'v' && sf.State[nexti][j][1-sf.StateID] == '.' {
					sf.State[i][j][1-sf.StateID] = '.'
					sf.State[nexti][j][1-sf.StateID] = 'v'
					counter++
				} else {
					sf.State[i][j][1-sf.StateID] = 'v'
				}
			}
		}
	}

	// Update id of the active state
	sf.StateID = 1 - sf.StateID

	// Return true if and only if at least one sea cumcumber moved
	return counter != 0
}

func (sf SeaFloor) String() (output string) {
	for i := 0; i < sf.MaxI; i++ {
		for j := 0; j < sf.MaxJ; j++ {
			output += string(sf.State[i][j][sf.StateID])
		}
		output += "\n"
	}
	return output
}

func run(s string) int {
	// Your code goes here
	result := 1
	seafloor := NewSeaFloor(s)

	for seafloor.Step() {
		result++
	}

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
