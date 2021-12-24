package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Point struct {
	x int
	y int
}

type Line struct {
	start Point
	end Point
}

func getPoints(line *Line) []Point {
	var result []Point
	if line.start.x == line.end.x {
		var minY, maxY int
		if line.start.y >= line.end.y {
			minY = line.end.y
			maxY = line.start.y
		} else {
			maxY = line.end.y
			minY = line.start.y
		}
		for y := minY; y <= maxY; y++ {
			result = append(result, Point{line.start.x, y})
		}
	} else if line.start.y == line.end.y {
		var minX, maxX int
		if line.start.x >= line.end.x {
			minX = line.end.x
			maxX = line.start.x
		} else {
			maxX = line.end.x
			minX = line.start.x
		}
		for x := minX; x <= maxX; x++ {
			result = append(result, Point{x, line.start.y})
		}
	}
	/*else {
		fmt.Printf("Not vertical or horizontal line : %v\n", line)
	}*/
	return result
}

type Puzzle struct {
	lines []Line
}

func parsePoint(pointStr string) Point {
	coords := strings.Split(pointStr, ",")
	x, _ := strconv.Atoi(coords[0])
	y, _ := strconv.Atoi(coords[1])
	return Point{
		x: x,
		y: y,
	}
}

func parseData(input string) Puzzle {
	var lines []Line
	for _, line := range strings.Split(input, "\n") {
		if len(line) > 0 {
			points := strings.Split(line, " -> ")
			startPoint := parsePoint(points[0])
			endPoint := parsePoint(points[1])
			lines = append(lines, Line{
				start: startPoint,
				end:   endPoint,
			})
		}
	}
	return Puzzle{lines: lines}
}

func puzzle(puzzle Puzzle) int {
	var grid [][]int
	grid = make([][]int, 1000)
	for i := 0; i < 1000; i++ {
		grid[i] = make([]int, 1000)
	}
	var plus2Count int = 0
	for _, line := range puzzle.lines {
		points := getPoints(&line)
		for _, point := range points {
			value := grid[point.x][point.y] +1
			grid[point.x][point.y] = value
			if value == 2 {
				plus2Count++
			}
		}
	}
	return plus2Count
}

func run(s string) interface{} {
	// Your code goes here
	data := parseData(s)
	result := puzzle(data)
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
