use std::env::args;
use std::time::Instant;

// This solution assumes that the zone is always under 0 vertically

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn parse_number(input: &[u8]) -> (i32, usize) {
    let mut acc = 0;
    let mut sign = 1;
    let mut len = 0;
    for c in input {
        match c {
            b'-' => sign = -1,
            b'.' | b',' => break,
            c => acc = acc * 10 + (c - 48) as i32,
        }
        len += 1;
    }
    (acc * sign, len)
}

#[inline]
fn parse(input: &[u8]) -> (i32, i32, i32, i32) {
    let mut idx = 15;
    let (xs, xsl) = parse_number(&input[idx..]);
    idx += xsl + 2;
    let (xe, xel) = parse_number(&input[idx..]);
    idx += xel + 4;
    let (ys, ysl) = parse_number(&input[idx..]);
    idx += ysl + 2;
    let (ye, _) = parse_number(&input[idx..]);
    (xs, xe, ys, ye)
}

fn run(input: &[u8]) -> i32 {
    let (_xs, _xe, ys, _ye) = parse(input);
    (ys + 1) * ys / 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("target area: x=20..30, y=-10..-5".as_bytes()), 45);
    }
}
