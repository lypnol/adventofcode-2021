use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::env::args;
use std::num::ParseIntError;
use std::str::FromStr;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let cave = Cave::from_str(input).unwrap();
    cave.shortest_path_length((0, 0), (cave.height() - 1, cave.width() - 1))
        .unwrap()
}

const TILING_FACTOR: usize = 5;

struct Cave(Vec<Vec<u8>>);

impl FromStr for Cave {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut cave = Vec::new();
        for line in s.lines() {
            let mut row = Vec::new();
            for c in line.as_bytes().iter().cloned() {
                row.push(c - b'0');
            }
            cave.push(row);
        }
        Ok(Cave(cave))
    }
}

impl Cave {
    fn neighbors(&self, i: usize, j: usize) -> impl Iterator<Item = (usize, usize)> + '_ {
        [
            (i as isize - 1, j as isize),
            (i as isize + 1, j as isize),
            (i as isize, j as isize - 1),
            (i as isize, j as isize + 1),
        ]
        .into_iter()
        .filter_map(move |(x, y)| {
            if x >= 0 && y >= 0 && (x as usize) < self.height() && (y as usize) < self.width() {
                Some((x as usize, y as usize))
            } else {
                None
            }
        })
    }

    fn value(&self, i: usize, j: usize) -> u8 {
        let original_height = self.0.len();
        let original_width = self.0[0].len();
        ((self.0[i % original_height][j % original_width] as usize
            + i / original_height
            + j / original_width
            - 1)
            % 9
            + 1) as u8
    }

    fn height(&self) -> usize {
        self.0.len() * TILING_FACTOR
    }

    fn width(&self) -> usize {
        self.0[0].len() * TILING_FACTOR
    }

    fn shortest_path_length(&self, start: (usize, usize), end: (usize, usize)) -> Option<usize> {
        // Shortest Path Length using A* with the Manhattan distance as heuristic
        let (height, width) = (self.height(), self.width());
        let mut heap = BinaryHeap::new();
        let mut visited = vec![false; height * width];
        let mut best_low_bound_by_node = vec![usize::MAX; height * width];

        heap.push((Reverse(manhattan_distance(start, end)), start, 0));
        while let Some((_, node, dist)) = heap.pop() {
            if node == end {
                return Some(dist);
            }

            let (i, j) = node;
            if visited[i * width + j] {
                continue;
            }
            visited[i * width + j] = true;

            for neighbor in self.neighbors(i, j) {
                let (ni, nj) = neighbor;
                let neighbor_dist = dist + self.value(ni, nj) as usize;
                let low_bound = neighbor_dist + manhattan_distance(neighbor, end);
                let cur_low_bound = best_low_bound_by_node[ni * width + nj];
                if low_bound < cur_low_bound {
                    heap.push((Reverse(low_bound), neighbor, neighbor_dist));
                    best_low_bound_by_node[ni * width + nj] = low_bound;
                }
            }
        }
        None
    }
}

fn manhattan_distance(p1: (usize, usize), p2: (usize, usize)) -> usize {
    ((p1.0 as isize - p2.0 as isize).abs() + (p1.1 as isize - p2.1 as isize).abs()) as usize
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"),
            315
        )
    }
}
