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
    let mut scores: Vec<usize> = input
        .lines()
        .map(line_score)
        .filter(|score| *score != 0)
        .collect();
    scores.sort();

    scores[scores.len() / 2]
}

fn line_score(line: &str) -> usize {
    let mut stack = Vec::<u8>::new();

    for c in line.as_bytes() {
        match c {
            b'(' | b'{' | b'[' | b'<' => stack.push(*c),
            b')' => {
                if stack.pop().unwrap() != b'(' {
                    return 0;
                }
            }
            b'}' => {
                if stack.pop().unwrap() != b'{' {
                    return 0;
                }
            }
            b']' => {
                if stack.pop().unwrap() != b'[' {
                    return 0;
                }
            }
            b'>' => {
                if stack.pop().unwrap() != b'<' {
                    return 0;
                }
            }
            _ => {}
        }
    }

    let mut score = 0;
    while stack.len() > 0 {
        score *= 5;

        match stack.pop().unwrap() {
            b'(' => {
                score += 1;
            }
            b'{' => {
                score += 3;
            }
            b'[' => {
                score += 2;
            }
            b'<' => {
                score += 4;
            }
            _ => {}
        }
    }

    score
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]";

        assert_eq!(run(test_case), 288957)
    }
}
