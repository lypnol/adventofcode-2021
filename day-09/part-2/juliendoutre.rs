use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const WIDTH: usize = 100;

fn run(input: &str) -> u32 {
    let mut map = [u32::MAX; WIDTH * WIDTH];
    let mut score = 0;

    for (i, line) in input.lines().enumerate() {
        for (j, n) in line.chars().enumerate() {
            map[i * WIDTH + j] = n.to_digit(10).unwrap();
        }
    }

    for idx in 0..(WIDTH * WIDTH) {
        let mut smallest_neighbour = u32::MAX;

        if idx % WIDTH > 0 && map[idx - 1] < smallest_neighbour {
            smallest_neighbour = map[idx - 1];
        }

        if idx % WIDTH < WIDTH - 1 && map[idx + 1] < smallest_neighbour {
            smallest_neighbour = map[idx + 1];
        }

        if idx >= WIDTH && map[idx - WIDTH] < smallest_neighbour {
            smallest_neighbour = map[idx - WIDTH];
        }

        if idx < WIDTH * (WIDTH - 1) && map[idx + WIDTH] < smallest_neighbour {
            smallest_neighbour = map[idx + WIDTH];
        }

        if map[idx] < smallest_neighbour {
            let mut size = 1;

            // TODO: compute basin size

            score *= size;
        }
    }

    score
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "2199943210
3987894921
9856789892
8767896789
9899965678";

        assert_eq!(run(test_case), 1134)
    }
}
