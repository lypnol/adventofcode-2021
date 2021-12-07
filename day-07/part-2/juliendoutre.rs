use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> i32 {
    let positions = input
        .split(',')
        .map(|n| n.parse::<i32>().unwrap())
        .collect::<Vec<i32>>();

    let average = positions.iter().sum::<i32>() / positions.len() as i32;
    let (mut r1, mut r2) = (0, 0);

    for n in positions {
        let (a, b) = ((average - n).abs(), (average + 1 - n).abs());
        r1 += a * (a + 1) / 2;
        r2 += b * (b + 1) / 2;
    }

    std::cmp::min(r1, r2)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("16,1,2,0,4,2,7,1,2,14"), 168)
    }
}
