use std::collections::HashMap;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 10);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str, steps: usize) -> usize {
    let mut lines = input.lines();

    let mut state = lines.next().unwrap().as_bytes().to_owned();

    lines.next();

    let mut rules = HashMap::<(u8, u8), u8>::new();
    lines
        .map(|line| line.split_once(" -> ").unwrap())
        .for_each(|(pattern, insert)| {
            let pattern = pattern.as_bytes();
            rules.insert((pattern[0], pattern[1]), insert.as_bytes()[0]);
        });

    for _ in 0..steps {
        let mut new_state = Vec::<u8>::new();
        new_state.push(state[0]);

        for idx in 1..state.len() {
            if let Some(&rule) = rules.get(&(state[idx - 1], state[idx])) {
                new_state.push(rule);
            }

            new_state.push(state[idx]);
        }

        state = new_state;
    }

    let mut frequencies = [0; 26];
    for n in state {
        frequencies[n as usize - 65] += 1;
    }

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

        assert_eq!(run(test_case, 10), 1588)
    }
}
