use std::collections::HashMap;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 40);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str, steps: usize) -> usize {
    let mut lines = input.lines();

    let state = lines.next().unwrap().as_bytes().to_owned();
    lines.next();

    let mut table = HashMap::<(u8, u8), [usize; 26]>::new();
    let mut rules = HashMap::<(u8, u8), u8>::new();

    lines
        .map(|line| line.split_once(" -> ").unwrap())
        .for_each(|(pattern, insert)| {
            let pattern = pattern.as_bytes();
            let insert = insert.as_bytes()[0];
            rules.insert((pattern[0], pattern[1]), insert);
            table.insert((pattern[0], pattern[1]), init_frequencies(insert));
        });

    for _ in 1..steps {
        let mut tmp = HashMap::<(u8, u8), [usize; 26]>::new();

        for ((a, b), &frequencies) in &table {
            if let Some(rule) = rules.get(&(*a, *b)) {
                let mut f = merge_frequencies(
                    table.get(&(*a, *rule)).unwrap(),
                    table.get(&(*rule, *b)).unwrap(),
                );
                f[*rule as usize - 65] += 1;

                tmp.insert((*a, *b), f);
            } else {
                tmp.insert((*a, *b), frequencies);
            }
        }

        table = tmp;
    }

    let mut frequencies = [0; 26];
    let mut previous = state[0];
    for b in &state[1..] {
        if let Some(f) = table.get(&(previous, *b)) {
            for i in 0..26 {
                frequencies[i] += f[i];
            }
        }

        frequencies[previous as usize - 65] += 1;
        previous = *b;
    }

    frequencies[previous as usize - 65] += 1;

    let (mut max, mut min) = (0, usize::MAX);
    for n in frequencies {
        if n > max {
            max = n;
        }

        if n < min && n != 0 {
            min = n;
        }
    }

    max - min
}

fn init_frequencies(a: u8) -> [usize; 26] {
    let mut f = [0; 26];
    f[a as usize - 65] = 1;

    f
}

fn merge_frequencies(a: &[usize; 26], b: &[usize; 26]) -> [usize; 26] {
    let mut f = [0; 26];

    for i in 0..26 {
        f[i] = a[i] + b[i];
    }

    f
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C";

        assert_eq!(run(test_case, 40), 2188189693529)
    }
}
