use std::env::args;
use std::fmt::Error;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

enum Direction {
    Forward,
    Down,
    Up,
}

impl Direction {
    fn new(input: &str) -> Result<Direction, Error> {
        match input {
            "forward" => Ok(Direction::Forward),
            "down" => Ok(Direction::Down),
            "up" => Ok(Direction::Up),
            _ => Err(Error),
        }
    }
}

struct Move {
    direction: Direction,
    value: isize,
}

#[derive(Default)]
struct Position {
    horizontal: isize,
    depth: isize,
}

impl Position {
    fn update(&mut self, direction: Direction, value: isize) {
        match direction {
            Direction::Forward => self.horizontal += value,
            Direction::Down => self.depth += value,
            Direction::Up => self.depth -= value,
        }
    }
}

fn parse<'a>(input: &'a str) -> impl Iterator<Item = Move> + 'a {
    input.lines().filter_map(|l| {
        let mut vals = l.split(" ");
        let direction = Direction::new(vals.next()?).ok()?;
        let value = vals.next()?.parse().ok()?;
        Some(Move { direction, value })
    })
}

fn run(input: &str) -> isize {
    // Your code goes here
    let mut position = Position::default();
    for Move { direction, value } in parse(input) {
        position.update(direction, value);
    }
    position.horizontal * position.depth
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
