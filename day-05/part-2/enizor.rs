#![feature(int_abs_diff)]
use std::env::args;
use std::fmt::{self, Write};
use std::ops::{Index, IndexMut};
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

type Coord = u16;
/// Always set (x1, y1) < (x2, y2)
#[derive(Debug, Clone, Copy)]
struct Line {
    x1: Coord,
    y1: Coord,
    x2: Coord,
    y2: Coord,
}

impl Line {
    fn from_str(s: &str) -> Self {
        let mut splits = s.split(|c| c == ',' || c == ' ');
        let x1: Coord = splits.next().unwrap().parse().unwrap();
        let y1: Coord = splits.next().unwrap().parse().unwrap();
        let _ = splits.next();
        let x2: Coord = splits.next().unwrap().parse().unwrap();
        let y2: Coord = splits.next().unwrap().parse().unwrap();
        if x1 == x2 || y1 == y2 {
            Self {
                x1: x1.min(x2),
                y1: y1.min(y2),
                x2: x1.max(x2),
                y2: y1.max(y2),
            }
        } else if x1 < x2 {
            Self { x1, y1, x2, y2 }
        } else {
            Self {
                x1: x2,
                y1: y2,
                x2: x1,
                y2: y1,
            }
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum GridPoint {
    Empty,
    Drawn,
    Overlap,
}

const SIZE: usize = 1024;
struct Grid {
    plane: Vec<GridPoint>,
    count: usize,
}

impl Grid {
    fn insert_line(&mut self, line: Line) {
        if line.x1 == line.x2 {
            for i in line.y1..=line.y2 {
                self.insert_point(line.x1, i);
            }
        } else if line.y1 == line.y2 {
            for i in line.x1..=line.x2 {
                self.insert_point(i, line.y1);
            }
        } else if line.y1 < line.y2 {
            for k in 0..=(line.x2 - line.x1) {
                self.insert_point(line.x1 + k, line.y1 + k);
            }
        } else {
            for k in 0..=(line.x2 - line.x1) {
                self.insert_point(line.x1 + k, line.y1 - k);
            }
        }
    }

    fn insert_point(&mut self, x: Coord, y: Coord) {
        match self[(x, y)] {
            GridPoint::Empty => self[(x, y)] = GridPoint::Drawn,
            GridPoint::Drawn => {
                self[(x, y)] = GridPoint::Overlap;
                self.count += 1
            }
            _ => {}
        }
    }
}

impl Default for Grid {
    fn default() -> Self {
        Self {
            plane: vec![GridPoint::Empty; SIZE * SIZE],
            count: 0,
        }
    }
}

impl Index<(Coord, Coord)> for Grid {
    type Output = GridPoint;

    fn index(&self, (x, y): (Coord, Coord)) -> &Self::Output {
        &self.plane[SIZE * (x as usize) + y as usize]
    }
}

impl IndexMut<(Coord, Coord)> for Grid {
    fn index_mut(&mut self, (x, y): (Coord, Coord)) -> &mut Self::Output {
        &mut self.plane[SIZE * (x as usize) + y as usize]
    }
}

impl fmt::Debug for Grid {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut s = String::with_capacity(SIZE + 1);
        f.write_char('\n')?;
        for x in 0..SIZE {
            s.clear();
            for y in 0..SIZE {
                match self[(x as Coord, y as Coord)] {
                    GridPoint::Empty => s.push('.'),
                    GridPoint::Drawn => s.push('X'),
                    GridPoint::Overlap => s.push('#'),
                }
            }
            s.push('\n');
            f.write_str(&s)?;
        }
        Ok(())
    }
}

fn run(input: &str) -> usize {
    let mut grid = Grid::default();
    for l in input.lines() {
        let new_line = Line::from_str(l);
        grid.insert_line(new_line);
    }
    grid.count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";
        assert_eq!(run(input), 12)
    }
}
