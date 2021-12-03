use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn parse(input: &str) -> Vec<&str> {
    input.lines().filter(|s| !s.is_empty()).collect()
}

fn get_gamma_epsilon(lines: Vec<&str>) -> (isize, isize) {
    let mut count_ones = vec![];
    let n_lines = lines.len();
    for line in lines {
        for (idx, char) in line.chars().enumerate() {
            match char {
                '1' => {
                    if count_ones.len() <= idx {
                        count_ones.push(1)
                    } else {
                        count_ones[idx] += 1
                    }
                }
                _ => (),
            }
        }
    }
    let size = count_ones.len();
    let mut res = 0;
    for value in count_ones {
        res = 2 * res + if 2 * value > n_lines { 1 } else { 0 };
    }
    (res, ((1 << size) - 1) ^ res)
}

fn run(input: &str) -> isize {
    // Your code goes here
    let (gamma, epsilon) = get_gamma_epsilon(parse(input));
    gamma * epsilon
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
