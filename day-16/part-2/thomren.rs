use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut parser = Parser::new(input.as_bytes());
    parser.parse_packet()
}

struct Parser<'a> {
    input: &'a [u8],
    position: usize,
    bit: u8,
}

impl<'a> Parser<'a> {
    fn new(input: &'a [u8]) -> Self {
        Self {
            input,
            position: 0,
            bit: 3,
        }
    }

    fn take_bits(&mut self, n: usize) -> usize {
        let mut res = 0;
        for _ in 0..n {
            res = (res << 1) + self.next().unwrap() as usize;
        }
        res
    }

    fn bit_index(&mut self) -> usize {
        return 4 * self.position + (3 - self.bit as usize);
    }

    fn parse_packet(&mut self) -> usize {
        let _version = self.take_bits(3);
        let type_id = self.take_bits(3);

        if type_id == 4 {
            // literal
            let mut value = 0;
            let mut x = self.take_bits(5);
            while (x >> 4) == 1 {
                value = (value << 4) + (x & 0b1111);
                x = self.take_bits(5);
            }
            value = (value << 4) + (x & 0b1111);

            value
        } else {
            // operator
            let length_type_id = self.take_bits(1);
            if length_type_id == 1 {
                let n_subpackets = self.take_bits(11);
                let mut values = Vec::with_capacity(n_subpackets);
                for _ in 0..n_subpackets {
                    values.push(self.parse_packet());
                }
                fold_values(type_id, values)
            } else {
                let subpackets_length = self.take_bits(15);
                let end = self.bit_index() + subpackets_length;
                let mut values = vec![];
                while self.bit_index() < end {
                    values.push(self.parse_packet());
                }
                fold_values(type_id, values)
            }
        }
    }
}

impl<'a> Iterator for Parser<'_> {
    type Item = bool;

    fn next(&mut self) -> Option<Self::Item> {
        if self.position >= self.input.len() {
            None
        } else {
            let hex = self.input[self.position];
            let dec = if hex < b'A' {
                hex - b'0'
            } else {
                10 + (hex - b'A')
            };

            let res = Some(((dec >> self.bit) & 1) == 1);

            if self.bit == 0 {
                self.position += 1;
                self.bit = 3;
            } else {
                self.bit -= 1;
            }

            res
        }
    }
}

fn fold_values(type_id: usize, values: Vec<usize>) -> usize {
    match type_id {
        0 => values.into_iter().sum(),
        1 => values.into_iter().product(),
        2 => values.into_iter().min().unwrap(),
        3 => values.into_iter().max().unwrap(),
        5 => (values[0] > values[1]) as usize,
        6 => (values[0] < values[1]) as usize,
        7 => (values[0] == values[1]) as usize,
        _ => panic!("Invalid type id: {}", type_id),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("C200B40A82"), 3);
        assert_eq!(run("04005AC33890"), 54);
        assert_eq!(run("880086C3E88112"), 7);
        assert_eq!(run("CE00C43D881120"), 9);
        assert_eq!(run("D8005AC2A8F0"), 1);
        assert_eq!(run("F600BC2D8F"), 0);
        assert_eq!(run("9C005AC2F8F0"), 0);
        assert_eq!(run("9C0141080250320F1802104A08"), 1);
    }
}
