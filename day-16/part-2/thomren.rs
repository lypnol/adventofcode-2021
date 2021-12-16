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
    let _version = bin_to_dec(&s_bytes[position..(position + 3)]);
    let type_id = bin_to_dec(&s_bytes[(position + 3)..(position + 6)]);

    let mut p = position + 6;
    let res;
    match type_id {
        4 => {
            let mut literal_value = 0;
            while s_bytes[p] == b'1' {
                literal_value = (literal_value << 4) + bin_to_dec(&s_bytes[(p + 1)..(p + 5)]);
                p += 5;
            }
            literal_value = (literal_value << 4) + bin_to_dec(&s_bytes[(p + 1)..(p + 5)]);
            res = literal_value;
            p += 5;
        }
        _ => {
            let length_type_id = s_bytes[p];
            p += 1;
            match length_type_id == b'1' {
                true => {
                    let n_subpackets = bin_to_dec(&s_bytes[p..(p + 11)]);
                    p += 11;

                    let mut values = Vec::with_capacity(n_subpackets);
                    for _ in 0..n_subpackets {
                        let (next_pos, v) = parse_packet(s, p);
                        values.push(v);
                        p = next_pos;
                    }
                    res = fold_values(type_id, values)
                }
                false => {
                    let subpackets_length = bin_to_dec(&s_bytes[p..(p + 15)]);
                    p += 15;
                    let end = p + subpackets_length;
                    let mut values = vec![];
                    while p < end {
                        let (next_pos, v) = parse_packet(s, p);
                        values.push(v);
                        p = next_pos;
                    }
                    res = fold_values(type_id, values)
                }
            }
        }
    }
    (p, res)
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
        assert_eq!(run("C200B40A82"), 3);
        assert_eq!(run("04005AC33890"), 54);
        assert_eq!(run("880086C3E88112"), 7);
        assert_eq!(run("CE00C43D881120"), 9);
        assert_eq!(run("D8005AC2A8F0"), 1);
        assert_eq!(run("F600BC2D8F"), 0);
        assert_eq!(run("9C005AC2F8F0"), 0);
        assert_eq!(run("9C0141080250320F1802104A08"), 1);
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
