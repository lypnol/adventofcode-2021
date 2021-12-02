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
    let (mut x, mut z) = (0, 0);
    for command in input.lines() {
        let (direction, delta) = command.split_once(" ").unwrap();
        let delta = delta.parse::<isize>().unwrap();
        match direction {
            "down" => z = z + delta,
            "up" => z = z - delta,
            "forward" => x = x + delta,
            _ => {}
        }
    }

    x * z
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("forward 5
down 5
forward 8
up 3
down 8
forward 2"),
            150
        )
    }
}
