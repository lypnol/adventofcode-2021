#![feature(int_abs_diff)]

use std::env::args;
use std::time::Instant;

#[cfg(test)]
const SIZE: usize = 10;

#[cfg(not(test))]
const SIZE: usize = 1000;

static mut DATA: [u32; SIZE] = [0; SIZE];

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

macro_rules! commit {
    ($acc: expr, $idx: expr) => {{
        unsafe {
            *DATA.get_unchecked_mut($idx) = $acc;
        }
        $acc = 0;
        $idx += 1;
    }};
}

#[inline(always)]
fn dist(x: u32) -> u32 {
    let mut i = 0;
    let mut s = 0;
    while i < SIZE {
        let dist = unsafe { DATA.get_unchecked(i).abs_diff(x) };
        s += (dist * (dist + 1)) / 2;
        i += 1;
    }
    s
}

fn run(input: &[u8]) -> u32 {
    let len = input.len();
    let mut idx = 0;
    let mut num_acc = 0;
    let mut c = 0;
    // Parsing
    while c < len {
        match unsafe { input.get_unchecked(c) } {
            b',' => commit!(num_acc, idx),
            c => num_acc = 10 * num_acc + (c - 48) as u32,
        }
        c += 1;
    }
    unsafe {
        *DATA.get_unchecked_mut(idx) = num_acc;
    }

    let mut prev = 0;
    let mut prev_dist = dist(0);
    loop {
        let next = prev + 1;
        let next_dist = dist(next);
        if next_dist >= prev_dist {
            return prev_dist;
        }
        prev = next;
        prev_dist = next_dist;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("16,1,2,0,4,2,7,1,2,14".as_bytes()), 168)
    }
}
