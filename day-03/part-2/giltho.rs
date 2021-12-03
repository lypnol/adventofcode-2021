use std::env::args;
use std::time::Instant;

#[cfg(test)]
const SIZE: usize = 32;

#[cfg(test)]
const LEN: usize = 5;

#[cfg(not(test))]
const SIZE: usize = 4096;

#[cfg(not(test))]
const LEN: usize = 12;

static mut TREE: [(u16, u16); SIZE] = [(0, 0); SIZE];

fn insert(tree: &mut [(u16, u16); SIZE], word: &[u8]) {
    let mut idx = 0;
    for s in word {
        if *s - 48 == 0 {
            // left
            tree[idx].0 += 1;
            idx = 2 * idx + 1;
        } else {
            // right
            tree[idx].1 += 1;
            idx = 2 * idx + 2;
        }
    }
}

macro_rules! declare_find {
    ($name: ident, $op: tt) => {
        fn $name(tree: &[(u16, u16); SIZE]) -> u32 {
            let mut val: u32 = 0;
            let mut fact: u32 = 2u32.pow(LEN as u32 - 1);
            let mut idx = 0;
            for _ in 0..LEN {
                let (a, b) = tree[idx];
                if a == 0 || (b > 0 && b $op a) {
                    // go right
                    val += fact;
                    idx = 2 * idx + 2;
                } else {
                    // go left
                    idx = 2 * idx + 1;
                }
                fact >>= 1;
            }
            val
        }
    };
}

declare_find!(co2, <);
declare_find!(oxygen, >=);

fn main() {
    let mut input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(input.as_mut());
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u32 {
    // let mut tree: [(u16, u16); SIZE] = [(0, 0); SIZE];
    for word in input.as_bytes().split(|x| *x == 10) {
        insert(unsafe { &mut TREE }, word);
    }
    let y = unsafe { oxygen(&TREE) };
    let x = unsafe { co2(&TREE) };
    x * y
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
        assert_eq!(run(small_input), 230);
    }
}
