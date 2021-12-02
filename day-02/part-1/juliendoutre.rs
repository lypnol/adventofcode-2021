use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Position {
    horizontal: u32,
    depth: u32,
}

fn run(input: &str) -> u32 {
    let mut position = Position {
        horizontal: 0,
        depth: 0,
    };

    for (instruction, value) in input
        .lines()
        .map(|line| line.split_once(' ').unwrap())
        .map(|line| (line.0, line.1.parse::<u32>().unwrap()))
    {
        match instruction {
            "up" => position.depth -= value,
            "down" => position.depth += value,
            "forward" => position.horizontal += value,
            _ => {}
        }
    }

    position.horizontal * position.depth
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "forward 5
down 5
forward 8
up 3
down 8
forward 2";

        assert_eq!(run(test_case), 150)
    }
}
