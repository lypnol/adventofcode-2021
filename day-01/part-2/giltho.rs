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
    let second = lines.next().unwrap().parse::<u32>().unwrap();
    let third = lines.next().unwrap().parse::<u32>().unwrap();
    input
        .lines()
        .fold(
            (0, (first, second, third)),
            |(count, (first, second, third)), next| {
                let next_i = next.parse::<u32>().unwrap();
                let next_triple = (second, third, next_i);
                let next_count = if first + second + third < second + third + next_i {
                    count + 1
                } else {
                    count
                };
                (next_count, next_triple)
            },
        )
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
        assert_eq!(run(small_input), 5);
    }
}
