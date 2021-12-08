use std::collections::HashSet;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let mut sum = 0;
    for line in input.lines() {
        let (patterns, numbers) = line.split_once(" | ").unwrap();
        let (mut one, mut four) = (HashSet::new(), HashSet::new());
        for pattern in patterns.split_whitespace() {
            match pattern.as_bytes().len() {
                2 => one.extend(pattern.as_bytes()),
                4 => four.extend(pattern.as_bytes()),
                _ => {}
            }
        }

        sum += numbers
            .split_whitespace()
            .map(|number| {
                let nb = HashSet::from_iter(number.as_bytes().iter().cloned());
                match (
                    nb.len(),
                    nb.intersection(&one).count(),
                    nb.intersection(&four).count(),
                ) {
                    (2, _, _) => 1,
                    (3, _, _) => 7,
                    (4, _, _) => 4,
                    (5, 2, _) => 3,
                    (5, 1, 3) => 5,
                    (5, 1, 2) => 2,
                    (6, 1, _) => 6,
                    (6, 2, 4) => 9,
                    (6, 2, 3) => 0,
                    (7, _, _) => 8,
                    _ => panic!("invalid number: {:?}", number),
                }
            })
            .fold(0, |acc, x| 10 * acc + x);
    }

    sum
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_cases = vec!(
            (
                "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf",
                5353,
            ),
            (
                "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
                8394,
            ),
            (
                "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
                9781,
            ),
            (
                "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
                1197,
            ),
            (
                "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
                9361,
            ),
            (
                "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
                4873,
            ),
        );
        for (i, r) in test_cases.iter() {
            assert_eq!(run(i), *r);
        }

        assert_eq!(run("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"), 61229)
    }
}
