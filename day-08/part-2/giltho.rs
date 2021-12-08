use std::env::args;
use std::time::Instant;

const EIGHT: u8 = 254;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

enum State {
    Patterns,
    Output,
}

#[inline(always)]
fn is_zero_or_power_of_2(x: u8) -> bool {
    x & (x - 1) == 0
}

#[inline(always)]
fn reverse(x: u8, digits: &[u8; 10]) -> usize {
    let mut idx = 0;
    loop {
        if x == unsafe { *digits.get_unchecked(idx) } {
            return idx;
        }
        idx += 1;
    }
}

/*
    Parsed digits are represented as u8 of the form
    gfedcba0
    The fact that a parsed digit can never equal 0 means that
    (d & (d-1)) == 0 <=> d is a power of two, i.e, only one side is on.
*/
fn run(input: &[u8]) -> usize {
    let len = input.len();
    let mut res: usize = 0;
    let mut word_sz: u32 = 0;
    let mut current_digit: u8 = 0;
    let mut current_state = State::Patterns;
    let mut len_fives: [u8; 3] = [0, 0, 0];
    let mut len_sixes: [u8; 3] = [0, 0, 0];
    let mut five_idx = 0;
    let mut six_idx = 0;
    let mut digits: [u8; 10] = [0, 0, 0, 0, 0, 0, 0, 0, EIGHT, 0];
    let mut c = 0;
    let mut current_output: usize = 0;
    // Parsing
    while c < len {
        match unsafe { input.get_unchecked(c) } {
            b'\n' => {
                res += 10 * current_output + reverse(current_digit, &digits);
                current_digit = 0;
                word_sz = 0;
                current_output = 0;
                current_state = State::Patterns;
            }
            b' ' => {
                match current_state {
                    State::Patterns => {
                        match word_sz {
                            5 => unsafe {
                                *len_fives.get_unchecked_mut(five_idx) = current_digit;
                                five_idx += 1;
                            },
                            6 => unsafe {
                                *len_sixes.get_unchecked_mut(six_idx) = current_digit;
                                six_idx += 1;
                            },
                            2 => digits[1] = current_digit,
                            3 => digits[7] = current_digit,
                            4 => digits[4] = current_digit,
                            _ => (), // it's an 8
                        }
                    }
                    State::Output => {
                        current_output = 10 * current_output + reverse(current_digit, &digits)
                    }
                }
                word_sz = 0;
                current_digit = 0;
            }
            b'|' => {
                // First we solve the correspondance
                // top = digits[7] ^ digits[1];
                // top_left_and_center = digits[4] ^ digits[1]
                six_idx = 0;
                while six_idx < 3 {
                    let z = unsafe { *len_sixes.get_unchecked(six_idx) };
                    if is_zero_or_power_of_2(z ^ (digits[7] | digits[4])) {
                        digits[9] = z;
                    } else if (EIGHT ^ z) & digits[1] == 0 {
                        digits[0] = z
                    } else {
                        digits[6] = z
                    }
                    six_idx += 1;
                }
                six_idx = 0;
                while six_idx < 3 {
                    let z = unsafe { *len_fives.get_unchecked(six_idx) };
                    if z & digits[1] == digits[1] {
                        digits[3] = z;
                    } else if z | digits[4] == EIGHT {
                        digits[2] = z;
                    } else {
                        digits[5] = z
                    }
                    six_idx += 1;
                }
                // Then we increase the state
                current_state = State::Output;
                c += 1;
                five_idx = 0;
                six_idx = 0;
            }
            l => {
                current_digit |= 2u8 << (l - b'a');
                word_sz += 1;
            }
        }
        c += 1;
    }
    res + 10 * current_output + reverse(current_digit, &digits)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn smaller_test() {
        assert_eq!(run(
            "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
                .as_bytes()
        ), 5353)
    }

    #[test]
    fn run_test() {
        assert_eq!(run("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce".as_bytes()), 61229)
    }
}
