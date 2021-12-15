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
    // size of the extended grid
    let big_size = 5 * size;
    // remember the current distance to each node
    // MSB determines of the node was previously visited
    let mut distances = vec![!VISITED_MASK; big_size * big_size];
    // starting point has distance 0 (and stays unvisited)
    distances[0] = 0;
    // priority queue of (best distance, x, y)
    let mut heap = BinaryHeap::new();
    // std heap is a max-heap, use Reverse helper to make it a min-heap
    heap.push((Reverse(0), 0, 0));
    // classic Dijkstra algorithm
    while let Some((v, x, y)) = heap.pop() {
        let p = distances[big_size * y + x];
        // only consider the closest unvisited point
        if !visited(p) {
            for (i, j) in neighbours(x, y, big_size) {
                let p2 = &mut distances[big_size * j + i];
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
            if y == big_size - 1 && x == big_size - 1 {
                return distances[big_size * y + x];
            }
            // mark current point as visited
            distances[big_size * y + x] |= VISITED_MASK;
        }
    }
    distances[big_size * (big_size - 1) + big_size - 1] & !VISITED_MASK
}

/// helper function to access the value of a point in the input
fn get(grid: &str, size: usize, x: usize, y: usize) -> usize {
    let i = x % size;
    let j = y % size;
    let v = grid.as_bytes()[(size + 1) * j + i] - b'0';
    let distance_to_grid = (x / size) + (y / size);
    // values are in range 1-9 so sub 1 to get in range of mod 9, then add back 1
    ((v as usize + distance_to_grid - 1) % 9) + 1
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
        assert_eq!(run(input), 315)
    }
}
