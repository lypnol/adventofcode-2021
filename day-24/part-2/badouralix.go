package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

const ModelNumberLength = 14

// Monad struct assumes the input monad is following the pattern in https://gist.github.com/badouralix/63539b1a15d0026836362251271193a6
//
//      0    inp w
//      1    mul x 0
//      2    add x z
//      3    mod x 26
//      4    div z <OperandsDiv>
//      5    add x <OperandsSub>
//      6    eql x w
//      7    eql x 0
//      8    mul y 0
//      9    add y 25
//     10    mul y x
//     11    add y 1
//     12    mul z y
//     13    mul y 0
//     14    add y w
//     15    add y <OperandsAdd>
//     16    mul y x
//     17    add z y
//
// As such, each iteration i updates z such that :
//
//     z =                            z / OperandsDiv[i]     if (z % 26 == w - OperandsSub[i])
//     z = 26*(z / OperandsDiv[i]) + (w + OperandsAdd[i])    otherwise
//
type Monad struct {
	OperandsAdd []int
	OperandsDiv []int
	OperandsSub []int
	Raw         string
}

// NewMonad returns a parsed structure for s, with a lot of assumptions on the index of each instruction
func NewMonad(s string) Monad {
	lines := strings.Split(s, "\n")

	operandsAdd := make([]int, 0, ModelNumberLength)
	operandsDiv := make([]int, 0, ModelNumberLength)
	operandsSub := make([]int, 0, ModelNumberLength)

	for i := 0; i < ModelNumberLength; i++ {
		operandAdd, _ := strconv.Atoi(lines[i*18+15][6:])
		operandsAdd = append(operandsAdd, operandAdd)

		operandDiv, _ := strconv.Atoi(lines[i*18+4][6:])
		operandsDiv = append(operandsDiv, operandDiv)

		operandSub, _ := strconv.Atoi(lines[i*18+5][6:])
		operandsSub = append(operandsSub, operandSub)
	}

	return Monad{
		OperandsAdd: operandsAdd,
		OperandsDiv: operandsDiv,
		OperandsSub: operandsSub,
		Raw:         s,
	}
}

// Solve is the entrypoint of the MONAD solver, doing nothing but calling SolveRec
func (m Monad) Solve() int {
	solution := make([]int, 0, ModelNumberLength)
	solution, _ = m.SolveRec(solution, make([]int, 0, ModelNumberLength))

	result := 0
	for _, v := range solution {
		result = 10*result + v
	}

	return result
}

// SolveRec contains the actual solver logic
func (m Monad) SolveRec(current []int, z []int) ([]int, bool) {
	// Fetch recursion depth from the current state
	i := len(current)

	// Handle base case of the recursion
	if i == ModelNumberLength {
		return current, len(z) == 0
	}

	// Cut the branch early if we know that we cannot get z to 0 in time
	if ModelNumberLength-i < len(z) {
		return current, false
	}

	// Get z0 as in z = z0 * 26^0 + z1 * 26^1 + z2 * 26^2 + z3 * 26^3 + ...
	// By construction, z0 is the last element of z
	z0 := 0
	if len(z) != 0 {
		z0 = z[len(z)-1]
	}

	// Try all possible inputs recursively
	for w := 1; w <= 9; w++ {
		// As per the input, m.OperandsDiv[i] is either 1 or 26
		// By construction, z / 26 is z shifted right
		if m.OperandsDiv[i] == 26 && len(z) != 0 {
			z = z[:len(z)-1]
		}

		if z0 == w-m.OperandsSub[i] {
			new := append(current, w)
			new, valid := m.SolveRec(new, z)
			// If the recursive call returned a valid solution, stop the recursion right now
			if valid {
				return new, true
			}
		} else {
			new := append(current, w)
			// As per the input, we have 0 < w+m.OperandsAdd[i] < 26 and the complex operation becomes an append
			z = append(z, w+m.OperandsAdd[i])
			new, valid := m.SolveRec(new, z)
			// If the recursive call returned a valid solution, stop the recursion right now
			if valid {
				return new, true
			}
			// Revert change on z
			z = z[:len(z)-1]
		}

		// Revert change on z, making sure we don't introduce leading zeros
		if m.OperandsDiv[i] == 26 && (len(z) != 0 || z0 != 0) {
			z = append(z, z0)
		}
	}

	// At this point we found no further w, which means the current branch should be backtracked
	return current, false
}

// String implements fmt.Stringer interface for Monad
func (m Monad) String() (output string) {
	blocks := 2 // Must be a divisor ModelNumberLength
	lines := strings.Split(m.Raw, "\n")

	for i := 0; i <= blocks; i++ {
		for j := 0; j < 18; j++ {
			for k := (ModelNumberLength / blocks) * i; k < (ModelNumberLength/blocks)*(i+1); k++ {
				output += fmt.Sprintf("%-9s\t", lines[k*18+j])
			}
			output += "\n"
		}

		output += "\n"
	}

	return output
}

func run(s string) int {
	// Your code goes here
	return NewMonad(s).Solve()
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
