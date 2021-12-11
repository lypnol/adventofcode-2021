use std::env::args;
use std::ops::{Index, IndexMut};
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut grid = Grid::new();
    for (i, l) in input.lines().enumerate() {
        for (j, b) in l.as_bytes().iter().enumerate() {
            grid[(i, j)] = b - b'0';
        }
    }
    let mut res = 0;
    for _ in 0..NB_ITER {
        res += grid.step();
    }
    res
}

const GRID_SIZE: usize = 10;
const MASK: u8 = 0x7f;
const NB_ITER: usize = 100;

struct Grid {
    grid: [u8; GRID_SIZE * GRID_SIZE],
    blinks: Vec<(usize, usize)>,
}

impl Index<(usize, usize)> for Grid {
    type Output = u8;
    fn index(&self, (x, y): (usize, usize)) -> &Self::Output {
        &self.grid[x * GRID_SIZE + y]
    }
}

impl IndexMut<(usize, usize)> for Grid {
    fn index_mut(&mut self, (x, y): (usize, usize)) -> &mut Self::Output {
        &mut self.grid[x * GRID_SIZE + y]
    }
}

impl Grid {
    fn new() -> Self {
        Self {
            grid: [0u8; GRID_SIZE * GRID_SIZE],
            blinks: Vec::with_capacity(GRID_SIZE * GRID_SIZE / 4),
        }
    }

    fn step(&mut self) -> usize {
        self.blinks.clear();
        let mut count = 0;
        for i in 0..GRID_SIZE {
            for j in 0..GRID_SIZE {
                self[(i, j)] &= MASK;
                self[(i, j)] += 1;
                if self[(i, j)] > 9 {
                    self[(i, j)] = !MASK;
                    self.blinks.push((i, j));
                }
            }
        }
        while let Some((i, j)) = self.blinks.pop() {
            count += 1;
            for (x, y) in Neighbours::new(i, j) {
                if self[(x, y)] & !MASK == 0 {
                    self[(x, y)] += 1;
                    if self[(x, y)] > 9 {
                        self[(x, y)] = !MASK;
                        self.blinks.push((x, y));
                    }
                }
            }
        }
        count
    }
}

struct Neighbours {
    x: isize,
    y: isize,
    step: isize,
}
impl Neighbours {
    fn new(x: usize, y: usize) -> Self {
        Self {
            x: x as isize,
            y: y as isize,
            step: 4,
        }
    }
}

impl Iterator for Neighbours {
    type Item = (usize, usize);

    fn next(&mut self) -> Option<Self::Item> {
        while self.step < 13 {
            self.step += 1;
            let x1 = self.x + self.step % 3 - 1;
            let y1 = self.y + (self.step / 3) % 3 - 1;
            if x1 >= 0 && y1 >= 0 && x1 < GRID_SIZE as isize && y1 < GRID_SIZE as isize {
                return Some((x1 as usize, y1 as usize));
            }
        }
        None
    }
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
            1656
        )
    }
}
