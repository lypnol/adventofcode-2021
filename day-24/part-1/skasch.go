package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"runtime/pprof"
	"strconv"
	"strings"
	"time"
)

type binaryOp = int
type unaryOp = int
type memory = int

const (
	add binaryOp = iota
	mul
	div
	mod
	eql
	inp unaryOp = iota
)

type instruction interface{}

type unaryInstruction struct {
	operation unaryOp
	arg1      memory
}

type binaryInstructionMemory struct {
	operation binaryOp
	arg1      memory
	arg2      memory
}

type binaryInstructionConst struct {
	operation binaryOp
	arg1      memory
	arg2      int
}

type interval struct {
	min, max int
}

func getMinMax(op binaryOp, left, right interval) interval {
	switch op {
	case add:
		return interval{left.min + right.min, left.max + right.max}
	case mul:
		min := left.min * right.min
		max := min
		for _, val := range []int{left.min * right.max, left.max * right.min, left.max * right.max} {
			if val < min {
				min = val
			} else if val > max {
				max = val
			}
		}
		return interval{min, max}
	case div:
		if right.min == right.max {
			min := left.min / right.min
			max := min
			other := left.max / right.min
			if other < min {
				min = other
			} else if max < other {
				max = other
			}
			if left.min < 0 && 0 < left.max {
				if min > 0 {
					min = 0
				} else if max < 0 {
					max = 0
				}
			}
			return interval{min, max}
		}
		min := left.min / right.min
		max := min
		for _, val := range []int{left.min / right.max, left.max / right.min, left.max / right.max} {
			if val < min {
				min = val
			} else if val > max {
				max = val
			}
		}
		if left.min < 0 && 0 < left.max {
			if min > 0 {
				min = 0
			} else if max < 0 {
				max = 0
			}
		}
		return interval{min, max}
	case mod:
		if right.min == right.max {
			if left.max-left.min >= right.min {
				return interval{0, right.min - 1}
			}
			modmin := left.min % right.min
			modmax := left.max % right.min
			if modmin <= modmax {
				return interval{modmin, modmax}
			}
			return interval{0, right.min - 1}
		}
		min := left.min % right.max
		max := min
		for modValue := right.max; modValue >= right.min; modValue-- {
			for value := left.min; value <= left.max && value < left.min+modValue; value++ {
				v := value % modValue
				if v < min {
					min = v
				} else if v > max {
					max = v
				}
			}
			if min == 0 && max >= modValue-1 {
				break
			}
		}
		return interval{min, max}
	case eql:
		if left.min == left.max && left.max == right.min && right.min == right.max {
			return interval{1, 1}
		}
		var leftMax, rightMin int
		if left.min < right.min {
			leftMax = left.max
			rightMin = right.min
		} else {
			leftMax = right.max
			rightMin = left.min
		}
		if rightMin <= leftMax {
			return interval{0, 1}
		}
		return interval{0, 0}
	}
	panic("Invalid binary operator")
}

const minVal = 1
const maxVal = 9

func evaluate(instructions []instruction, input []int) interval {
	state := []interval{
		{0, 0},
		{0, 0},
		{0, 0},
		{0, 0},
	}
	idx := 0
	for _, instruction := range instructions {
		switch instruction.(type) {
		case unaryInstruction:
			instr := instruction.(unaryInstruction)
			switch instr.operation {
			case inp:
				if idx < len(input) {
					state[instr.arg1] = interval{input[idx], input[idx]}
				} else {
					state[instr.arg1] = interval{minVal, maxVal}
				}
				idx++
				continue
			}
			panic("Unhandled operation")
		case binaryInstructionConst:
			instr := instruction.(binaryInstructionConst)
			state[instr.arg1] = getMinMax(instr.operation, state[instr.arg1], interval{instr.arg2, instr.arg2})
			continue
		case binaryInstructionMemory:
			instr := instruction.(binaryInstructionMemory)
			state[instr.arg1] = getMinMax(instr.operation, state[instr.arg1], state[instr.arg2])
			continue
		}
		panic("Unhandled instruction")
	}
	return state[3]
}

func nameToMemory(mem string) memory {
	switch mem {
	case "w":
		return 0
	case "x":
		return 1
	case "y":
		return 2
	case "z":
		return 3
	}
	panic("Invalid memory")
}

func parseLine(s string) instruction {
	args := strings.Split(s, " ")
	var op int
	switch args[0] {
	case "inp":
		op = inp
	case "add":
		op = add
	case "mul":
		op = mul
	case "div":
		op = div
	case "mod":
		op = mod
	case "eql":
		op = eql
	}
	arg1 := args[1]
	if op == inp {
		return unaryInstruction{operation: op, arg1: nameToMemory(arg1)}
	}
	if arg2, ok := strconv.Atoi(args[2]); ok == nil {
		return binaryInstructionConst{operation: op, arg1: nameToMemory(arg1), arg2: arg2}
	} else {
		arg2 := args[2]
		return binaryInstructionMemory{operation: op, arg1: nameToMemory(arg1), arg2: nameToMemory(arg2)}
	}
}

func parse(s string) []instruction {
	lines := strings.Split(s, "\n")
	res := make([]instruction, len(lines))
	for idx, line := range lines {
		res[idx] = parseLine(line)
	}
	return res
}

const from = 9
const to = 1
const delta = -1

func nextBaseInput(input []int, index int) ([]int, int) {
	if index < 0 {
		panic("Invalid index")
	}
	if input[index] == to {
		for idx := index + 1; idx < len(input); idx++ {
			input[idx] = from
		}
		for input[index] == to {
			input[index] = from
			index--
		}
	}
	input[index] += delta
	return input, index
}

func outOfRange(i interval) bool {
	return i.max < 0 || i.min > 0
}

func evalInput(instructions []instruction, input []int) []int {
	index := len(input) - 1
	for index < len(input) {
		intrv := evaluate(instructions, input[:index+1])
		for outOfRange(intrv) {
			input, index = nextBaseInput(input, index)
			intrv = evaluate(instructions, input[:index+1])
		}
		index++
	}
	return input
}

func inputToString(input []int) int {
	strs := make([]string, len(input))
	for idx, d := range input {
		strs[idx] = fmt.Sprintf("%d", d)
	}
	if v, ok := strconv.Atoi(strings.Join(strs, "")); ok == nil {
		return v
	}
	panic("Failed to convert")
}

const inputSize = 14

func run(s string) int {
	// Your code goes here
	instructions := parse(s)
	input := make([]int, inputSize)
	for idx := 0; idx < inputSize; idx++ {
		input[idx] = from
	}
	input = evalInput(instructions, input)
	return inputToString(input)
}

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to `file`")

func main() {
	// Uncomment this line to disable garbage collection
	// debug.SetGCPercent(-1)
	flag.Parse()
	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal("could not create CPU profile: ", err)
		}
		defer f.Close() // error handling omitted for example
		if err := pprof.StartCPUProfile(f); err != nil {
			log.Fatal("could not start CPU profile: ", err)
		}
		defer pprof.StopCPUProfile()
	}

	var input []byte
	var err error
	if len(os.Args) > 1 {
		// Read input from file for local debugging
		input, err = ioutil.ReadFile(os.Args[len(os.Args)-1])
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
