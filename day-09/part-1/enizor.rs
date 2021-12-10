use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const MASK: u8 = 0x7f;
const GRID_SIZE: usize = 100;

fn run(input: &str) -> usize {
    let mut prev_line = [b'9'; GRID_SIZE + 2];
    // MSB indicates the point is a potential minimum
    let mut res = 0;
    for l in input.lines() {
        for (i, &c) in l.as_bytes().iter().enumerate() {
            let up = prev_line[i + 1];
            prev_line[i + 1] = c;
            let left = &mut prev_line[i];
            if c < *left & MASK {
                *left &= MASK;
            }
            if up & !MASK > 0 && c > up & MASK {
                res += ((up & MASK) - b'0' + 1) as usize;
            }
            if c < *left & MASK && c < up & MASK {
                prev_line[i + 1] |= !MASK;
            }
        }
    }
    for c in prev_line {
        if c & !MASK > 0 {
            res += ((c & MASK) - b'0' + 1) as usize;
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
9899965678"),
            15
        )
    }
}
