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
    simulate(input, 256)
}

fn simulate(input: &str, n_days: usize) -> usize {
    let mut fish_counts: [usize; 9] = [0; 9];
    let mut zero_idx = 0;

    for n in input.split(",") {
        fish_counts[n.parse::<usize>().unwrap()] += 1
    }

    for _ in 0..n_days {
        fish_counts[(zero_idx + 1 + 6) % 9] += fish_counts[zero_idx];
        zero_idx = (zero_idx + 1) % 9;
    }

    fish_counts.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("3,4,3,1,2"), 26984457539)
    }
}
