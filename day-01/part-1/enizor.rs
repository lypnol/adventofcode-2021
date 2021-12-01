use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output.unwrap_or_default());
}

fn run(input: &str) -> Option<usize> {
    let mut res = 0;
    let mut d1: usize = usize::MAX;
    for line in input.lines() {
        let d2: usize = line.parse().ok()?;
        if d2 > d1 {
            res += 1;
        }
        d1 = d2;
    }
    Some(res)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let example = r"199
200
208
210
200
207
240
269
260
263
";
        assert_eq!(run(example), Some(7))
    }
}
