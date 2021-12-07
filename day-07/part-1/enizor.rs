#![feature(int_abs_diff)]
use std::cmp::Ordering;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

// ∀n, f_n(x) = |x-n| is convex
// So the fuel computation function F(x) = sum_i(f_i(x)) is convex
// and we can happily use a dichotomy
fn run(input: &str) -> usize {
    let mut crabs = Vec::with_capacity(input.len() / 3);
    let mut max = 0;
    for s in input.split(',') {
        let c: usize = s.parse().unwrap();
        crabs.push(c);
        max = max.max(c);
    }
    let mut p0 = 0;
    let mut p1 = max;
    // Invariant: the global minimum is in [p0, p1]
    loop {
        let pos = (p0 + p1) / 2;
        let new_fuel = compute_fuel(pos, &crabs);
        if (p1 - p0) < 2 {
            return new_fuel.0.min(new_fuel.1); // cannot divide further
        }
        match new_fuel.0.cmp(&new_fuel.1) {
            Ordering::Greater => p0 = pos + 1,
            Ordering::Less => p1 = pos,
            Ordering::Equal => return new_fuel.0, // real minimum is between pos and pos+1
        }
    }
}

/// Computes fuel consumption for pos and pos+1
fn compute_fuel(pos: usize, crabs: &[usize]) -> (usize, usize) {
    crabs.iter().fold((0, 0), |x, c| {
        (x.0 + c.abs_diff(pos), x.1 + c.abs_diff(pos + 1))
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("16,1,2,0,4,2,7,1,2,14"), 37)
    }
}
