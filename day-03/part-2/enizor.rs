use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

/// More brittle but GOTTA GO FAST
type DiagnosticNumber = u16;
/// More resilient
// type diagnosticNumber = usize;

fn read_input(input: &str) -> (Vec<DiagnosticNumber>, Vec<DiagnosticNumber>, isize) {
    let mut ones = Vec::new();
    let mut zeroes = Vec::new();
    let mut len = 0;
    for line in input.lines() {
        let mut n = 0;
        let bytes = line.as_bytes();
        if len == 0 {
            len = bytes.len() as isize;
        }
        let first = bytes[0];
        n |= (first & 1) as DiagnosticNumber;
        for &c in &bytes[1..] {
            n <<= 1;
            n |= (c & 1) as u16;
        }
        if first & 1 > 0 {
            ones.push(n);
        } else {
            zeroes.push(n);
        }
    }
    if ones.len() >= zeroes.len() {
        (ones, zeroes, len)
    } else {
        (zeroes, ones, len)
    }
}

fn run(input: &str) -> usize {
    let (common, uncommon, len) = read_input(input);
    compute_rating::<true>(common, len - 2) * compute_rating::<false>(uncommon, len - 2)
}

/// Recursively computes an oxygen or carbon dioxyde rating
///
/// Parameters:
/// values: numbers to consider
/// pos: position of the bit to consider. 0=LSB
/// common: consider the most common bit or not
fn compute_rating<const COMMON: bool>(mut values: Vec<DiagnosticNumber>, mut pos: isize) -> usize {
    let mut ones = Vec::with_capacity(values.len());
    let mut zeroes = Vec::with_capacity(values.len());
    loop {
        if values.len() == 1 || pos < 0 {
            return values[0] as usize;
        } else {
            ones.clear();
            zeroes.clear();
            for &v in &values {
                if ((v >> pos) & 1) > 0 {
                    ones.push(v);
                } else {
                    zeroes.push(v);
                }
            }
            pos -= 1;
            if COMMON ^ (ones.len() >= zeroes.len()) {
                std::mem::swap(&mut values, &mut zeroes);
            } else {
                std::mem::swap(&mut values, &mut ones);
            }
        }
    }
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
        assert_eq!(run(input), 230)
    }
}
