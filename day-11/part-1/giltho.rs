#![allow(clippy::manual_range_contains)]

use std::collections::VecDeque;
use std::env::args;
use std::fmt::Display;
use std::time::Instant;

// Inputs are squares of 10 x 10
const SIZE: usize = 10;

struct Grid {
    data: [u8; 100],
    queue: VecDeque<usize>,
    flash_count: u32,
    flashed: u128,
}

impl Display for Grid {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for i in 0..SIZE {
            for j in 0..SIZE {
                write!(f, "{}", self.data[i * SIZE + j])?;
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

impl Grid {
    fn new(input: &[u8]) -> Self {
        let mut arr = [0; SIZE * SIZE];
        let mut idx = 0;
        for c in input {
            if let b'\n' = c {
                continue;
            }
            arr[idx] = c - 48;
            idx += 1;
        }
        Self {
            data: arr,
            queue: VecDeque::with_capacity(SIZE * SIZE),
            flash_count: 0,
            flashed: 0,
        }
    }

    // Only safe is called within the bounds
    unsafe fn flash(&mut self, idx: usize) {
        self.flash_count += 1;

        self.flashed |= 1 << idx;
        *self.data.get_unchecked_mut(idx) = 0;
        if idx >= SIZE {
            self.queue.push_back(idx - SIZE);
            if idx % SIZE > 0 {
                self.queue.push_back(idx - SIZE - 1)
            }
            if idx % SIZE < SIZE - 1 {
                self.queue.push_back(idx - SIZE + 1)
            }
        }
        if idx < SIZE * (SIZE - 1) {
            self.queue.push_back(idx + SIZE);

            if idx % SIZE > 0 {
                self.queue.push_back(idx + SIZE - 1)
            }
            if idx % SIZE < SIZE - 1 {
                self.queue.push_back(idx + SIZE + 1)
            }
        }
        if idx % SIZE > 0 {
            self.queue.push_back(idx - 1)
        }
        if idx % SIZE < SIZE - 1 {
            self.queue.push_back(idx + 1)
        }
    }

    unsafe fn add_one(&mut self, idx: usize) {
        let c = self.data.get_unchecked_mut(idx);
        *c += 1;
        if *c == 10 {
            self.flash(idx);
        }
    }

    unsafe fn reset_octos(&mut self) {
        let mut mask = 1;
        for i in 0..(SIZE * SIZE) {
            if (self.flashed & mask) > 0 {
                *self.data.get_unchecked_mut(i) = 0;
            }
            mask <<= 1
        }
        self.flashed = 0;
    }

    fn run(mut self, rounds: u32) -> u32 {
        for _ in 0..rounds {
            unsafe {
                // increment everything
                for i in 0..(SIZE * SIZE) {
                    self.add_one(i);
                }
                // flashes
                while !self.queue.is_empty() {
                    let next = self.queue.pop_front().unwrap();
                    self.add_one(next);
                }
                self.reset_octos()
            };
        }
        self.flash_count
    }
}

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &[u8]) -> u32 {
    Grid::new(input).run(100)
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
5283751526"
                .as_bytes()),
            1656
        )
    }
}
