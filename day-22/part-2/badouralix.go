package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

type Cuboid struct {
	Xmin, Xmax int
	Ymin, Ymax int
	Zmin, Zmax int
}

func (c Cuboid) Volume() int {
	return (c.Xmax - c.Xmin + 1) * (c.Ymax - c.Ymin + 1) * (c.Zmax - c.Zmin + 1)
}

// SplitCuboidAroundOtherCuboid returns a list of cuboids such that for each cube in c1 and not c2
// there is one and only one cuboid containing it.
//
//      ┌────────────────────────────────────────────────────────┐
//      │                                                        │
//      │   ┌──────────┐                     ┌───┐┌─────┐        │
//      │   │          │                     │   ││     │        │
//      │   │   c1     │         becomes     │   │└─────┘        │
//      │   │    ┌─────┼────┐   ─────────►   │   │┌──────────┐   │
//      │   │    │     │    │                │   ││          │   │
//      │   └────┼─────┘    │                └───┘│          │   │
//      │        │     c2   │                     │          │   │
//      │        └──────────┘                     └──────────┘   │
//      │                                                        │
//      └────────────────────────────────────────────────────────┘
//
func SplitCuboidAroundOtherCuboid(c1, c2 Cuboid) (cuboids []Cuboid) {
	xmin := c1.Xmin
	xmax := c1.Xmax
	ymin := c1.Ymin
	ymax := c1.Ymax
	zmin := c1.Zmin
	zmax := c1.Zmax

	// When c1 is completely left or right or below or above or behind or in front of c1, return c1
	if c1.Xmax < c2.Xmin || c1.Xmin > c2.Xmax || c1.Ymax < c2.Ymin || c1.Ymin > c2.Ymax || c1.Zmax < c2.Zmin || c1.Zmin > c2.Zmax {
		cuboids = append(cuboids, Cuboid{xmin, xmax, ymin, ymax, zmin, zmax})
		return cuboids
	}

	// When part of c1 is left from c2, cut the left part of c1 into a dedicated cuboid
	if c1.Xmin < c2.Xmin {
		cuboids = append(cuboids, Cuboid{xmin, c2.Xmin - 1, ymin, ymax, zmin, zmax})
		xmin = c2.Xmin
	}
	// When part of c1 is right from c2, cut the right part of c1 into a dedicated cuboid
	if c1.Xmax > c2.Xmax {
		cuboids = append(cuboids, Cuboid{c2.Xmax + 1, xmax, ymin, ymax, zmin, zmax})
		xmax = c2.Xmax
	}

	// When c1 is completely below or above or behind or in front of c1, return c1
	if c1.Ymax < c2.Ymin || c1.Ymin > c2.Ymax || c1.Zmax < c2.Zmin || c1.Zmin > c2.Zmax {
		cuboids = append(cuboids, Cuboid{xmin, xmax, ymin, ymax, zmin, zmax})
		return cuboids
	}

	// When part of c1 is below c2, cut the bottom part of c1 into a dedicated cuboid
	if c1.Ymin < c2.Ymin {
		cuboids = append(cuboids, Cuboid{xmin, xmax, ymin, c2.Ymin - 1, zmin, zmax})
		ymin = c2.Ymin
	}
	// When part of c1 is above c2, cut the top part of c1 into a dedicated cuboid
	if c1.Ymax > c2.Ymax {
		cuboids = append(cuboids, Cuboid{xmin, xmax, c2.Ymax + 1, ymax, zmin, zmax})
		ymax = c2.Ymax
	}

	// When c1 is completely behind or in front of c1, return c1
	if c1.Zmax < c2.Zmin || c1.Zmin > c2.Zmax {
		cuboids = append(cuboids, Cuboid{xmin, xmax, ymin, ymax, zmin, zmax})
		return cuboids
	}

	// When part of c1 is behind of c2, cut the behind part of c1 into a dedicated cuboid
	if c1.Zmin < c2.Zmin {
		cuboids = append(cuboids, Cuboid{xmin, xmax, ymin, ymax, zmin, c2.Zmin - 1})
		// zmin = c2.Zmin
	}
	// When part of c1 is in front of c2, cut the front part of c1 into a dedicated cuboid
	if c1.Zmax > c2.Zmax {
		cuboids = append(cuboids, Cuboid{xmin, xmax, ymin, ymax, c2.Zmax + 1, zmax})
		// zmax = c2.Zmax
	}

	// At this point, c2 == Cuboid{xmin, xmax, ymin, ymax, zmin, zmax}
	// It is not added to cuboids, as it will be added to the reactor later on

	return cuboids
}

type Reactor []Cuboid

func NewEmptyReactor() Reactor {
	// A reactor contains at most 4096 cuboids, and way less than that most of the time
	return make(Reactor, 0, 2<<10)
}

func NewReactorAfterTurningOffACuboid(reactor Reactor, cuboid Cuboid) Reactor {
	newreactor := NewEmptyReactor()

	for _, c := range reactor {
		newreactor = append(newreactor, SplitCuboidAroundOtherCuboid(c, cuboid)...)
	}

	return newreactor
}

func NewReactorAfterTurningOnACuboid(reactor Reactor, cuboid Cuboid) Reactor {
	newreactor := NewReactorAfterTurningOffACuboid(reactor, cuboid)
	newreactor = append(newreactor, cuboid)
	return newreactor
}

func (r Reactor) Volume() (volume int) {
	for _, c := range r {
		volume += c.Volume()
	}

	return volume
}

func run(s string) int {
	// Your code goes here
	reactor := NewEmptyReactor()

	for idx, line := range strings.Split(s, "\n") {
		_ = idx

		ssplit := strings.Split(line, " ")
		nsplit := strings.Split(ssplit[1], ",")

		xsplit := strings.Split(nsplit[0][2:], "..")
		xmin, _ := strconv.Atoi(xsplit[0])
		xmax, _ := strconv.Atoi(xsplit[1])

		ysplit := strings.Split(nsplit[1][2:], "..")
		ymin, _ := strconv.Atoi(ysplit[0])
		ymax, _ := strconv.Atoi(ysplit[1])

		zsplit := strings.Split(nsplit[2][2:], "..")
		zmin, _ := strconv.Atoi(zsplit[0])
		zmax, _ := strconv.Atoi(zsplit[1])

		switch ssplit[0] {
		case "off":
			reactor = NewReactorAfterTurningOffACuboid(reactor, Cuboid{xmin, xmax, ymin, ymax, zmin, zmax})
		case "on":
			reactor = NewReactorAfterTurningOnACuboid(reactor, Cuboid{xmin, xmax, ymin, ymax, zmin, zmax})
		}
	}

	return reactor.Volume()
}

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)

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
