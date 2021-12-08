use std::env::args;
use std::time::Instant;

const BEG_TRIM: usize = 61;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[inline(always)]
fn word_is_looked_for(word_sz: u32) -> u32 {
    match word_sz {
        2 | 3 | 4 | 7 => 1,
        _ => 0,
    }
}

fn run(input: &[u8]) -> u32 {
    let len = input.len();
    let mut res: u32 = 0;
    let mut word_sz: u32 = 0;
    let mut c = BEG_TRIM;
    // Parsing
    while c < len {
        match unsafe { input.get_unchecked(c) } {
            b'\n' => {
                c += BEG_TRIM + 1;
                res += word_is_looked_for(word_sz);
                word_sz = 0;
            }
            b' ' => {
                res += word_is_looked_for(word_sz);
                word_sz = 0;
                c += 1;
            }
            _ => {
                word_sz += 1;
                c += 1;
            }
        }
    }
    res + word_is_looked_for(word_sz)
}

#[cfg(test)]
mod tests {
    use super::*;

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
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce".as_bytes()), 26)
    }
}
