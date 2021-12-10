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

fn score_line(line: &[u8]) -> u32 {
    let mut stack = Vec::with_capacity(20);
    for c in line {
        match c {
            b'(' | b'[' | b'{' | b'<' => stack.push(*c),
            b')' => {
                if stack.pop().unwrap() != b'(' {
                    return 3;
                }
            }
            b']' => {
                if stack.pop().unwrap() != b'[' {
                    return 57;
                }
            }
            b'}' => {
                if stack.pop().unwrap() != b'{' {
                    return 1197;
                }
            }
            b'>' => {
                if stack.pop().unwrap() != b'<' {
                    return 25137;
                }
            }
            _ => panic!("Incorrect input"),
        }
    }
    0
}

fn run(input: &[u8]) -> u32 {
    // Parsing
    input
        .split(|x| *x == b'\n')
        .fold(0, |s, l| s + score_line(l))
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
            26397
        )
    }
}
