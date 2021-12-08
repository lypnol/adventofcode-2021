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

/// Analyses a pattern with multiple possibilities
fn solve_clue(clue: u8, bd: u8, cf: u8, n: u8) -> usize {
    // patterns 2, 3, 5
    // changing segments are b,c,e,f
    // with the previous clue of digit 1 we know if the clue contain both segments cf or only one of them
    let count_cf = (clue & cf).count_ones();
    // with the previous clues of digit 1 and 4 we know if the clue contain both segments db or only one of them
    let count_bd = (clue & bd).count_ones();
    match (n, count_bd, count_cf) {
        (2, _, _) => 1,
        (3, _, _) => 7,
        (4, _, _) => 4,
        (5, 1, 1) => 2,
        (5, 1, 2) => 3,
        (5, 2, 1) => 5,
        (6, 2, 2) => 9,
        (6, 1, 2) => 0,
        (6, 2, 1) => 6,
        (7, _, _) => 8,
        _ => panic!("{} {} {}", n, count_bd, count_cf),
    }
}

fn solve_line(input: &str) -> usize {
    let mut clues = input.split(' ');
    let mut cf = 0;
    let mut bd = 0;
    for _ in 0..10 {
        let c = clues.next().unwrap();
        let mut clue_byte = 0;
        let n = c.len();
        if n == 2 || n == 4 {
            for c in c.as_bytes() {
                clue_byte |= 1 << (c - b'a');
            }
            if n == 2 {
                cf = clue_byte;
                bd &= !clue_byte;
            } else if n == 4 {
                bd = clue_byte & !cf;
            }
        }
    }
    let mut res = 0;
    for c in clues.skip(1) {
        res *= 10;
        let mut clue_byte = 0;
        let n = c.len() as u8;
        for c in c.as_bytes() {
            clue_byte |= 1 << (c - b'a');
        }
        res += solve_clue(clue_byte, bd, cf, n)
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
        // cagedb:
        // since it does not contain "ef" i.e. the segments bd it must be a 0
        assert_eq!(solve_clue(0b01011111, 0b00110000, 0b00000011, 6), 0);
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
