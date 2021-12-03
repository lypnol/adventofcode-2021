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
    let lines: Vec<&[u8]> = input.lines().map(|line| line.as_bytes()).collect();

    let o2_rating = compute_rating(&lines, Mode::MostCommon);
    let co2_rating = compute_rating(&lines, Mode::LeastCommon);

    o2_rating * co2_rating
}

enum Mode {
    MostCommon,
    LeastCommon,
}

fn compute_rating(numbers: &Vec<&[u8]>, mode: Mode) -> usize {
    let compare = match mode {
        Mode::MostCommon => |x, y| x > y,
        Mode::LeastCommon => |x, y| x <= y,
    };

    let mut numbers = numbers.clone();
    let mut position = 0;
    while (&numbers).len() > 1 {
        let mut start_with_one = vec![];
        let mut start_with_zero = vec![];
        for &number in (&numbers).iter() {
            match number[position] {
                b'0' => start_with_zero.push(number),
                b'1' => start_with_one.push(number),
                _ => {}
            }
        }

        numbers = if compare(start_with_zero.len(), (&numbers).len() / 2) {
            start_with_zero
        } else {
            start_with_one
        };

        position += 1;
    }

    numbers[0]
        .iter()
        .map(|b| b - b'0')
        .fold(0, |acc, b| (acc << 1) + (b as usize))
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
