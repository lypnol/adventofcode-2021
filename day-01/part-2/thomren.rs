use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let depths: Vec<isize> = input.lines().map(|x| x.parse().unwrap()).collect();
    depths
        .windows(3)
        .map(|w| w.iter().sum())
        .collect::<Vec<isize>>()
        .windows(2)
        .filter(|w| w[1] > w[0])
        .count() as isize
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
