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
    let mut popcount = [0i16;16];
    let mut len = 0;
    for line in input.lines() {
        if len == 0 {
            len = line.len();
        }
        for (i, &c) in line.as_bytes().iter().enumerate() {
            match c {
                b'0' => popcount[i] -=1,
                b'1' => popcount[i] +=1,
                _ => {},
            }
        }
    }
    let mut gamma: usize = 0;
    for &b in &popcount {
        gamma <<= 1;
        if b > 0 {
            gamma |= 1;
        }
    }
    let mask = (1<<len) -1;
    gamma * (!gamma & mask)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010";
        assert_eq!(run(input), 198)
    }
}
