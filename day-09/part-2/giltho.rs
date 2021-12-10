use std::collections::{HashSet, VecDeque};
use std::env::args;
use std::ops::Index;
use std::time::Instant;

#[cfg(test)]
const H_LEN: isize = 10;
#[cfg(test)]
const V_LEN: isize = 5;

#[cfg(not(test))]
const H_LEN: isize = 100;
#[cfg(not(test))]
const V_LEN: isize = 100;

struct Grid<'a>(&'a [u8]);

impl<'a> Index<(isize, isize)> for Grid<'a> {
    type Output = u8;
    fn index(&self, index: (isize, isize)) -> &u8 {
        if index.0 >= V_LEN || index.1 >= H_LEN || index.0 < 0 || index.1 < 0 {
            &u8::MAX
        } else {
            // bound checks already done
            unsafe {
                self.0
                    .get_unchecked((index.0 * (H_LEN + 1) + index.1) as usize)
            }
        }
    }
}

impl<'a> Grid<'a> {
    fn is_low_point(&self, index: (isize, isize)) -> bool {
        let (a, b) = index;
        self[index] < self[(a, b - 1)]
            && self[index] < self[(a, b + 1)]
            && self[index] < self[(a - 1, b)]
            && self[index] < self[(a + 1, b)]
    }

    /// Returns 0 if not a low point, size of the basin otherwise
    pub fn basin_size(&self, index: (isize, isize)) -> u32 {
        if !self.is_low_point(index) {
            return 0;
        }
        let (a, b) = index;
        let mut size = 1;
        let mut visited = HashSet::new();
        let curr_val = self[index];
        visited.insert(index);
        let mut to_visit = VecDeque::from(vec![
            (curr_val, (a, b - 1)),
            (curr_val, (a, b + 1)),
            (curr_val, (a - 1, b)),
            (curr_val, (a + 1, b)),
        ]);
        while !to_visit.is_empty() {
            let current = to_visit.pop_front().unwrap();
            let (v, curr_pos) = current;
            let (a, b) = curr_pos;
            let curr_val = self[curr_pos];

            if visited.contains(&curr_pos) || v >= curr_val || curr_val >= b'9' {
                continue;
            };
            visited.insert(curr_pos);
            size += 1;
            to_visit.push_back((curr_val, (a, b - 1)));
            to_visit.push_back((curr_val, (a, b + 1)));
            to_visit.push_back((curr_val, (a - 1, b)));
            to_visit.push_back((curr_val, (a + 1, b)));
        }
        size
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
    let grid = Grid(input);
    let mut basins: [u32; 3] = [0, 0, 0];
    for i in 0..V_LEN {
        for j in 0..H_LEN {
            let sz = grid.basin_size((i, j));
            if sz == 0 {
                continue;
            }
            if sz > basins[0] {
                basins[0] = sz;
                basins.sort_unstable();
            } else if sz > basins[1] {
                basins[1] = sz;
                basins.sort_unstable();
            } else if sz > basins[2] {
                basins[2] = sz;
                basins.sort_unstable();
            }
        }
    }
    basins[0] * basins[1] * basins[2]
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
9899965678"
                .as_bytes()),
            1134
        )
    }
}
