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
        b'(' => 1,
        b'[' => 2,
        b'{' => 3,
        b'<' => 4,
        _ => panic!(),
    }
}

fn run(input: &str) -> usize {
    let mut scores = Vec::new();
    let mut stack = Vec::new();
    'line: for line in input.lines() {
        stack.clear();
        for &c in line.as_bytes() {
            match c {
                b'(' | b'[' | b'{' | b'<' => stack.push(c),
                _ => {
                    let c2 = stack.pop().unwrap_or(0);
                    // diff between opening and closing char is 1 for () and 2 for []{}<>
                    if c2.abs_diff(c) > 2 {
                        continue 'line;
                    }
                }
            }
        }
        let mut res = 0;
        while let Some(c) = stack.pop() {
            res *= 5;
            res += score(c);
        }
        scores.push(res);
    }
    scores.sort_unstable();
    scores[scores.len() / 2]
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
        assert_eq!(run(input), 288957)
    }

    #[test]
    fn test_single_line() {
        assert_eq!(run("[({(<(())[]>[[{[]{<()<>>"), 288957);
        assert_eq!(run("[(()[<>])]({[<{<<[]>>("), 5566);
        assert_eq!(run("(((({<>}<{<{<>}{[]{[]{}"), 1480781);
        assert_eq!(run("{<[[]]>}<{[{[{[]{()[[[]"), 995444);
        assert_eq!(run("<{([{{}}[<[[[<>{}]]]>[]]"), 294);
    }
}
