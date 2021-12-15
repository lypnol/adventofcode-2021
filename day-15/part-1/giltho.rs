use std::collections::HashSet;
use std::env::args;
use std::time::Instant;

#[cfg(test)]
const GRID_SIZE: usize = 10;

#[cfg(not(test))]
const GRID_SIZE: usize = 100;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = unsafe { run(input) };
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Graph {
    graph: [usize; GRID_SIZE * GRID_SIZE],
    distances: [usize; GRID_SIZE * GRID_SIZE],
    visited: [bool; GRID_SIZE * GRID_SIZE],
    max_visited: usize,
    nexts: HashSet<usize>,
}

impl Graph {
    fn visited(&self, x: usize) -> bool {
        self.visited[x]
    }

    fn mark_visited(&mut self, x: usize) {
        self.visited[x] = true;
        self.max_visited = std::cmp::max(self.max_visited, x);
    }

    fn next(&mut self) -> usize {
        let mut min_dist = usize::MAX;
        let mut next_node = 0;
        for i in &self.nexts {
            if !self.visited(*i) && self.distances[*i] < min_dist {
                min_dist = self.distances[*i];
                next_node = *i;
            }
        }
        self.nexts.remove(&next_node);
        next_node
    }

    fn unvisited_neighbours(&self, x: usize) -> Vec<usize> {
        let mut ret = Vec::with_capacity(4);
        if x > GRID_SIZE && !self.visited(x - GRID_SIZE) {
            ret.push(x - GRID_SIZE);
        }
        if x < GRID_SIZE * (GRID_SIZE - 1) && !self.visited(x + GRID_SIZE) {
            ret.push(x + GRID_SIZE);
        }
        if x % GRID_SIZE > 0 && !self.visited(x - 1) {
            ret.push(x - 1);
        }
        if x % GRID_SIZE < GRID_SIZE - 1 && !self.visited(x + 1) {
            ret.push(x + 1);
        }
        ret
    }

    fn actual_graph(&self, x: usize) -> usize {
        self.graph[x]
    }

    #[inline]
    fn is_dest(&self, x: usize) -> bool {
        x == GRID_SIZE * GRID_SIZE - 1
    }

    fn dijkstra(mut self) -> usize {
        loop {
            let current = self.next();
            for n in self.unvisited_neighbours(current) {
                let new_dist = self.actual_graph(n) + self.distances[current];
                if new_dist < self.distances[n] {
                    self.distances[n] = new_dist;
                    self.nexts.insert(n);
                }
            }
            self.mark_visited(current);
            if self.is_dest(current) {
                break;
            }
        }
        self.distances[GRID_SIZE * GRID_SIZE - 1]
    }

    fn from_input(input: &[u8]) -> Self {
        let mut distances = [usize::MAX; GRID_SIZE * GRID_SIZE];
        let mut graph = [0; GRID_SIZE * GRID_SIZE];
        let mut idx = 0;
        for i in input {
            match i {
                b'\n' => (),
                c => {
                    graph[idx] = (c - b'0') as usize;
                    idx += 1;
                }
            }
        }
        let mut nexts = HashSet::with_capacity(50);
        distances[0] = 0;
        nexts.insert(0);
        Self {
            distances,
            graph,
            max_visited: 0,
            visited: [false; GRID_SIZE * GRID_SIZE],
            nexts,
        }
    }
}

unsafe fn run(input: &[u8]) -> usize {
    Graph::from_input(input).dijkstra()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            unsafe {
                run("1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"
                    .as_bytes())
            },
            40
        )
    }
}
