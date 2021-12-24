package main

import (
	"container/heap"
	"errors"
	"fmt"
	"io/ioutil"
	"math"
	"os"
	"time"
)

var EnergyPerStep = map[byte]int{
	'A': 1,
	'B': 10,
	'C': 100,
	'D': 1000,
}

// Burrow represents the state of the burrow with regards to the location of each amphipod
//
//           #########################
// Hallway = # 0 1 . 2 . 3 . 4 . 5 6 #
//           ##### 0 # 0 # 0 # 0 #####
//               # 1 # 1 # 1 # 1 #
//               # 2 # 2 # 2 # 2 #
//               # 3 # 3 # 3 # 3 #
//               #################
// Rooms   =       A   B   C   D
//
type Burrow struct {
	Hallway     [7]byte
	Rooms       map[byte][4]byte
	TotalEnergy int

	hash  *string
	index *int
	str   *string
}

func NewBurrowFromString(s string) *Burrow {
	hallway := [7]byte{}
	for space := range hallway {
		hallway[space] = '.'
	}

	rooms := make(map[byte][4]byte)
	for _, room := range []byte{'A', 'B', 'C', 'D'} {
		rooms[room] = [4]byte{
			s[2*14+0*12+2*(int(room-'A'))+3],
			s[3*14+0*12+2*(int(room-'A'))+3],
			s[3*14+1*12+2*(int(room-'A'))+3],
			s[3*14+2*12+2*(int(room-'A'))+3],
		}
	}

	return &Burrow{
		Hallway:     hallway,
		Rooms:       rooms,
		TotalEnergy: math.MaxInt64,

		hash:  nil,
		index: nil,
		str:   nil,
	}
}

func (b Burrow) CopyForUpdate() *Burrow {
	// Hallway copy works because it is an array and not a slice
	hallway := b.Hallway

	// Single room copy works for the same reason
	rooms := make(map[byte][4]byte)
	for k, v := range b.Rooms {
		rooms[k] = v
	}

	return &Burrow{
		Hallway:     hallway,
		Rooms:       rooms,
		TotalEnergy: math.MaxInt64,

		// Invalidate cached values to be later edited in place
		hash:  nil,
		index: nil,
		str:   nil,
	}
}

func (b *Burrow) Hash() (output string) {
	if b.hash != nil {
		return *b.hash
	}

	for space := range b.Hallway {
		output += string(b.Hallway[space])
	}

	for _, room := range []byte{'A', 'B', 'C', 'D'} {
		output += string(b.Rooms[room][0])
		output += string(b.Rooms[room][1])
		output += string(b.Rooms[room][2])
		output += string(b.Rooms[room][3])
	}

	b.hash = &output
	return *b.hash
}

func (b Burrow) MoveFromHallwayToRoom(space int, room byte) (*Burrow, int, error) {
	amphipod := b.Hallway[space]
	if amphipod == '.' {
		return nil, 0, errors.New("space in hallway is empty")
	}

	if b.Rooms[room][0] != '.' {
		return nil, 0, errors.New("room has not space left")
	}

	// Black magic to detect non-empty spaces in path
	for i := 2 + int(room-'A'); i < space; i++ {
		if b.Hallway[i] != '.' {
			return nil, 0, errors.New("found non-empty space in path")
		}
	}
	for i := 1 + space; i < 2+int(room-'A'); i++ {
		if b.Hallway[i] != '.' {
			return nil, 0, errors.New("found non-empty space in path")
		}
	}

	// Black magic to compute the number of steps
	steps := 3 - 2*space + 2*int(room-'A')
	if steps < 0 {
		steps = -steps
	}
	if space == 0 {
		steps = 2 + 2*int(room-'A')
	}
	if space == 6 {
		steps = 8 - 2*int(room-'A')
	}
	steps += 1
	// This piece of black magic is a bit different from MoveFromRoomToHallway
	if b.Rooms[room][1] == '.' {
		steps += 1
	}
	if b.Rooms[room][2] == '.' {
		steps += 1
	}
	if b.Rooms[room][3] == '.' {
		steps += 1
	}

	energy := steps * EnergyPerStep[amphipod]

	burrow := b.CopyForUpdate()
	burrow.Hallway[space] = '.'
	if b.Rooms[room][3] == '.' {
		burrow.Rooms[room] = [4]byte{'.', '.', '.', amphipod}
	} else if b.Rooms[room][2] == '.' {
		burrow.Rooms[room] = [4]byte{'.', '.', amphipod, b.Rooms[room][3]}
	} else if b.Rooms[room][1] == '.' {
		burrow.Rooms[room] = [4]byte{'.', amphipod, b.Rooms[room][2], b.Rooms[room][3]}
	} else {
		burrow.Rooms[room] = [4]byte{amphipod, b.Rooms[room][1], b.Rooms[room][2], b.Rooms[room][3]}
	}

	return burrow, energy, nil
}

