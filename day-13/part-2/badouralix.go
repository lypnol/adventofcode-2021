package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"runtime/debug"
	"strconv"
	"strings"
	"time"
)

type Dot struct {
	X int
	Y int
}

type Paper struct {
	Grid map[Dot]struct{}
	MinX int
	MinY int
	MaxX int
	MaxY int
}

func NewPaper() Paper {
	return Paper{
		Grid: make(map[Dot]struct{}),
	}
}

func (p *Paper) AddDot(x, y int) {
	p.Grid[Dot{x, y}] = struct{}{}

	if x < p.MinX {
		p.MinX = x
	}
	if x > p.MaxX {
		p.MaxX = x
	}

	if y < p.MinY {
		p.MinY = y
	}
	if y > p.MaxY {
		p.MaxY = y
	}
}

func (p *Paper) DelDot(x, y int) {
	delete(p.Grid, Dot{x, y})
}

func (p *Paper) FoldLeft(v int) {
	for dot := range p.Grid {
		if dot.X <= v {
			continue
		}

		p.AddDot(2*v-dot.X, dot.Y)
		p.DelDot(dot.X, dot.Y)
	}

	p.MaxX = v
}

func (p *Paper) FoldUp(v int) {
	for dot := range p.Grid {
		if dot.Y <= v {
			continue
		}

		p.AddDot(dot.X, 2*v-dot.Y)
		p.DelDot(dot.X, dot.Y)
	}

	p.MaxY = v
}

func (p Paper) Len() int {
	return len(p.Grid)
}

func (p Paper) String() (output string) {
	for y := p.MinY; y < p.MaxY; y++ {
		for x := p.MinX; x < p.MaxX; x++ {
			if _, ok := p.Grid[Dot{x, y}]; ok {
				output += "#"
			} else {
				output += "."
			}
		}
		output += "\n"
	}
	return output[:len(output)-1]
}

func run(s string) (output string) {
	// Your code goes here
	paper := NewPaper()
	split := strings.Split(s, "\n\n")

	for _, line := range strings.Split(split[0], "\n") {
		coordinates := strings.Split(line, ",")
		x, _ := strconv.Atoi(coordinates[0])
		y, _ := strconv.Atoi(coordinates[1])
		paper.AddDot(x, y)
	}

	for _, instruction := range strings.Split(split[1], "\n") {
		v, _ := strconv.Atoi(strings.Split(instruction, "=")[1])
		if instruction[11] == 'x' {
			paper.FoldLeft(v)
		} else {
			paper.FoldUp(v)
		}
	}

	return paper.String()
}

func main() {
	// Uncomment this line to disable garbage collection
	debug.SetGCPercent(-1)

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
	fmt.Println("_parse")
	fmt.Println(result)
}
