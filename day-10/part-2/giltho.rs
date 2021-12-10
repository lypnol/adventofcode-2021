use std::env::args;
use std::time::Instant;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn score_line(line: &[u8]) -> Option<u64> {
    let mut stack = Vec::with_capacity(20);
    for c in line {
        match c {
            b'(' | b'[' | b'{' | b'<' => stack.push(*c),
            b')' => {
                if stack.pop().unwrap() != b'(' {
                    return None;
                }
            }
            b']' => {
                if stack.pop().unwrap() != b'[' {
                    return None;
                }
            }
            b'}' => {
                if stack.pop().unwrap() != b'{' {
                    return None;
                }
            }
            b'>' => {
                if stack.pop().unwrap() != b'<' {
                    return None;
                }
            }
            _ => panic!("Incorrect input"),
        }
    }
    Some(stack.into_iter().rfold(0, |s, c| match c {
        b'(' => s * 5 + 1,
        b'[' => s * 5 + 2,
        b'{' => s * 5 + 3,
        b'<' => s * 5 + 4,
        _ => unreachable!(),
    }))
}

fn run(input: &[u8]) -> u64 {
    // Parsing
    let mut scores = Vec::with_capacity(200);
    for l in input.split(|x| *x == b'\n') {
        if let Some(s) = score_line(l) {
            scores.push(s)
        }
    }
    scores.sort_unstable();
    scores[scores.len() / 2]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r#"[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"#
                .as_bytes()),
            288957
        )
    }
}
