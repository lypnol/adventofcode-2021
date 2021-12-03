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
    // we assume that all lines have the same length
    let first_line = input.lines().next().unwrap();
    let line_length = first_line.len();
    let mut frequencies = vec![0; line_length];
    let mut n_lines: usize = 0;

    for line in input.lines() {
        n_lines += 1;
        for i in 0..line_length {
            frequencies[i] += (line.as_bytes()[i] == b'1') as usize;
        }
    }

    let gamma_rate = frequencies
        .iter()
        .map(|&n| if n > n_lines / 2 { 1 } else { 0 } as u8)
        .fold(0, |acc, b| (acc << 1) + (b as usize));
    let mask = (1 << first_line.len()) - 1;
    let epsilon_rate = !gamma_rate & mask;

    gamma_rate * epsilon_rate
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("00100
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
01010"),
            198
        )
    }
}
