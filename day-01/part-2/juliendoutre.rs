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
    let sliding_window_size = 3;

    let measurements: Vec<u64> = input
        .lines()
        .map(|line| line.parse::<u64>().unwrap())
        .collect();

    (0..(measurements.len() - sliding_window_size)).fold(0, |increases, index| {
        increases + (measurements[index] < measurements[index + sliding_window_size]) as u64
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "199
200
208
210
200
207
240
269
260
263";

        assert_eq!(run(test_case), 5)
    }
}
