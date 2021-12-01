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
    let mut antepenultimate;
    let (mut penultimate, mut previous, mut current) = (usize::MAX, usize::MAX, usize::MAX);
    let mut result = 0;

    for line in input.lines() {
        antepenultimate = penultimate;
        penultimate = previous;
        previous = current;
        current = line.parse::<usize>().unwrap();
        if current > antepenultimate {
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
            5
        )
    }
}
