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
    let mut prev_depth;
    let mut cur_depth = usize::MAX;
    let mut result = 0;

    for line in input.lines() {
        prev_depth = cur_depth;
        cur_depth = line.parse::<usize>().unwrap();
        if cur_depth > prev_depth {
            result += 1;
        }
    }

    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("199
200
208
210
200
207
240
269
260
263"),
            7
        )
    }
}
