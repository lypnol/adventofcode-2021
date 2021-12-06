use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 256);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str, generations: usize) -> isize {
    let mut populations = [0; 9];

    input
        .lines()
        .next()
        .unwrap()
        .split(',')
        .map(|n| n.parse::<usize>().unwrap())
        .for_each(|n| populations[n] += 1);

    for _ in 0..generations {
        let new = populations[0];
        populations[0] = populations[1];
        populations[1] = populations[2];
        populations[2] = populations[3];
        populations[3] = populations[4];
        populations[4] = populations[5];
        populations[5] = populations[6];
        populations[6] = new + populations[7];
        populations[7] = populations[8];
        populations[8] = new;
    }

    populations.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("3,4,3,1,2", 256), 26984457539)
    }
}
