use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u64 {
    let mut t = Transmission::new(input);
    t.parse_packet().unwrap().value
}

struct Transmission<'a> {
    buf: BitBuffer<'a>,
}

#[derive(Debug, PartialEq, Eq)]
struct Packet {
    version: u8,
    type_id: u8,
    value: u64,
}

impl<'a> Transmission<'a> {
    fn new<'b: 'a>(input: &'b str) -> Self {
        Self {
            buf: BitBuffer::new(input),
        }
    }

    fn parse_header(&mut self) -> Option<(u8, u8)> {
        let version = self.buf.get_bits(3)? as u8;
        let type_id = self.buf.get_bits(3)? as u8;
        Some((version, type_id))
    }

    fn parse_literal(&mut self) -> Option<u64> {
        let mut v = 0;
        while self.buf.get_bits(1)? == 1 {
            v <<= 4;
            v += self.buf.get_bits(4)? as u64;
        }
        v <<= 4;
        v += self.buf.get_bits(4)? as u64;
        Some(v)
    }

    fn parse_binary_operator(&mut self, f: impl FnOnce(u64, u64) -> u64) -> Option<u64> {
        let len_id = self.buf.get_bits(1)?;
        if len_id == 0 {
            let _bits_len = self.buf.get_bits(15)?;
        } else {
            let _nb_packet = self.buf.get_bits(11)?;
        }
        let x = self.parse_packet()?.value;
        let y = self.parse_packet()?.value;
        Some(f(x, y))
    }

    fn parse_reduce_operator(
        &mut self,
        mut acc: u64,
        mut f: impl FnMut(u64, u64) -> u64,
    ) -> Option<u64> {
        let len_id = self.buf.get_bits(1)?;
        if len_id == 0 {
            let bits_len = self.buf.get_bits(15)?;
            let max = self.buf.cur * 4 - (self.buf.len as usize) + bits_len as usize;
            while self.buf.cur * 4 - (self.buf.len as usize) < max {
                let v = self.parse_packet()?.value;
                acc = f(acc, v);
            }
        } else {
            let nb_packet = self.buf.get_bits(11)?;
            for _ in 0..nb_packet {
                let v = self.parse_packet()?.value;
                acc = f(acc, v);
            }
        }
        Some(acc)
    }

    fn parse_packet(&mut self) -> Option<Packet> {
        let (version, type_id) = self.parse_header()?;
        let v = match type_id {
            0 => self.parse_reduce_operator(0, |acc, v| acc + v),
            1 => self.parse_reduce_operator(1, |acc, v| acc * v),
            2 => self.parse_reduce_operator(u64::MAX, |acc, v| acc.min(v)),
            3 => self.parse_reduce_operator(0, |acc, v| acc.max(v)),
            4 => self.parse_literal(),
            5 => self.parse_binary_operator(|a, b| if a > b { 1 } else { 0 }),
            6 => self.parse_binary_operator(|a, b| if a < b { 1 } else { 0 }),
            7 => self.parse_binary_operator(|a, b| if a == b { 1 } else { 0 }),
            _ => panic!(),
        }?;
        Some(Packet {
            version,
            type_id,
            value: v,
        })
    }
}

#[derive(Clone, Copy)]
struct BitBuffer<'a> {
    data: u32,
    len: u8,
    cur: usize,
    str_bytes: &'a [u8],
}

impl<'a> BitBuffer<'a> {
    fn new<'b: 'a>(input: &'b str) -> Self {
        Self {
            data: 0,
            len: 0,
            cur: 0,
            str_bytes: input.as_bytes(),
        }
    }
    /// add 4 bits into the buffer
    fn parse_add_bits(&mut self) -> Option<()> {
        if self.cur >= self.str_bytes.len() {
            return None;
        }
        let c = self.str_bytes[self.cur];
        self.cur += 1;
        let v = if c <= b'9' { c - b'0' } else { 10 + c - b'A' };
        self.data <<= 4;
        self.data |= v as u32;
        self.len += 4;
        Some(())
    }
    /// get n bits - n MUST BE <= 17
    fn get_bits(&mut self, n: u8) -> Option<u32> {
        while self.len < n {
            self.parse_add_bits()?;
        }
        let shift = self.len - n;
        let v = self.data & (u32::MAX << shift);
        self.data &= (1 << shift) - 1;
        self.len -= n;
        Some(v >> shift)
    }
}

impl Packet {}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn buffer_test() {
        let mut b = BitBuffer::new("D2FE28");
        assert_eq!(b.get_bits(3).unwrap(), 6);
        assert_eq!(b.get_bits(3).unwrap(), 4);
        assert_eq!(b.get_bits(1).unwrap(), 1);
        assert_eq!(b.get_bits(4).unwrap(), 7);
        assert_eq!(b.get_bits(1).unwrap(), 1);
        assert_eq!(b.get_bits(4).unwrap(), 14);
        assert_eq!(b.get_bits(1).unwrap(), 0);
        assert_eq!(b.get_bits(4).unwrap(), 5);
        let mut b = BitBuffer::new("38006F45291200");
        assert_eq!(b.get_bits(3).unwrap(), 1);
        assert_eq!(b.get_bits(3).unwrap(), 6);
        assert_eq!(b.get_bits(1).unwrap(), 0);
        assert_eq!(b.get_bits(15).unwrap(), 27);
    }

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
