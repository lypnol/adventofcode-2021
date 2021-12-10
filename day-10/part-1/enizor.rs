#![feature(int_abs_diff)]
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn score(c: u8) -> usize {
    match c {
        b')' => 3,
        b']' => 57,
        b'}' => 1197,
        b'>' => 25137,
        _ => panic!(),
    }
}

fn run(input: &str) -> usize {
    let mut res = 0;
    let mut stack = Vec::new();
    for line in input.lines() {
        stack.clear();
        for &c in line.as_bytes() {
            match c {
                b'(' | b'[' | b'{' | b'<' => stack.push(c),
                _ => {
                    let c2 = stack.pop().unwrap_or(0);
                    if c2.abs_diff(c) > 2 {
                        res += score(c);
                        break;
                    }
                }
            }
        }
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]";
        assert_eq!(run(input), 26397)
    }
}
