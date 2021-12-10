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
    input.lines().map(line_score).sum()
}

fn line_score(line: &str) -> usize {
    let mut stack = Vec::<u8>::new();

    for c in line.as_bytes() {
        match c {
            b'(' | b'{' | b'[' | b'<' => stack.push(*c),
            b')' => {
                if stack.pop().unwrap() != b'(' {
                    return 3;
                }
            }
            b'}' => {
                if stack.pop().unwrap() != b'{' {
                    return 1197;
                }
            }
            b']' => {
                if stack.pop().unwrap() != b'[' {
                    return 57;
                }
            }
            b'>' => {
                if stack.pop().unwrap() != b'<' {
                    return 25137;
                }
            }
            _ => {}
        }
    }

    0
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

        assert_eq!(run(test_case), 26397)
    }
}
