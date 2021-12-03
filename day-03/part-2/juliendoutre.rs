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
    let numbers: Vec<&str> = input.lines().collect();
    filter(&numbers, 0, true) * filter(&numbers, 0, false)
}

fn filter(numbers: &[&str], cursor: usize, most_common: bool) -> u64 {
    if numbers.len() > 1 {
        let mut ones: Vec<&str> = Vec::new();
        let mut zeros: Vec<&str> = Vec::new();

        for n in numbers {
            if n.chars().nth(cursor).unwrap() == '1' {
                ones.push(n);
            } else {
                zeros.push(n);
            }
        }

        if most_common {
            if ones.len() >= zeros.len() {
                filter(&ones, cursor + 1, true)
            } else {
                filter(&zeros, cursor + 1, true)
            }
        } else {
            if ones.len() >= zeros.len() {
                filter(&zeros, cursor + 1, false)
            } else {
                filter(&ones, cursor + 1, false)
            }
        }
    } else {
        u64::from_str_radix(numbers[0], 2).unwrap()
    }
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
        assert_eq!(run(test_case), 230)
    }
}
