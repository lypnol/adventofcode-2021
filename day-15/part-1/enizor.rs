use std::cmp::Reverse;
use std::collections::BinaryHeap;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u16 {
    let size = input.find('\n').unwrap();
    // remember the current distance to each node
    // MSB determines of the node was previously visited
    let mut distances = vec![!VISITED_MASK; size * size];
    // starting point has distance 0 (and stays unvisited)
    distances[0] = 0;
    // priority queue of (best distance, x, y)
    let mut heap = BinaryHeap::new();
    // std heap is a max-heap, use Reverse helper to make it a min-heap
    heap.push((Reverse(0), 0, 0));
    // classic Dijkstra algorithm
    while let Some((v, x, y)) = heap.pop() {
        let p = distances[size * y + x];
        // only consider the closest unvisited point
        if !visited(p) {
            for (i, j) in neighbours(x, y, size) {
                let p2 = &mut distances[size * j + i];
                // Only update unvisited points
                if !visited(*p2) {
                    let d = get(input, size, i, j) as u16;
                    let new_best = v.0 + d;
                    if new_best < *p2 {
                        *p2 = new_best as u16;
                        heap.push((Reverse(*p2), i, j));
                    }
                }
            }
            if y == size - 1 && x == size - 1 {
                return distances[size * y + x];
            }
            // mark current point as visited
            distances[size * y + x] |= VISITED_MASK;
        }
    }
    distances[size * (size - 1) + size - 1] & !VISITED_MASK
}

/// helper function to access the value of a point in the input
fn get(grid: &str, size: usize, x: usize, y: usize) -> u8 {
    // use size+1 since the input has an additional '\n'
    grid.as_bytes()[(size + 1) * y + x] - b'0'
}

/// helper function to iterate over the neighbours of a point
fn neighbours(x: usize, y: usize, size: usize) -> impl Iterator<Item = (usize, usize)> {
    [
        (x as isize - 1, y as isize),
        (x as isize, y as isize - 1),
        (x as isize, y as isize + 1),
        (x as isize + 1, y as isize),
    ]
    .into_iter()
    .filter_map(move |(i, j)| {
        if i >= 0 && j >= 0 && i < size as isize && j < size as isize {
            Some((i as usize, j as usize))
        } else {
            None
        }
    })
}

const VISITED_MASK: u16 = 1 << 15;

fn visited(v: u16) -> bool {
    v & VISITED_MASK > 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
";
        assert_eq!(run(input), 40)
    }
}
