package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
	"time"
)

const PAD_DEPTH = 2

func show(image [][]bool) {
	for _, row := range image {
		for _, v := range row {
			if v {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println("")
	}
}

func pad(image [][]bool, border bool) [][]bool {
	pad_top := 0
	for _, v := range image[PAD_DEPTH-1] {
		if v != border {
			pad_top = 1
			break
		}
	}
	pad_bot := 0
	for _, v := range image[len(image)-PAD_DEPTH] {
		if v != border {
			pad_bot = 1
			break
		}
	}
	pad_left := 0
	for _, row := range image {
		if row[PAD_DEPTH-1] != border {
			pad_left = 1
			break
		}
	}
	pad_right := 0
	for _, row := range image {
		if row[len(row)-PAD_DEPTH] != border {
			pad_right = 1
			break
		}
	}
	if pad_top == 0 && pad_bot == 0 && pad_left == 0 && pad_right == 0 {
		return image
	}
	new_image := make([][]bool, 0)
	row_size := len(image[0]) + pad_left + pad_right
	if pad_top == 1 {
		row := make([]bool, row_size)
		for i := 0; i < row_size; i++ {
			row[i] = border
		}
		new_image = append(new_image, row)
	}
	for _, base_row := range image {
		row := make([]bool, row_size)
		if pad_left == 1 {
			row[0] = border
		}
		if pad_right == 1 {
			row[len(row)-1] = border
		}
		for i := pad_left; i < row_size-pad_right; i++ {
			row[i] = base_row[i-pad_left]
		}
		new_image = append(new_image, row)
	}
	if pad_bot == 1 {
		row := make([]bool, row_size)
		for i := 0; i < row_size; i++ {
			row[i] = border
		}
		new_image = append(new_image, row)
	}
	return new_image
}

const ENCODE_SIZE = 9

var ENCODE_VALS = [ENCODE_SIZE]int{256, 128, 64, 32, 16, 8, 4, 2, 1}

var mem_encode = make(map[[ENCODE_SIZE]bool]int)

func encode(im [ENCODE_SIZE]bool) int {
	if v, ok := mem_encode[im]; ok {
		return v
	}
	v := 0
	for i := 0; i < ENCODE_SIZE; i++ {
		if im[i] {
			v += ENCODE_VALS[i]
		}
	}
	mem_encode[im] = v
	return v
}

func conv(image [][]bool, algorithm [ALGO_SIZE]bool, border bool) ([][]bool, bool) {
	var new_border bool
	if border {
		new_border = algorithm[len(algorithm)-1]
	} else {
		new_border = algorithm[0]
	}
	res := make([][]bool, 0)
	nrows := len(image)
	ncols := len(image[0])
	row := make([]bool, ncols)
	for c := 0; c < ncols; c++ {
		row[c] = new_border
	}
	res = append(res, row)
	for r := 1; r < nrows-1; r++ {
		row := make([]bool, ncols)
		row[0] = new_border
		for c := 1; c < ncols-1; c++ {
			im := [ENCODE_SIZE]bool{
				image[r-1][c-1], image[r-1][c], image[r-1][c+1],
				image[r][c-1], image[r][c], image[r][c+1],
				image[r+1][c-1], image[r+1][c], image[r+1][c+1],
			}
			row[c] = algorithm[encode(im)]
		}
		row[ncols-1] = new_border
		res = append(res, row)
	}
	row = make([]bool, ncols)
	for c := 0; c < ncols; c++ {
		row[c] = new_border
	}
	res = append(res, row)
	return res, new_border
}

const ALGO_SIZE = 512

func parse(s string) ([ALGO_SIZE]bool, [][]bool) {
	lines := strings.Split(s, "\n")
	algorithm := [ALGO_SIZE]bool{false}
	for idx, c := range lines[0] {
		if c == '#' {
			algorithm[idx] = true
		}
	}
	image := make([][]bool, 0)
	for _, line := range lines[2:] {
		row := make([]bool, 0)
		for _, char := range strings.TrimSpace(line) {
			row = append(row, char == '#')
		}
		image = append(image, row)
	}
	return algorithm, image
}

const TIMES = 50

func run(s string) int {
	// Your code goes here
	algorithm, image := parse(s)
	border := false
	image = pad(image, border)
	for times := 0; times < TIMES; times++ {
		image = pad(image, border)
		image, border = conv(image, algorithm, border)
	}
	res := 0
	for _, row := range image {
		for _, v := range row {
			if v {
				res += 1
			}
		}
	}
	return res
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
