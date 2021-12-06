use std::env::args;
use std::time::Instant;

const DATA: [u64; 5] = [6206821033, 5617089148, 5217223242, 4726100874, 4368232009];

fn main() {
    let mut input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(input.as_mut());
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u64 {
    let mut ret = 0;
    for c in input.as_bytes() {
        match c {
            b',' => (),
            _ => ret += DATA[(c - 49) as usize],
        }
    }
    ret
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "3,4,3,1,2";
        assert_eq!(run(small_input), 26984457539);
    }
}