func (b Burrow) MoveFromRoomToHallway(room byte, space int) (*Burrow, int, error) {
	amphipod := b.Rooms[room][3]
	if b.Rooms[room][2] != '.' {
		amphipod = b.Rooms[room][2]
	}
	if b.Rooms[room][1] != '.' {
		amphipod = b.Rooms[room][1]
	}
	if b.Rooms[room][0] != '.' {
		amphipod = b.Rooms[room][0]
	}
	if amphipod == '.' {
		return nil, 0, errors.New("room is empty")
	}

	if b.Hallway[space] != '.' {
		return nil, 0, errors.New("space in hallway is already occupied")
	}

	// Black magic to detect non-empty spaces in path
	for i := 2 + int(room-'A'); i < space; i++ {
		if b.Hallway[i] != '.' {
			return nil, 0, errors.New("found non-empty space in path")
		}
	}
	for i := 1 + space; i < 2+int(room-'A'); i++ {
		if b.Hallway[i] != '.' {
			return nil, 0, errors.New("found non-empty space in path")
		}
	}

	// Black magic to compute the number of steps
	steps := 3 - 2*space + 2*int(room-'A')
	if steps < 0 {
		steps = -steps
	}
	if space == 0 {
		steps = 2 + 2*int(room-'A')
	}
	if space == 6 {
		steps = 8 - 2*int(room-'A')
	}
	steps += 1
	// This piece of black magic is a bit different from MoveFromHallwayToRoom
	if b.Rooms[room][2] == '.' {
		steps += 1
	}
	if b.Rooms[room][1] == '.' {
		steps += 1
	}
	if b.Rooms[room][0] == '.' {
		steps += 1
	}

	energy := steps * EnergyPerStep[amphipod]

	burrow := b.CopyForUpdate()
	burrow.Hallway[space] = amphipod
	if b.Rooms[room][2] == '.' {
		burrow.Rooms[room] = [4]byte{'.', '.', '.', '.'}
	} else if b.Rooms[room][1] == '.' {
		burrow.Rooms[room] = [4]byte{'.', '.', '.', b.Rooms[room][3]}
	} else if b.Rooms[room][0] == '.' {
		burrow.Rooms[room] = [4]byte{'.', '.', b.Rooms[room][2], b.Rooms[room][3]}
	} else {
		burrow.Rooms[room] = [4]byte{'.', b.Rooms[room][1], b.Rooms[room][2], b.Rooms[room][3]}
	}

	return burrow, energy, nil
}

func (b *Burrow) String() (output string) {
	if b.str != nil {
		return *b.str
	}

	output += "#############\n"
	output += "#"
	output += string(b.Hallway[0])
	output += string(b.Hallway[1])
	output += "."
	output += string(b.Hallway[2])
	output += "."
	output += string(b.Hallway[3])
	output += "."
	output += string(b.Hallway[4])
	output += "."
	output += string(b.Hallway[5])
	output += string(b.Hallway[6])
	output += "#\n"
	output += "###"
	for _, room := range []byte{'A', 'B', 'C', 'D'} {
		output += string(b.Rooms[room][0])
		output += "#"
	}
	output += "##\n"
	output += "  #"
	for _, room := range []byte{'A', 'B', 'C', 'D'} {
		output += string(b.Rooms[room][1])
		output += "#"
	}
	output += "\n"
	output += "  #"
	for _, room := range []byte{'A', 'B', 'C', 'D'} {
		output += string(b.Rooms[room][2])
		output += "#"
	}
	output += "\n"
	output += "  #"
	for _, room := range []byte{'A', 'B', 'C', 'D'} {
		output += string(b.Rooms[room][3])
		output += "#"
	}
	output += "\n"
	output += "  #########"

	b.str = &output
	return *b.str
}

type PriorityQueue []*Burrow

func NewPriorityQueue() PriorityQueue {
	return make(PriorityQueue, 0, 50_000)
}

func (pq PriorityQueue) Len() int {
	return len(pq)
}

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].TotalEnergy < pq[j].TotalEnergy
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	*pq[i].index = i
	*pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	b := x.(*Burrow)
	b.index = &n
	*pq = append(*pq, b)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	b := old[n-1]
	old[n-1] = nil
	b.index = nil
	*pq = old[0 : n-1]
	return b
}

func run(s string) int {
	// Your code goes here
	pq := NewPriorityQueue()
	heap.Init(&pq)

	start := NewBurrowFromString(s[0:3*14] + "  #D#C#B#A#\n" + "  #D#B#A#C#\n" + s[3*14:])
	start.TotalEnergy = 0
	pq.Push(start)

	// costs gives the least total energy to go from the initial burrow to the given burrow
	cache := map[string]*Burrow{}
	cache[start.Hash()] = start

	for pq.Len() > 0 {
		src := heap.Pop(&pq).(*Burrow)
		for room := range src.Rooms {
			if src.Rooms[room][0] == room && src.Rooms[room][1] == room && src.Rooms[room][2] == room && src.Rooms[room][3] == room {
				continue
			}

			for space := range src.Hallway {
				if src.Hallway[space] == room {
					skip := false
					for _, v := range src.Rooms[room] {
						skip = skip || (v != room && v != '.')
					}
					if skip {
						continue
					}

					dst, cost, err := src.MoveFromHallwayToRoom(space, room)
					if err == nil {
						if _, ok := cache[dst.Hash()]; !ok {
							cache[dst.Hash()] = dst
						}

						if src.TotalEnergy+cost < cache[dst.Hash()].TotalEnergy {
							cache[dst.Hash()].TotalEnergy = src.TotalEnergy + cost

							if cache[dst.Hash()].index == nil {
								heap.Push(&pq, dst)
							} else {
								heap.Fix(&pq, *cache[dst.Hash()].index)
							}
						}
					}
				}

				skip := true
				for _, v := range src.Rooms[room] {
					skip = skip && (v == room || v == '.')
				}
				if skip {
					continue
				}

				dst, cost, err := src.MoveFromRoomToHallway(room, space)
				if err == nil {
					if _, ok := cache[dst.Hash()]; !ok {
						cache[dst.Hash()] = dst
					}

					if src.TotalEnergy+cost < cache[dst.Hash()].TotalEnergy {
						cache[dst.Hash()].TotalEnergy = src.TotalEnergy + cost

						if cache[dst.Hash()].index == nil {
							heap.Push(&pq, dst)
						} else {
							heap.Fix(&pq, *cache[dst.Hash()].index)
						}
					}
				}
			}
		}
	}

	return cache[".......AAAABBBBCCCCDDDD"].TotalEnergy
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
