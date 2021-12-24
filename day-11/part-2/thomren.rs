use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const SIZE: usize = 10;

fn run(input: &str) -> usize {
    let mut octopuses: [u8; SIZE * SIZE] = [0; SIZE * SIZE];
    let input_bytes = input.as_bytes();
    for i in 0..(SIZE * SIZE) {
        octopuses[i] = input_bytes[i + i / SIZE] - b'0';
    }

    let mut n_flashes;
    let mut flash_stack = vec![];
    let mut step = 0;
    loop {
        flash_stack.clear();
        n_flashes = 0;

        for x in 0..octopuses.len() {
            octopuses[x] += 1;
            if octopuses[x] == 10 {
                flash_stack.push((x / SIZE, x % SIZE));
            }
        }

        while let Some((i, j)) = flash_stack.pop() {
            octopuses[i * SIZE + j] = 0;
            n_flashes += 1;
            for (x, y) in neighbors(i, j) {
                if octopuses[x * SIZE + y] > 0 {
                    octopuses[x * SIZE + y] += 1
                }
                if octopuses[x * SIZE + y] == 10 {
                    flash_stack.push((x, y))
                }
            }
        }

        step += 1;
        if n_flashes == SIZE * SIZE {
            return step;
        }
    }
}

fn neighbors(i: usize, j: usize) -> impl Iterator<Item = (usize, usize)> {
    let (i, j) = (i as isize, j as isize);
    [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
        (i - 1, j + 1),
        (i - 1, j - 1),
        (i + 1, j + 1),
        (i + 1, j - 1),
    ]
    .into_iter()
    .filter_map(move |(x, y)| {
        if x >= 0 && y >= 0 && (x as usize) < SIZE && (y as usize) < SIZE {
            Some((x as usize, y as usize))
        } else {
            None
        }
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"),
            195
        )
    }
}
