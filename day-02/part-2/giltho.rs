use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}
#[derive(PartialEq, Eq)]
enum State {
    Cmd,
    Forward,
    Down,
    Up,
}

fn run(input: &str) -> usize {
    let mut aim: usize = 0;
    let mut hor: usize = 0;
    let mut ver: usize = 0;
    let mut i: usize = 0;
    let chars = input.as_bytes();
    let mut state = State::Cmd;
    while i < chars.len() {
        let next_char = chars[i];
        match (&state, next_char) {
            (State::Cmd, 10 /*\n*/) => (),
            (State::Cmd, 102 /*f*/) => state = State::Forward,
            (State::Cmd, 117 /*u*/) => state = State::Up,
            (State::Cmd, 100 /*d*/) => state = State::Down,
            (State::Forward, 32 /* space */) => {
                i += 1;
                let val = (chars[i] - 48) as usize;
                hor += val;
                ver += val * aim;
                state = State::Cmd;
            }
            (State::Down, 32 /* space */) => {
                i += 1;
                aim += (chars[i] - 48) as usize;
                state = State::Cmd;
            }
            (State::Up, 32 /* space */) => {
                i += 1;
                aim -= (chars[i] - 48) as usize;
                state = State::Cmd;
            }
            (State::Up | State::Forward | State::Down, _) => (),
            _ => panic!("Wrong input: {}", next_char as char),
        }
        i += 1;
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
        assert_eq!(run(small_input), 900);
    }
}
