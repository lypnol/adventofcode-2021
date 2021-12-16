use std::env::args;
use std::time::Instant;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[inline]
fn bit_rev_4(mut x: u8) -> u8 {
    x = (x & 0x3) << 2 | (x & 0xC) >> 2;
    (x & 0xA) >> 1 | (x & 0x5) << 1
}

struct Biterator<'a> {
    buffer: std::slice::Iter<'a, u8>,
    leftovers: u8,
    leftovers_to_consume: u8,
    read: u16,
}

impl<'a> From<&'a [u8]> for Biterator<'a> {
    fn from(input: &'a [u8]) -> Self {
        Self {
            buffer: input.iter(),
            leftovers: 0,
            leftovers_to_consume: 0,
            read: 0,
        }
    }
}

impl<'a> Iterator for Biterator<'a> {
    type Item = u16;

    fn next(&mut self) -> Option<Self::Item> {
        if self.leftovers_to_consume == 0 {
            let x = *self.buffer.next()?;
            let b = if x < b'A' { x - b'0' } else { (x - b'A') + 10 };
            self.leftovers = bit_rev_4(b);
            self.leftovers_to_consume = 4;
            self.next()
        } else {
            let res = (self.leftovers % 2) as u16;
            self.leftovers >>= 1;
            self.leftovers_to_consume -= 1;
            self.read += 1;
            Some(res)
        }
    }
}

macro_rules! take_3 {
    ($it: expr) => {
        $it.next().unwrap() << 2 | $it.next().unwrap() << 1 | $it.next().unwrap()
    };
}

macro_rules! take_15 {
    ($it: expr) => {
        $it.next().unwrap() << 14
            | $it.next().unwrap() << 13
            | $it.next().unwrap() << 12
            | $it.next().unwrap() << 11
            | $it.next().unwrap() << 10
            | $it.next().unwrap() << 9
            | $it.next().unwrap() << 8
            | $it.next().unwrap() << 7
            | $it.next().unwrap() << 6
            | $it.next().unwrap() << 5
            | $it.next().unwrap() << 4
            | $it.next().unwrap() << 3
            | $it.next().unwrap() << 2
            | $it.next().unwrap() << 1
            | $it.next().unwrap()
    };
}

macro_rules! take_11 {
    ($it: expr) => {
        $it.next().unwrap() << 10
            | $it.next().unwrap() << 9
            | $it.next().unwrap() << 8
            | $it.next().unwrap() << 7
            | $it.next().unwrap() << 6
            | $it.next().unwrap() << 5
            | $it.next().unwrap() << 4
            | $it.next().unwrap() << 3
            | $it.next().unwrap() << 2
            | $it.next().unwrap() << 1
            | $it.next().unwrap()
    };
}

macro_rules! take_4 {
    ($it: expr) => {
        $it.next().unwrap() << 3
            | $it.next().unwrap() << 2
            | $it.next().unwrap() << 1
            | $it.next().unwrap()
    };
}

fn parse_literal(it: &mut Biterator<'_>) -> u128 {
    let mut last = it.next().unwrap() == 0;
    let mut acc: u128 = 0;
    loop {
        acc = acc << 4 | (take_4!(it) as u128);
        if last {
            return acc;
        }
        last = it.next().unwrap() == 0
    }
}

fn parse(it: &mut Biterator<'_>) -> u128 {
    let _version = take_3!(it);
    let type_id = take_3!(it);
    if type_id == 4 {
        parse_literal(it)
    } else {
        // operator
        let subpackets = if it.next().unwrap() == 0 {
            // Next 15 bits give the size of the next packet
            let packet_size = take_15!(it);
            parse_with_size(it, packet_size)
        } else {
            let packet_amount = take_11!(it);
            parse_amount(it, packet_amount)
        };
        match type_id {
            0 => subpackets.into_iter().fold(0, std::ops::Add::add),
            1 => subpackets.into_iter().fold(1, std::ops::Mul::mul),
            2 => subpackets.into_iter().fold(u128::MAX, std::cmp::min),
            3 => subpackets.into_iter().fold(u128::MIN, std::cmp::max),
            5 => (subpackets[0] > subpackets[1]) as u128,
            6 => (subpackets[0] < subpackets[1]) as u128,
            7 => (subpackets[0] == subpackets[1]) as u128,
            _ => panic!("Unhandled operation"),
        }
    }
}

fn parse_amount(it: &mut Biterator<'_>, amount: u16) -> Vec<u128> {
    let mut content = Vec::with_capacity(2);
    for _ in 0..amount {
        content.push(parse(it))
    }
    content
}

fn parse_with_size(it: &mut Biterator<'_>, sz: u16) -> Vec<u128> {
    let read_before = it.read;
    let mut content = Vec::with_capacity(2);
    while it.read - read_before < sz {
        content.push(parse(it))
    }
    content
}

fn run(input: &[u8]) -> u128 {
    let mut biterator = Biterator::from(input);
    parse(&mut biterator)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bit_rev() {
        assert_eq!(0b0000, bit_rev_4(0b0000));
        assert_eq!(0b1000, bit_rev_4(0b0001));
        assert_eq!(0b0100, bit_rev_4(0b0010));
        assert_eq!(0b1100, bit_rev_4(0b0011));
    }

    #[test]
    fn run_test() {
        assert_eq!(run("C200B40A82".as_bytes()), 3);
        assert_eq!(run("04005AC33890".as_bytes()), 54);
        assert_eq!(run("880086C3E88112".as_bytes()), 7);
        assert_eq!(run("CE00C43D881120".as_bytes()), 9);
        assert_eq!(run("D8005AC2A8F0".as_bytes()), 1);
        assert_eq!(run("F600BC2D8F".as_bytes()), 0);
        assert_eq!(run("9C005AC2F8F0".as_bytes()), 0);
        assert_eq!(run("9C0141080250320F1802104A08".as_bytes()), 1);
    }
}
