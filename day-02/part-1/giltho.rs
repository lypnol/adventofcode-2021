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
    let mut hor: usize = 0;
    let mut ver: usize = 0;
    for line in input.lines() {
        let mut words = line.split_ascii_whitespace();
        let command_first_letter = words.next().unwrap().chars().next().unwrap();
        let val = words.next().unwrap().parse::<usize>().unwrap();
        match command_first_letter {
            'f' => hor += val,
            'd' => ver += val,
            'u' => ver -= val,
            _ => panic!("Wrong input"),
        }
    }
    hor * ver
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "forward 5
down 5
forward 8
up 3
down 8
forward 2";
        assert_eq!(run(small_input), 150);
    }
}
