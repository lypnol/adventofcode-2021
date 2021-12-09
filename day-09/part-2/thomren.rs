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
    let cave: Vec<Vec<u8>> = input
        .lines()
        .map(|line| line.as_bytes().into_iter().map(|x| x - b'0').collect())
        .collect();

    let basin_centers = find_basin_centers(&cave);

    let mut basin_sizes: Vec<usize> = basin_centers
        .into_iter()
        .map(|center| basin_size(&cave, center))
        .collect();

    basin_sizes.sort();
    basin_sizes.reverse();
    basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
}

fn find_basin_centers(cave: &Vec<Vec<u8>>) -> Vec<(usize, usize)> {
    let mut res = vec![];
    let width = cave[0].len();
    let height = cave.len();

    for i in 0..height {
        for j in 0..width {
            if neighbors(i, j, height, width)
                .into_iter()
                .all(|(ni, nj)| cave[ni][nj] > cave[i][j])
            {
                res.push((i, j));
            }
        }
    }

    res
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

fn basin_size(cave: &Vec<Vec<u8>>, center: (usize, usize)) -> usize {
    let width = cave[0].len();
    let height = cave.len();
    let (x, y) = center;

    let mut size = 0;
    let mut visited = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back((x, y));

    while queue.len() > 0 {
        let (i, j) = queue.pop_front().unwrap();
        if visited.contains(&(i, j)) {
            continue;
        };
        visited.insert((i, j));
        size += 1;
        for n in neighbors(i, j, height, width) {
            if !visited.contains(&n) && cave[n.0][n.1] != 9 {
                queue.push_back(n);
            }
        }
    }

    size
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
