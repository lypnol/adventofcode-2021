use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u64 {
    let mut total = 0;
    let mut ones_frequencies = [0; 12];
    let mut size = None;

    for line in input.lines() {
        total += 1;
        size.get_or_insert(line.len());

        for (i, c) in line.chars().enumerate() {
            if c == '1' {
                ones_frequencies[12 - size.unwrap() + i] += 1;
            }
        }
    }

    total /= 2;
    let mut gamma = 0;

    for i in 0..12 {
        if ones_frequencies[i] >= total {
            gamma += u64::pow(2, 11 - i as u32);
        }
    }

    gamma * ((1 << size.unwrap()) - 1 ^ gamma)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "00100
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
        assert_eq!(run(test_case), 198)
    }
}
