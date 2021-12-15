use std::env::args;
use std::intrinsics::copy_nonoverlapping;
use std::time::Instant;

const NUMBER_OF_STEPS: usize = 39;

const NUMBER_OF_ELEMS: usize = 10;

#[cfg(test)]
const TEMPLATE_SIZE: usize = 4;

#[cfg(not(test))]
const TEMPLATE_SIZE: usize = 20;

const fn index_of_elem(x: u8) -> usize {
    match x {
        66 /*B*/ => 0,
        67 /*C*/ => 1,
        70 /*F*/ => 2,
        72 /*H*/ => 3,
        75 /*K*/ => 4,
        78 /*N*/ => 5,
        79 /*O*/ => 6,
        80 /*P*/ => 7,
        83 /*S*/ => 8,
        86 /*V*/ => 9,
        _ => unreachable!()
    }
}

// const fn rev_idx(x: usize) -> char {
//     match x {
//         0 => 'B',
//         1 => 'C',
//         2 => 'F',
//         3 => 'H',
//         4 => 'K',
//         5 => 'N',
//         6 => 'O',
//         7 => 'P',
//         8 => 'S',
//         9 => 'V',
//         _ => unreachable!(),
//     }
// }

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct RuleTable([usize; NUMBER_OF_ELEMS * NUMBER_OF_ELEMS]);
impl RuleTable {
    fn new() -> Self {
        Self([0; NUMBER_OF_ELEMS * NUMBER_OF_ELEMS])
    }

    fn add_rule(&mut self, x: usize, y: usize, z: usize) {
        self.0[x * NUMBER_OF_ELEMS + y] = z;
    }

    fn rule(&mut self, x: usize, y: usize) -> usize {
        self.0[x * NUMBER_OF_ELEMS + y]
    }
}

#[derive(Debug)]
struct Memory {
    mem: [u64; (NUMBER_OF_STEPS + 1) * NUMBER_OF_ELEMS * NUMBER_OF_ELEMS * NUMBER_OF_ELEMS],
    seen: [bool; (NUMBER_OF_STEPS + 1) * NUMBER_OF_ELEMS * NUMBER_OF_ELEMS],
}

impl Memory {
    fn new() -> Self {
        Self {
            mem: [0; (NUMBER_OF_STEPS + 1) * NUMBER_OF_ELEMS * NUMBER_OF_ELEMS * NUMBER_OF_ELEMS],
            seen: [false; (NUMBER_OF_STEPS + 1) * NUMBER_OF_ELEMS * NUMBER_OF_ELEMS],
        }
    }

    /// Marks as seen and returns if it was previously seen
    fn seen(&mut self, x: usize, y: usize, d: usize) -> bool {
        let key_seen =
            (x * NUMBER_OF_ELEMS * (NUMBER_OF_STEPS + 1)) + y * (NUMBER_OF_STEPS + 1) + d;
        let seen = self.seen[key_seen];
        self.seen[key_seen] = true;
        seen
    }

    fn get_res_mut(&mut self, x: usize, y: usize, d: usize) -> &mut [u64] {
        let key = x * NUMBER_OF_ELEMS * (NUMBER_OF_STEPS + 1) * NUMBER_OF_ELEMS
            + y * (NUMBER_OF_STEPS + 1) * NUMBER_OF_ELEMS
            + d * NUMBER_OF_ELEMS;
        &mut self.mem[key..key + NUMBER_OF_ELEMS]
    }

    fn add_rule(&mut self, x: usize, y: usize, z: usize) {
        self.seen(x, y, 0);
        let data = self.get_res_mut(x, y, 0);
        data[z] = 1;
    }
}

struct Polymerisation {
    memory: Memory,
    template: [usize; TEMPLATE_SIZE],
    rules: RuleTable,
}

impl Polymerisation {
    // Parses input and executes one step
    pub fn from_input(input: &[u8]) -> Self {
        let mut parse_idx = 0;
        let mut template_idx = 0;
        let mut template = [0; TEMPLATE_SIZE];
        let mut memory = Memory::new();
        let mut rules = RuleTable::new();
        loop {
            match unsafe { input.get_unchecked(parse_idx) } {
                b'\n' => {
                    break;
                }
                x => {
                    let elem_idx = index_of_elem(*x);
                    template[template_idx] = elem_idx;
                    template_idx += 1;
                    parse_idx += 1;
                }
            }
        }
        parse_idx += 2;
        let length = input.len();
        while parse_idx < length {
            let x = index_of_elem(*unsafe { input.get_unchecked(parse_idx) });
            let y = index_of_elem(*unsafe { input.get_unchecked(parse_idx + 1) });
            let z = index_of_elem(*unsafe { input.get_unchecked(parse_idx + 6) });
            rules.add_rule(x, y, z);
            memory.add_rule(x, y, z);
            parse_idx += 8;
        }
        Self {
            memory,
            template,
            rules,
        }
    }

    fn poly_pair(&mut self, x: usize, y: usize, d: usize) -> &[u64] {
        if !self.memory.seen(x, y, d) {
            // let mut data = [0; NUMBER_OF_ELEMS];
            // do the computation
            let mid = self.rules.rule(x, y);
            let left = self.poly_pair(x, mid, d - 1).as_ptr();
            let right = self.poly_pair(mid, y, d - 1).as_ptr();
            let res = self.memory.get_res_mut(x, y, d);
            // SAFETY: the two ranges are guarnteed to not be overlapping
            unsafe {
                copy_nonoverlapping(left, res.as_mut_ptr(), NUMBER_OF_ELEMS);
                for (i, v) in res.iter_mut().enumerate() {
                    *v += *right.add(i);
                }
            };
            res[mid] += 1;
            res
        } else {
            self.memory.get_res_mut(x, y, d)
        }
    }

    fn run(&mut self) -> u64 {
        let mut iter = self.template.into_iter();
        let mut prev = iter.next().unwrap();
        let mut total_seen = [0; NUMBER_OF_ELEMS];
        total_seen[prev] += 1;
        for this in iter {
            total_seen[this] += 1;
            let data = self.poly_pair(prev, this, NUMBER_OF_STEPS);
            for (j, v) in data.iter().enumerate() {
                total_seen[j] += v;
            }
            prev = this;
        }
        total_seen.iter().max().unwrap() - total_seen.into_iter().filter(|x| *x > 0).min().unwrap()
    }
}

fn run(input: &[u8]) -> u64 {
    Polymerisation::from_input(input).run()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_case() {
        assert_eq!(
            run("NNCB

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
CN -> C"
                .as_bytes()),
            2188189693529
        )
    }
}
