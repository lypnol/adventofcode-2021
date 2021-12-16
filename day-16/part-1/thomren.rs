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
    let bits = hex_to_bin(input);

    parse_packet(&bits[..], 0).1
}

fn parse_packet(s: &str, position: usize) -> (usize, usize) {
    if position >= s.len() - 6 {
        return (position + 1, 0);
    }

    let s_bytes = s.as_bytes();
    let version = bin_to_dec(&s_bytes[position..(position + 3)]);
    let type_id = bin_to_dec(&s_bytes[(position + 3)..(position + 6)]);

    let mut p = position + 6;
    let mut versions_sum = version;
    match type_id {
        4 => {
            let mut literal_value = 0;
            while s_bytes[p] == b'1' {
                literal_value = (literal_value << 4) + bin_to_dec(&s_bytes[(p + 1)..(p + 5)]);
                p += 5;
            }
            literal_value = (literal_value << 4) + bin_to_dec(&s_bytes[(p + 1)..(p + 5)]);
            p += 5;
        }
        _ => {
            let length_type_id = s_bytes[p];
            p += 1;
            match length_type_id == b'1' {
                true => {
                    let n_subpackets = bin_to_dec(&s_bytes[p..(p + 11)]);
                    p += 11;
                    for _ in 0..n_subpackets {
                        let (next_pos, v) = parse_packet(s, p);
                        p = next_pos;
                        versions_sum += v;
                    }
                }
                false => {
                    let subpackets_length = bin_to_dec(&s_bytes[p..(p + 15)]);
                    p += 15;
                    let end = p + subpackets_length;
                    while p < end {
                        let (next_pos, v) = parse_packet(s, p);
                        p = next_pos;
                        versions_sum += v;
                    }
                }
            }
        }
    }
    (p, versions_sum)
}

fn hex_to_bin(hex_string: &str) -> String {
    hex_string
        .chars()
        .filter_map(|c| {
            if let Ok(b) = u8::from_str_radix(&c.to_string(), 16) {
                Some(format!("{:04b}", b))
            } else {
                None
            }
        })
        .collect::<Vec<String>>()
        .join("")
}

fn bin_to_dec(bits: &[u8]) -> usize {
    bits.iter()
        .fold(0, |acc, x| (acc << 1) + (x - b'0') as usize)
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

    #[test]
    fn bin_to_dec_test() {
        assert_eq!(bin_to_dec("111".as_bytes()), 7);
        assert_eq!(bin_to_dec("10011".as_bytes()), 19);
        assert_eq!(bin_to_dec("00000".as_bytes()), 0);
        assert_eq!(bin_to_dec("0010".as_bytes()), 2);
    }

    #[test]
    fn hex_to_bin_test() {
        assert_eq!(hex_to_bin("D2FE28"), "110100101111111000101000");
        assert_eq!(
            hex_to_bin("38006F45291200"),
            "00111000000000000110111101000101001010010001001000000000"
        );
        assert_eq!(
            hex_to_bin("EE00D40C823060"),
            "11101110000000001101010000001100100000100011000001100000"
        );
    }
}
