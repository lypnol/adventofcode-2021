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

    fn next_bit(&mut self) -> Option<bool> {
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

    fn next_bits(&mut self, n: usize) -> usize {
        let mut res = 0;
        for _ in 0..n {
            res = (res << 1) + self.next_bit().unwrap() as usize;
        }
        res
    }

    fn bit_index(&mut self) -> usize {
        return 4 * self.position + (3 - self.bit as usize);
    }

    fn parse_packet(&mut self) -> usize {
        let version = self.next_bits(3);
        let type_id = self.next_bits(3);

        if type_id == 4 {
            self.parse_literal();
            version
        } else {
            version + self.parse_operator()
        }
    }

    fn parse_literal(&mut self) {
        let mut x = self.next_bits(5);
        while (x >> 4) == 1 {
            x = self.next_bits(5);
        }
    }

    fn parse_operator(&mut self) -> usize {
        let length_type_id = self.next_bits(1);
        let mut versions_sum = 0;
        if length_type_id == 1 {
            let n_subpackets = self.next_bits(11);
            for _ in 0..n_subpackets {
                versions_sum += self.parse_packet();
            }
        } else {
            let subpackets_length = self.next_bits(15);
            let end = self.bit_index() + subpackets_length;
            while self.bit_index() < end {
                versions_sum += self.parse_packet();
            }
        }
        versions_sum
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("D2FE28"), 6);
        assert_eq!(run("38006F45291200"), 9);
        assert_eq!(run("EE00D40C823060"), 14);
        assert_eq!(run("8A004A801A8002F478"), 16);
        assert_eq!(run("620080001611562C8802118E34"), 12);
        assert_eq!(run("C0015000016115A2E0802F182340"), 23);
        assert_eq!(run("A0016C880162017C3686B18A3D4780"), 31);
    }
}
