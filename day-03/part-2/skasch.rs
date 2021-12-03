use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn parse(input: &str) -> Vec<&str> {
    input.lines().filter(|s| !s.is_empty()).collect()
}

fn split(lines: Vec<&str>, pos: usize) -> (Vec<&str>, Vec<&str>) {
    let n_lines = lines.len();
    let (ones, zeros): (Vec<(&str, char)>, Vec<(&str, char)>) = lines
        .into_iter()
        .filter_map(|line| Some((line, line.chars().nth(pos)?)))
        .partition(|(_, char)| *char == '1');
    let (ones, zeros): (Vec<&str>, Vec<&str>) = (
        ones.into_iter().map(|(line, _)| line).collect(),
        zeros.into_iter().map(|(line, _)| line).collect(),
    );
    if ones.len() * 2 >= n_lines {
        (ones, zeros)
    } else {
        (zeros, ones)
    }
}

fn to_int(line: &str) -> isize {
    line.chars()
        .fold(0, |acc, val| acc * 2 + if val == '1' { 1 } else { 0 })
}

fn process(mut values: Vec<&str>, first: bool) -> isize {
    let mut pos = 1;
    while values.len() > 1 {
        values = {
            let res = split(values, pos);
            if first {
                res.0
            } else {
                res.1
            }
        };
        pos += 1;
    }
    to_int(values[0])
}

fn run(input: &str) -> isize {
    // Your code goes here
    let (o2_values, co2_values) = split(parse(input), 0);
    process(o2_values, true) * process(co2_values, false)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"),
            230
        )
    }
}
