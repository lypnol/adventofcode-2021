use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashMap, HashSet};
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
}

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
    fn neighbors(&self, i: usize, j: usize) -> Vec<(usize, usize)> {
        let (i, j) = (i as isize, j as isize);
        return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            .iter()
            .cloned()
            .filter(|(x, y)| {
                *x >= 0 && *y >= 0 && (*x as usize) < self.height() && (*y as usize) < self.width()
            })
            .map(|(x, y)| (x as usize, y as usize))
            .collect::<Vec<(usize, usize)>>();
    }

    fn value(&self, i: usize, j: usize) -> u8 {
        self.0[i][j]
    }

    fn height(&self) -> usize {
        self.0.len()
    }

    fn width(&self) -> usize {
        self.0[0].len()
    }

    fn shortest_path_length(&self, start: (usize, usize), end: (usize, usize)) -> usize {
        let mut heap = BinaryHeap::new();
        let mut visited = HashSet::new();
        let mut best_by_node = HashMap::new();

        heap.push((Reverse(manhattan_distance(start, end)), start, 0));
        while let Some((_, node, dist)) = heap.pop() {
            if node == end {
                return dist;
            }

            if visited.contains(&node) {
                continue;
            }
            visited.insert(node);

            let (i, j) = node;
            for neighbor in self.neighbors(i, j) {
                let neighbor_dist = dist + self.value(neighbor.0, neighbor.1) as usize;
                let neighbor_h = neighbor_dist + manhattan_distance(neighbor, end);
                let h = best_by_node.get(&neighbor);
                if h.is_none() || neighbor_h < *h.unwrap() {
                    heap.push((Reverse(neighbor_h), neighbor, neighbor_dist));
                    best_by_node.insert(neighbor, neighbor_h);
                }
            }
        }
        0
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
            40
        )
    }
}
