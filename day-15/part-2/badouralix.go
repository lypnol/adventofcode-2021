package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"strings"
	"time"
)

const (
	RepeatCount = 5
	TileSize    = 100
)

type Position struct {
	X int
	Y int
}

func NewPosition(x, y int) Position {
	return Position{x, y}
}

type Vertex struct {
	Position  Position
	Risk      int
	TotalRisk int
	Visited   bool
}

func NewVertex(p Position, risk int) *Vertex {
	return &Vertex{
		Position:  p,
		Risk:      risk,
		TotalRisk: math.MaxInt32,
		Visited:   false,
	}
}

type VertexSet map[*Vertex]struct{}

func NewVertexSet() VertexSet {
	return make(VertexSet)
}

func (vs VertexSet) Add(v *Vertex) {
	vs[v] = struct{}{}
}

func (vs VertexSet) PopSmallest() (v *Vertex) {
	currentTotalRisk := math.MaxInt32

	for candidate := range vs {
		if candidate.TotalRisk < currentTotalRisk {
			v = candidate
			currentTotalRisk = candidate.TotalRisk
		}
	}

	delete(vs, v)
	return v
}

type Graph struct {
	Edges    map[Position][]*Vertex
	Finish   Position
	Start    Position
	Vertices map[Position]*Vertex
}

func NewGraph(s string) *Graph {
	edges := make(map[Position][]*Vertex)
	vertices := make(map[Position]*Vertex)

	for x, line := range strings.Split(s, "\n") {
		for y, char := range line {
			for i := 0; i < RepeatCount; i++ {
				for j := 0; j < RepeatCount; j++ {
					p := NewPosition(x+TileSize*i, y+TileSize*j)
					risk := int(char-'0') + i + j
					if risk > 9 {
						risk -= 9
					}
					vertices[p] = NewVertex(p, risk)
				}
			}
		}
	}

	for p := range vertices {
		edges[p] = make([]*Vertex, 0, 4)

		if v, ok := vertices[NewPosition(p.X-1, p.Y)]; ok {
			edges[p] = append(edges[p], v)
		}
		if v, ok := vertices[NewPosition(p.X+1, p.Y)]; ok {
			edges[p] = append(edges[p], v)
		}
		if v, ok := vertices[NewPosition(p.X, p.Y-1)]; ok {
			edges[p] = append(edges[p], v)
		}
		if v, ok := vertices[NewPosition(p.X, p.Y+1)]; ok {
			edges[p] = append(edges[p], v)
		}
	}

	return &Graph{
		Edges:    edges,
		Finish:   NewPosition(TileSize*RepeatCount-1, TileSize*RepeatCount-1),
		Start:    NewPosition(0, 0),
		Vertices: vertices,
	}
}

func (g *Graph) FindLowestTotalRiskWithDijkstra() int {
	g.Vertices[g.Start].TotalRisk = 0

	remaining := NewVertexSet()
	remaining.Add(g.Vertices[g.Start])

	for {
		current := remaining.PopSmallest()

		for _, neighbor := range g.Edges[current.Position] {
			if neighbor.Visited {
				continue
			}

			if neighbor.TotalRisk > current.TotalRisk+neighbor.Risk {
				neighbor.TotalRisk = current.TotalRisk + neighbor.Risk
			}

			remaining.Add(neighbor)
		}

		current.Visited = true

		if current.Position == g.Finish {
			return current.TotalRisk
		}
	}

	return -1
}

func run(s string) int {
	// Your code goes here
	return NewGraph(s).FindLowestTotalRiskWithDijkstra()
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
