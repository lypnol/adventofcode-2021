use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u16 {
    let mut polymer = Polymer::default();
    let (start, rules) = input.split_once("\n\n").unwrap();
    polymer.parse_rules(rules);
    polymer.parse_start(start);
    for _ in 0..10 {
        polymer.pair_insertion();
    }
    polymer.score()
}

#[derive(Default)]
struct Polymer {
    id2name: Vec<u8>,
    rules: Vec<u8>,
    pairs_previous: Vec<u16>,
    pairs_current: Vec<u16>,
    id_count: Vec<u16>,
}

impl Polymer {
    fn new_id(&mut self, name: u8) -> u8 {
        self.id2name.push(name);
        self.id2name.len() as u8 - 1
    }
    fn get_known_id(&self, id: u8) -> Option<u8> {
        self.id2name.iter().position(|s| *s == id).map(|x| x as u8)
    }
    fn get_id(&mut self, id: u8) -> u8 {
        self.get_known_id(id).unwrap_or_else(|| self.new_id(id))
    }
    fn get_ids_from_rule(&mut self, rule: &[u8]) -> (u8, u8, u8) {
        let id1 = self.get_id(rule[0]);
        let id2 = self.get_id(rule[1]);
        let id3 = self.get_id(rule[6]);
        (id1, id2, id3)
    }
    fn parse_rules(&mut self, rules: &str) {
        let mut rules_ids = Vec::new();
        for r in rules.lines() {
            rules_ids.push(self.get_ids_from_rule(r.as_bytes()));
        }
        self.rules
            .resize(self.id2name.len() * self.id2name.len(), 0);
        for (id1, id2, id3) in rules_ids {
            self.rules[id1 as usize * self.id2name.len() + id2 as usize] = id3;
        }
    }
    fn parse_start(&mut self, start: &str) {
        self.id_count.resize(self.id2name.len(), 0);
        self.pairs_current.resize(self.rules.len(), 0);
        self.pairs_previous.resize(self.rules.len(), 0);
        let mut previous_id = u8::MAX;
        for &b in start.as_bytes() {
            let id = self.get_id(b);
            if previous_id != u8::MAX {
                self.pairs_current[previous_id as usize * self.id2name.len() + id as usize] += 1;
            }
            self.id_count[id as usize] += 1;
            previous_id = id;
        }
    }
    fn pair_insertion(&mut self) {
        std::mem::swap(&mut self.pairs_current, &mut self.pairs_previous);
        for (p_id, nb) in self.pairs_previous.iter_mut().enumerate() {
            if *nb > 0 {
                let id2 = p_id % self.id2name.len();
                let id1 = p_id / self.id2name.len();
                let to_insert = self.rules[p_id];
                self.id_count[to_insert as usize] += *nb;
                let p1 = id1 as usize * self.id2name.len() + to_insert as usize;
                let p2 = to_insert as usize * self.id2name.len() + id2 as usize;
                self.pairs_current[p1] += *nb;
                self.pairs_current[p2] += *nb;
                *nb = 0;
            }
        }
    }
    fn score(&self) -> u16 {
        let mut min = u16::MAX;
        let mut max = 0;
        for &c in &self.id_count {
            min = min.min(c);
            max = max.max(c);
        }
        max - min
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_less_rules() {
        let input = "AB

AB -> C
AC -> C
CB -> C
CC -> C
";
        assert_eq!(run(input), (1 << 10) - 2)
    }

    #[test]
    fn run_test() {
        // NCNBCHB
        let input = "NNCB

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
        assert_eq!(run(input), 1588)
    }
}
