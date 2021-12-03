use std::env::args;
use std::time::Instant;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(&input);
    let elapsed = now.elapsed();
    drop(input);
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u32 {
    let bytes = input.as_bytes();
    let mut lines = bytes.split(|x| *x == 10);
    let first_line = lines.next().unwrap();
    let mut total = 1;
    let line_len = first_line.len();
    let mut freqs: Vec<u16> = Vec::with_capacity(first_line.len());
    for i in first_line {
        freqs.push(*i as u16 - 48)
    }
    for line in lines {
        for i in 0..line_len {
            freqs[i] += (line[i] - 48) as u16;
        }
        total += 1;
    }
    let mask: u16 = (2u16.pow(line_len as u32) - 1) as u16;
    let mut gamma: u16 = 0;
    for (i, freq) in freqs.iter().enumerate() {
        gamma += (2u16.pow((line_len - 1 - i) as u32)) * ((*freq >= (total / 2)) as u16);
    }
    let epsilon = (!gamma) & mask;
    epsilon as u32 * gamma as u32
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "00100
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
01010";
        assert_eq!(run(small_input), 198);
    }
}
