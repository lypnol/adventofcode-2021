package main

import (
	"container/heap"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"runtime/debug"
	"strings"
	"time"
)

const (
	RepeatCount = 5
	TileSize    = 100
	TotalSize   = TileSize * RepeatCount
)

type Position int

func NewPosition(x, y int) Position {
	return Position(x*TotalSize + y)
}

func (p Position) GetX() int {
	return int(p) / TotalSize
}

func (p Position) GetY() int {
	return int(p) % TotalSize
}

func (p Position) String() string {
	return fmt.Sprintf("(%d,%d)", p.GetX(), p.GetY())
}

type Vertex struct {
	Position  Position
	Risk      int
	TotalRisk int
	Visited   bool

	index int
}

func NewVertex(p Position, risk int) *Vertex {
	return &Vertex{
		Position:  p,
		Risk:      risk,
		TotalRisk: math.MaxInt32,
		Visited:   false,

		index: -1,
	}
}

func (v Vertex) String() string {
	return fmt.Sprintf("%s=%d", v.Position, v.TotalRisk)
}

type VertexSet []*Vertex

func NewVertexSet() VertexSet {
	return make(VertexSet, 0)
}

func (vs VertexSet) Len() int {
	return len(vs)
}

func (vs VertexSet) Less(i, j int) bool {
	return vs[i].TotalRisk < vs[j].TotalRisk
}

func (vs VertexSet) Swap(i, j int) {
	vs[i], vs[j] = vs[j], vs[i]
	vs[i].index = i
	vs[j].index = j
}

func (vs *VertexSet) Push(x interface{}) {
	n := len(*vs)
	v := x.(*Vertex)
	v.index = n
	*vs = append(*vs, v)
}

func (vs *VertexSet) Pop() interface{} {
	old := *vs
	n := len(old)
	v := old[n-1]
	old[n-1] = nil
	v.index = -1
	*vs = old[0 : n-1]
	return v
}

type Graph struct {
	Edges    [][]*Vertex
	Finish   Position
	Start    Position
	Vertices []*Vertex
}

func NewGraph(s string) *Graph {
	edges := make([][]*Vertex, TotalSize*TotalSize)
	vertices := make([]*Vertex, TotalSize*TotalSize)

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

	for x := 0; x < TileSize; x++ {
		for y := 0; y < TileSize; y++ {
			for i := 0; i < RepeatCount; i++ {
				for j := 0; j < RepeatCount; j++ {
					p := NewPosition(x+TileSize*i, y+TileSize*j)
					edges[p] = make([]*Vertex, 0, 4)

					if p.GetX() != 0 {
						edges[p] = append(edges[p], vertices[NewPosition(p.GetX()-1, p.GetY())])
					}
					if p.GetX() != TotalSize-1 {
						edges[p] = append(edges[p], vertices[NewPosition(p.GetX()+1, p.GetY())])
					}
					if p.GetY() != 0 {
						edges[p] = append(edges[p], vertices[NewPosition(p.GetX(), p.GetY()-1)])
					}
					if p.GetY() != TotalSize-1 {
						edges[p] = append(edges[p], vertices[NewPosition(p.GetX(), p.GetY()+1)])
					}
				}
			}
		}
	}

	return &Graph{
		Edges:    edges,
		Finish:   NewPosition(TotalSize-1, TotalSize-1),
		Start:    NewPosition(0, 0),
		Vertices: vertices,
	}
}

func (g *Graph) FindLowestTotalRiskWithDijkstra() int {
	remaining := NewVertexSet()
	heap.Init(&remaining)

	g.Vertices[g.Start].TotalRisk = 0
	heap.Push(&remaining, g.Vertices[g.Start])

	for {
		current := heap.Pop(&remaining).(*Vertex)

		for _, neighbor := range g.Edges[current.Position] {
			if neighbor.Visited {
				continue
			}

			if neighbor.TotalRisk > current.TotalRisk+neighbor.Risk {
				neighbor.TotalRisk = current.TotalRisk + neighbor.Risk
			}

			if neighbor.index == -1 {
				heap.Push(&remaining, neighbor)
			} else {
				heap.Fix(&remaining, neighbor.index)
			}
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
	debug.SetGCPercent(-1)

	// defer profile.Start(profile.CPUProfile).Stop()
	// defer profile.Start(profile.GoroutineProfile).Stop()
	// defer profile.Start(profile.BlockProfile).Stop()
	// defer profile.Start(profile.ThreadcreationProfile).Stop()
	// defer profile.Start(profile.MemProfileHeap).Stop()
	// defer profile.Start(profile.MemProfileAllocs).Stop()
	// defer profile.Start(profile.MutexProfile).Stop()

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
