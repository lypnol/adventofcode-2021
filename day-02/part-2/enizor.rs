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
    let mut depth = 0;
    let mut pos = 0;
    let mut aim = 0;
    for line in input.lines() {
        let mut words = line.split_whitespace();
        let verb = words.next().unwrap_or_default();
        let val = words.next().unwrap_or_default().parse::<usize>().unwrap_or_default();
        match verb {
            "forward" => {pos += val; depth += val*aim },
            "down" => {aim += val},
            "up" => {aim -= val},
            _ => {}
        }
    }
    depth * pos
}


#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "forward 5
down 5
forward 8
up 3
down 8
forward 2";
        assert_eq!(run(input), 900)
    }
}
