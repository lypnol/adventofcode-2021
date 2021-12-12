package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
	"unicode"
)

type Vertex struct {
	Name    string
	Small   bool
	Visited bool
}

func NewVertex(name string) *Vertex {
	vertex := Vertex{Name: name}

	if unicode.IsLower(rune(name[0])) {
		vertex.Small = true
	}

	return &vertex
}

type Graph struct {
	Edges    map[string][]string
	Vertices map[string]*Vertex
}

func NewGraph(s string) Graph {
	edges := make(map[string][]string)
	vertices := make(map[string]*Vertex)

	for _, line := range strings.Split(s, "\n") {
		split := strings.Split(line, "-")
		if _, ok := vertices[split[0]]; !ok {
			vertices[split[0]] = NewVertex(split[0])
		}
		if _, ok := vertices[split[1]]; !ok {
			vertices[split[1]] = NewVertex(split[1])
		}

		if _, ok := edges[split[0]]; !ok {
			edges[split[0]] = make([]string, 0)
		}
		if _, ok := edges[split[1]]; !ok {
			edges[split[1]] = make([]string, 0)
		}
		edges[split[0]] = append(edges[split[0]], split[1])
		edges[split[1]] = append(edges[split[1]], split[0])
	}

	return Graph{Edges: edges, Vertices: vertices}
}

func (g *Graph) CountPathsToEnd(src string) (result int) {
	if src == "end" {
		return 1
	}

	g.Vertices[src].Visited = true
	for _, dst := range g.Edges[src] {
		if g.Vertices[dst].Visited && g.Vertices[dst].Small {
			continue
		}

		result += g.CountPathsToEnd(dst)
	}

	g.Vertices[src].Visited = false
	return result
}

func run(s string) int {
	// Your code goes here
	graph := NewGraph(s)

	return graph.CountPathsToEnd("start")
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
