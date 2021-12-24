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
    let t = Transmission::new(input);
    t.fold(0, |acc, p| {
        acc + p.internal_version_sum + p.version as usize
    })
}

struct Transmission<'a> {
    buf: BitBuffer<'a>,
}

#[derive(Debug, PartialEq, Eq)]
struct Packet {
    version: u8,
    type_id: u8,
    internal_version_sum: usize,
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

    fn parse_literal(&mut self) -> Option<usize> {
        let mut v = 0;
        while self.buf.get_bits(1)? == 1 {
            v <<= 4;
            v += self.buf.get_bits(4)? as usize;
        }
        v <<= 4;
        v += self.buf.get_bits(4)? as usize;
        Some(v)
    }

    fn parse_operator(&mut self) -> Option<usize> {
        let len_id = self.buf.get_bits(1)?;
        let mut version_sum = 0;
        if len_id == 0 {
            let bits_len = self.buf.get_bits(15)?;
            let max = self.buf.cur * 4 - (self.buf.len as usize) + bits_len as usize;
            while self.buf.cur * 4 - (self.buf.len as usize) < max {
                let p = self.parse_packet()?;
                version_sum += p.version as usize + p.internal_version_sum;
            }
        } else {
            let nb_packet = self.buf.get_bits(11)?;
            for _ in 0..nb_packet {
                let p = self.parse_packet()?;
                version_sum += p.version as usize + p.internal_version_sum;
            }
        }
        Some(version_sum)
    }

    fn parse_packet(&mut self) -> Option<Packet> {
        let (version, type_id) = self.parse_header()?;
        if type_id == 4 {
            Some(Packet {
                version,
                type_id,
                internal_version_sum: {
                    self.parse_literal();
                    0
                },
            })
        } else {
            Some(Packet {
                version,
                type_id,
                internal_version_sum: self.parse_operator()?,
            })
        }
    }
}

impl<'a> Iterator for Transmission<'a> {
    type Item = Packet;

    fn next(&mut self) -> Option<Self::Item> {
        self.parse_packet()
    }
}

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
        assert_eq!(run("D2FE28"), 6);
        assert_eq!(run("38006F45291200"), 9);
        assert_eq!(run("EE00D40C823060"), 14);
        assert_eq!(run("8A004A801A8002F478"), 16);
        assert_eq!(run("620080001611562C8802118E34"), 12);
        assert_eq!(run("C0015000016115A2E0802F182340"), 23);
        assert_eq!(run("A0016C880162017C3686B18A3D4780"), 31);
    }
}
