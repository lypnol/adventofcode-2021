use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[allow(unused)]
fn dbg_deductions(deductions: &[u8]) {
    println!("Deductions:");
    for d in deductions.iter() {
        println!("    {:8b}", d);
    }
}

/// Analyses the clue when the pattern is unique, i.e. with a length of 2, 3, or 4
fn analyse_uniq(clue: u8, bd: &mut u8, cf: &mut u8, n: u8, solved: &mut [u8; 10]) {
    if n == 3 {
        solved[7] = clue;
    } else if n == 2 {
        solved[1] = clue;
        *cf = clue;
        *bd &= !clue;
    } else if n == 4 {
        solved[4] = clue;
        *bd = clue & !*cf;
    }
}

/// Analyses a pattern with multiple possibilities
fn analyse_complex(clue: u8, bd: &mut u8, cf: &mut u8, n: u8, solved: &mut [u8; 10]) {
    // patterns 2, 3, 5
    // changing segments are b,c,e,f
    // with the previous clue of digit 1 we know if the clue contain both segments cf or only one of them
    let count_cf = (clue & *cf).count_ones();
    // with the previous clues of digit 1 and 4 we know if the clue contain both segments db or only one of them
    let count_bd = (clue & *bd).count_ones();
    let digit = match (n, count_bd, count_cf) {
        (5, 1, 1) => 2,
        (5, 1, 2) => 3,
        (5, 2, 1) => 5,
        (6, 2, 2) => 9,
        (6, 1, 2) => 0,
        (6, 2, 1) => 6,
        _ => panic!("{} {} {}", n, count_bd, count_cf),
    };
    solved[digit] = clue;
}

fn solve_line(input: &str) -> usize {
    let mut clues = input.split(' ');
    let mut complex = [(0, 0); 6];
    let mut pos_complex = 0;
    let mut solved = [0; 10];
    solved[8] = 0x7f;
    let mut cf = 0;
    let mut bd = 0;
    for _ in 0..10 {
        let c = clues.next().unwrap();
        let mut clue_byte = 0;
        let n = c.len();
        for c in c.as_bytes() {
            clue_byte |= 1 << (c - b'a');
        }
        if n <= 4 {
            analyse_uniq(clue_byte, &mut bd, &mut cf, n as u8, &mut solved);
        } else if n <= 6 {
            complex[pos_complex] = (clue_byte, n as u8);
            pos_complex += 1;
        }
    }
    for &(c, n) in &complex {
        analyse_complex(c, &mut bd, &mut cf, n as u8, &mut solved);
    }
    let mut res = 0;
    for c in clues.skip(1) {
        res *= 10;
        let mut clue_byte = 0;
        for c in c.as_bytes() {
            clue_byte |= 1 << (c - b'a');
        }
        res += solved
            .iter()
            .enumerate()
            .find(|(_, &m)| m == clue_byte)
            .unwrap()
            .0;
    }
    res
}

fn run(input: &str) -> usize {
    let mut res = 0;
    for line in input.lines() {
        res += solve_line(line);
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solving() {
        let mut cf = 0;
        let mut bd = 0;
        let mut solved = [0; 10];
        analyse_uniq(0b00110011, &mut bd, &mut cf, 4, &mut solved); // "abef"
        assert_eq!(bd, 0b00110011);
        assert_eq!(solved[4], 0b00110011);
        analyse_uniq(0b00000011, &mut bd, &mut cf, 2, &mut solved); // "ab"
        assert_eq!(bd, 0b00110000);
        assert_eq!(cf, 0b00000011);
        assert_eq!(solved[1], 0b00000011);
        analyse_uniq(0b00001011, &mut bd, &mut cf, 3, &mut solved); // "dab"
        assert_eq!(solved[7], 0b00001011);

        // cagedb:
        // since it does not contain "ef" i.e. the segments bd it must be a 0
        analyse_complex(0b01011111, &mut bd, &mut cf, 6, &mut solved);
        assert_eq!(solved[0], 0b01011111);
    }

    #[test]
    fn line_test() {
        let input =
        "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe";
        assert_eq!(solve_line(input), 8394);
        let input =
            "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf";
        assert_eq!(solve_line(input), 5353);
    }

    #[test]
    fn run_test() {
        let input =
            "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce";
        assert_eq!(run(input), 61229)
    }
}
