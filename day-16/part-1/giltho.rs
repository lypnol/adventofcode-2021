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

impl<'a> Biterator<'a> {
    fn skip_literal(&mut self) {
        let mut last = self.next().unwrap() == 0;
        loop {
            self.next();
            self.next();
            self.next();
            self.next();
            if last {
                break;
            }
            last = self.next().unwrap() == 0
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

struct Packet(u16); // For, we only consider the sum of all version numbers

impl Packet {
    fn parse(it: &mut Biterator<'_>) -> Self {
        let version = take_3!(it);
        let type_id = take_3!(it);
        if type_id == 4 {
            // Literal
            it.skip_literal();
            Self(version)
        } else {
            // operator
            if it.next().unwrap() == 0 {
                // Next 15 bits give the size of the next packet
                let packet_size = take_15!(it);
                let packet = Self::parse_with_size(it, packet_size);
                Self(version + packet.0)
            } else {
                let packet_amount = take_11!(it);
                let packet = Self::parse_amount(it, packet_amount);
                Self(version + packet.0)
            }
        }
    }

    fn parse_amount(it: &mut Biterator<'_>, amount: u16) -> Self {
        let mut acc = 0;
        for _ in 0..amount {
            acc += Self::parse(it).0
        }
        Self(acc)
    }

    fn parse_with_size(it: &mut Biterator<'_>, sz: u16) -> Self {
        let read_before = it.read;
        let mut acc = 0;
        while it.read - read_before < sz {
            acc += Self::parse(it).0
        }
        Self(acc)
    }
}

fn run(input: &[u8]) -> u16 {
    let mut biterator = Biterator::from(input);
    Packet::parse(&mut biterator).0
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
        assert_eq!(run("D2FE28".as_bytes()), 6);
        assert_eq!(run("8A004A801A8002F478".as_bytes()), 16);
        assert_eq!(run("C0015000016115A2E0802F182340".as_bytes()), 23);
        assert_eq!(run("A0016C880162017C3686B18A3D4780".as_bytes()), 31);
    }
}
