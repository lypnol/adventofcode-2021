use std::collections::{HashSet, VecDeque};
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let cave = input.as_bytes();
    let width = input.lines().next().unwrap().len();
    let height = (input.trim().as_bytes().len() + 1) / (width + 1);

    let mut basin_sizes = vec![];

    let mut size = 0;
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    for i in 0..height {
        for j in 0..width {
            if cave[(width + 1) * i + j] == b'9' {
                continue;
            }
            queue.push_back((i, j));

            while queue.len() > 0 {
                let (i, j) = queue.pop_front().unwrap();
                if visited.contains(&(i, j)) {
                    continue;
                };
                visited.insert((i, j));
                size += 1;
                for n in neighbors(i, j, height, width) {
                    if !visited.contains(&n) && cave[(width + 1) * n.0 + n.1] != b'9' {
                        queue.push_back(n);
                    }
                }
            }
            if size > 0 {
                basin_sizes.push(size);
                size = 0;
            }
        }
    }

    basin_sizes.sort();
    basin_sizes.reverse();
    basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
}

fn neighbors(i: usize, j: usize, height: usize, width: usize) -> Vec<(usize, usize)> {
    let mut res = vec![];
    if i > 0 {
        res.push((i - 1, j));
    }
    if j > 0 {
        res.push((i, j - 1));
    }
    if i < height - 1 {
        res.push((i + 1, j));
    }
    if j < width - 1 {
        res.push((i, j + 1));
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("2199943210
3987894921
9856789892
8767896789
9899965678"),
            1134
        )
    }
}
