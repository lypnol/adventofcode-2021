use std::env::args;
use std::time::Instant;

#[cfg(test)]
const MAX_COORD: usize = 10;

#[cfg(not(test))]
const MAX_COORD: usize = 1000;

#[derive(Clone, Copy)]
enum Overlap {
    Zero,
    One,
    Saturated,
}

static mut GRID: [Overlap; MAX_COORD * MAX_COORD] = [Overlap::Zero; MAX_COORD * MAX_COORD];

static mut CLASHES: u32 = 0;

fn main() {
    let mut input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(input.as_mut());
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[derive(Clone, Copy)]
enum State {
    X1,
    Y1,
    X2,
    Y2,
}

macro_rules! update_cell {
    ($coord: expr) => {
        let z = GRID.get_unchecked_mut($coord);
        match z {
            Overlap::Zero => {
                *z = Overlap::One;
            }
            Overlap::One => {
                *z = Overlap::Saturated;
                CLASHES += 1;
            }
            _ => (),
        }
    };
}

// unsafe in concurrent settings
macro_rules! add_to_grid {
    ($x1: expr, $y1: expr, $x2: expr, $y2: expr) => {
        if $x1 == $x2 {
            let (min, max) = if $y1 < $y2 { ($y1, $y2) } else { ($y2, $y1) };
            for i in min..max + 1 {
                update_cell!(MAX_COORD * $x1 + i);
            }
        } else if $y1 == $y2 {
            let (min, max) = if $x1 < $x2 { ($x1, $x2) } else { ($x2, $x1) };
            for i in min..max + 1 {
                update_cell!(MAX_COORD * i + $y1);
            }
        }
    };
}

fn run(input: &str) -> u32 {
    let bytes = input.as_bytes();
    let mut num_acc = 0;
    let mut state = State::X1;
    let mut x1 = 0;
    let mut x2 = 0;
    let mut y1 = 0;
    let mut idx = 0;
    while idx < bytes.len() {
        match (state, unsafe { bytes.get_unchecked(idx) }) {
            (State::Y2, b'\n') => {
                unsafe { add_to_grid!(x1, y1, x2, num_acc) };
                x1 = 0;
                x2 = 0;
                y1 = 0;
                num_acc = 0;
                idx += 1;
                state = State::X1;
            }
            (State::X1, b',') => {
                x1 = num_acc;
                num_acc = 0;
                idx += 1;
                state = State::Y1;
            }
            (State::Y1, b' ') => {
                y1 = num_acc;
                num_acc = 0;
                idx += 4; // skip the arrow
                state = State::X2;
            }
            (State::X2, b',') => {
                x2 = num_acc;
                num_acc = 0;
                idx += 1;
                state = State::Y2;
            }
            (_, n) => {
                num_acc = 10 * num_acc + (n - 48) as usize;
                idx += 1;
            }
        }
    }
    unsafe { add_to_grid!(x1, y1, x2, num_acc) };
    unsafe { CLASHES }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";
        assert_eq!(run(small_input), 5);
    }
}
