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
    pub fn risk_level(&self, index: (isize, isize)) -> u32 {
        (self[index] - 47) as u32
    }

    pub fn is_low_point(&self, index: (isize, isize)) -> bool {
        let (a, b) = index;
        self[index] < self[(a, b - 1)]
            && self[index] < self[(a, b + 1)]
            && self[index] < self[(a - 1, b)]
            && self[index] < self[(a + 1, b)]
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
    let mut res = 0;
    for i in 0..V_LEN {
        for j in 0..H_LEN {
            if grid.is_low_point((i, j)) {
                res += grid.risk_level((i, j))
            }
        }
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
9899965678"
                .as_bytes()),
            15
        )
    }
}
