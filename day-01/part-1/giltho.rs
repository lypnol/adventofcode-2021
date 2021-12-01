use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u32 {
    let mut lines = input.lines();
    let first = lines.next().unwrap().parse::<u32>().unwrap();
    input
        .lines()
        .fold((0, first), |(count, prev), next| {
            let next_i = next.parse::<u32>().unwrap();
            if next_i > prev {
                (count + 1, next_i)
            } else {
                (count, next_i)
            }
        })
        .0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "199
200
208
210
200
207
240
269
260
263";
        assert_eq!(run(small_input), 7);
    }
}
