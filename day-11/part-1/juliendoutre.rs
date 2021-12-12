use std::env::args;
use std::time::Instant;

const WIDTH: usize = 10;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 100);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str, step: usize) -> usize {
    let mut map: [u8; WIDTH * WIDTH] = [0; WIDTH * WIDTH];

    input.lines().enumerate().for_each(|(i, line)| {
        line.as_bytes()
            .iter()
            .enumerate()
            .for_each(|(j, b)| map[i * WIDTH + j] = b - 48)
    });

    let mut flashes = 0;

    for _ in 0..step {
        let mut flashed: [bool; WIDTH * WIDTH] = [false; WIDTH * WIDTH];

        for i in 0..(WIDTH * WIDTH) {
            map[i] += 1;
        }

        while flash(&mut map, &mut flashed, &mut flashes) > 0 {}
    }

    flashes
}

fn flash(
    map: &mut [u8; WIDTH * WIDTH],
    flashed: &mut [bool; WIDTH * WIDTH],
    flashes: &mut usize,
) -> usize {
    let mut count = 0;

    for i in 0..(WIDTH * WIDTH) {
        if map[i] > 9 {
            *flashes += 1;
            map[i] = 0;
            flashed[i] = true;

            if i >= WIDTH && i % WIDTH > 0 {
                if !flashed[i - WIDTH - 1] {
                    map[i - WIDTH - 1] += 1;
                    if map[i - WIDTH - 1] > 9 {
                        count += 1;
                    }
                }
            }

            if i >= WIDTH {
                if !flashed[i - WIDTH] {
                    map[i - WIDTH] += 1;
                    if map[i - WIDTH] > 9 {
                        count += 1;
                    }
                }
            }

            if i >= WIDTH && i % WIDTH < WIDTH - 1 {
                if !flashed[i - WIDTH + 1] {
                    map[i - WIDTH + 1] += 1;
                    if map[i - WIDTH + 1] > 9 {
                        count += 1;
                    }
                }
            }

            if i % WIDTH > 0 {
                if !flashed[i - 1] {
                    map[i - 1] += 1;
                    if map[i - 1] > 9 {
                        count += 1;
                    }
                }
            }

            if i % WIDTH < WIDTH - 1 {
                if !flashed[i + 1] {
                    map[i + 1] += 1;
                    if map[i + 1] > 9 {
                        count += 1;
                    }
                }
            }

            if i < WIDTH * (WIDTH - 1) && i % WIDTH > 0 {
                if !flashed[i + WIDTH - 1] {
                    map[i + WIDTH - 1] += 1;
                    if map[i + WIDTH - 1] > 9 {
                        count += 1;
                    }
                }
            }

            if i < WIDTH * (WIDTH - 1) {
                if !flashed[i + WIDTH] {
                    map[i + WIDTH] += 1;
                    if map[i + WIDTH] > 9 {
                        count += 1;
                    }
                }
            }

            if i < WIDTH * (WIDTH - 1) && i % WIDTH < WIDTH - 1 {
                if !flashed[i + WIDTH + 1] {
                    map[i + WIDTH + 1] += 1;
                    if map[i + WIDTH + 1] > 9 {
                        count += 1;
                    }
                }
            }
        }
    }

    count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526";

        assert_eq!(run(test_case, 100), 1656)
    }
}
