#![feature(int_abs_diff)]
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
    let mut crabs = Vec::with_capacity(input.len() / 3);
    let mut sum = 0;
    for s in input.split(',') {
        let c: usize = s.parse().unwrap();
        sum += c;
        crabs.push(c);
    }
    let mut fuel = sum;
    let mut pos = 0;
    loop {
        pos += 1;
        let new_fuel = crabs.iter().fold(0, |x, c| x + c.abs_diff(pos));
        if new_fuel > fuel {
            return fuel;
        }
        fuel = new_fuel;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("16,1,2,0,4,2,7,1,2,14"), 37)
    }
}
