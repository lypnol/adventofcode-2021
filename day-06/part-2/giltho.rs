use std::env::args;
use std::time::Instant;

const DATA: [u64; 5] = [6206821033, 5617089148, 5217223242, 4726100874, 4368232009];

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &[u8]) -> u64 {
    let mut ret = 0;
    let mut i = 0;
    let len = input.len();
    while i < len {
        match unsafe { input.get_unchecked(i) } {
            b',' => (),
            c => ret += unsafe { DATA.get_unchecked((c - 49) as usize) },
        };
        i += 1;
    }
    ret
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "3,4,3,1,2".as_bytes();
        assert_eq!(run(small_input), 26984457539);
    }
}
