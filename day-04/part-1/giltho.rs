use std::cmp::{max, min, Ordering};
use std::env::args;
use std::time::Instant;

const MAX_NUM: usize = 100;
const BOARD_SIZE: usize = 5;

static mut DRAWS: [usize; MAX_NUM] = [usize::MAX; MAX_NUM];
static mut CURRENT: [usize; 2 * BOARD_SIZE] = [0; 2 * BOARD_SIZE];

fn main() {
    let mut input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(input.as_mut());
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn result_from_board_at(board: &[u8], win_at: usize) -> usize {
    let mut num_acc = 0;
    let mut is_parsing = false;
    let mut last_number = 0;
    let mut sum_unmarked = 0;
    let mut lines = 0;
    for b in board {
        match b {
            b'\n' | b' ' => {
                if is_parsing {
                    let turn = unsafe { DRAWS[num_acc] };
                    match turn.cmp(&win_at) {
                        Ordering::Equal => last_number = num_acc,
                        Ordering::Greater => sum_unmarked += num_acc,
                        _ => (),
                    }
                    num_acc = 0;
                    if let b'\n' = b {
                        lines += 1;
                        if lines == 5 {
                            // this is not the last board
                            return last_number * sum_unmarked;
                        }
                    }
                }
            }
            _ => {
                is_parsing = true;
                num_acc = num_acc * 10 + (b - 48) as usize
            }
        }
    }
    // this is the last board
    let turn = unsafe { DRAWS[num_acc] };
    match turn.cmp(&win_at) {
        Ordering::Equal => last_number = num_acc,
        Ordering::Greater => sum_unmarked += num_acc,
        _ => (),
    }
    last_number * sum_unmarked
}

fn run(input: &str) -> usize {
    // number parse and other utils
    let mut num_acc: usize = 0;

    // variables for drawing time
    let mut drawing = true;
    let mut current_draw: usize = 0;

    // variables for borad time
    let mut win_at: usize = usize::MAX;
    let mut win_idx: usize = 0;
    let mut is_parsing = false;
    let mut x = 0;
    let mut y = 0;
    let mut last_start_idx: usize = 0;
    for (i, b) in input.as_bytes().iter().enumerate() {
        if drawing {
            match b {
                b',' => {
                    unsafe { DRAWS[num_acc] = current_draw };
                    num_acc = 0;
                    current_draw += 1;
                }
                b'\n' => {
                    unsafe { DRAWS[num_acc] = current_draw };
                    num_acc = 0;
                    current_draw += 1;
                    drawing = false;
                }
                _ => num_acc = num_acc * 10 + (b - 48) as usize,
            }
        } else {
            match b {
                b' ' | b'\n' => {
                    if is_parsing {
                        unsafe {
                            let turn = DRAWS[num_acc];
                            CURRENT[x] = max(CURRENT[x], turn);
                            CURRENT[5 + y] = max(CURRENT[5 + y], turn);
                        }
                        num_acc = 0;
                        x = (x + 1) % 5;
                        is_parsing = false;
                        if x == 0 {
                            y = (y + 1) % 5;
                            if y == 0 {
                                let this_wins_at =
                                    unsafe { CURRENT.iter().fold(usize::MAX, |x, y| min(x, *y)) };
                                if this_wins_at < win_at {
                                    win_at = this_wins_at;
                                    win_idx = last_start_idx;
                                }
                                last_start_idx = i + 2;
                                unsafe { CURRENT.fill(0) };
                            }
                        }
                    }
                }
                _ => {
                    is_parsing = true;
                    num_acc = num_acc * 10 + (b - 48) as usize
                }
            }
        }
    }
    // do it also after the last board
    unsafe {
        let turn = DRAWS[num_acc];
        CURRENT[x] = max(CURRENT[x], turn);
        CURRENT[5 + y] = max(CURRENT[5 + y], turn);
        let this_wins_at = CURRENT.iter().fold(usize::MAX, |x, y| min(x, *y));
        if this_wins_at < win_at {
            win_at = this_wins_at;
            win_idx = last_start_idx;
        }
    }

    result_from_board_at(&input.as_bytes()[win_idx..], win_at)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn example() {
        let small_input = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7";
        assert_eq!(run(small_input), 4512);
    }
}
