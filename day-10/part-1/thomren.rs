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
    input.lines().map(score_line).sum()
}

fn score_line(line: &str) -> usize {
    let mut stack = vec![];
    for c in line.as_bytes() {
        match c {
            b'(' | b'[' | b'{' | b'<' => stack.push(*c),
            b')' | b']' | b'}' | b'>' => {
                if *stack.last().unwrap_or(&0) == opening_char(*c) {
                    stack.pop();
                } else {
                    return char_score(*c);
                }
            }
            b'\n' => stack.clear(),
            _ => {}
        }
    }
    0
}

fn char_score(c: u8) -> usize {
    match c {
        b')' => 3,
        b']' => 57,
        b'}' => 1197,
        b'>' => 25137,
        _ => 0,
    }
}

fn opening_char(c: u8) -> u8 {
    match c {
        b')' => b'(',
        b']' => b'[',
        b'}' => b'{',
        b'>' => b'<',
        _ => 0,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"),
            26397
        )
    }
}
