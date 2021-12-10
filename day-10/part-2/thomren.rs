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
    let mut scores: Vec<usize> = input.lines().filter_map(score_line).collect();
    scores.sort();
    scores[scores.len() / 2]
}

fn score_line(line: &str) -> Option<usize> {
    let mut stack = vec![];
    for c in line.as_bytes() {
        match c {
            b'(' | b'[' | b'{' | b'<' => stack.push(*c),
            b')' | b']' | b'}' | b'>' => {
                if *stack.last().unwrap_or(&0) == opening_char(*c) {
                    stack.pop();
                } else {
                    // corrupted line
                    return None;
                }
            }
            _ => {}
        }
    }

    // compute score of incomplete lines
    let mut score = 0;
    while let Some(c) = stack.pop() {
        score *= 5;
        score += char_score(c);
    }
    Some(score)
}

fn char_score(c: u8) -> usize {
    match c {
        b'(' => 1,
        b'[' => 2,
        b'{' => 3,
        b'<' => 4,
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
            288957
        )
    }
}
