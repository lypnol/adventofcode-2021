use std::env::args;
use std::fmt::Display;
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

#[derive(PartialEq, Eq, Debug)]
struct JellyfishNumber {
    values: Vec<u32>,
    nesting: Vec<u8>,
}

impl Display for JellyfishNumber {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for v in &self.values {
            write!(f, "{} ", v)?;
        }
        writeln!(f)?;
        for v in &self.nesting {
            write!(f, "{} ", v)?;
        }
        Ok(())
    }
}

impl JellyfishNumber {
    fn empty() -> Self {
        Self {
            values: Vec::with_capacity(3),
            nesting: Vec::with_capacity(3),
        }
    }

    fn magnitude(&self) -> u32 {
        let mut stack = Vec::with_capacity(self.values.len());

        for (v, n) in self.values.iter().zip(self.nesting.iter()) {
            stack.push((*v, *n));
            while stack.len() >= 2 {
                let len = stack.len();
                let (last, last_nest) = *stack.last().unwrap();
                let (one_to_last, one_to_last_nest) = stack.get_mut(len - 2).unwrap();
                if *one_to_last_nest == last_nest {
                    *one_to_last_nest -= 1;
                    *one_to_last = 3 * (*one_to_last) + 2 * last;
                    stack.pop();
                } else {
                    break;
                }
            }
        }
        stack.last().unwrap().0
    }

    fn split_at(&mut self, v_idx: usize) {
        let nesting_mut = self.nesting.get_mut(v_idx).unwrap();
        *nesting_mut += 1;
        let new_nesting = *nesting_mut;

        let value_mut = self.values.get_mut(v_idx).unwrap();
        let left = *value_mut / 2;
        let right = left + (*value_mut % 2);
        *value_mut = left;
        self.values.insert(v_idx + 1, right);
        self.nesting.insert(v_idx + 1, new_nesting);
    }

    fn explode_at(&mut self, pair_idx: usize) {
        if pair_idx > 0 {
            self.values[pair_idx - 1] += self.values[pair_idx];
        }
        if pair_idx < self.values.len() - 2 {
            self.values[pair_idx + 2] += self.values[pair_idx + 1];
        }
        self.values[pair_idx] = 0;
        self.nesting[pair_idx] -= 1;
        self.values.remove(pair_idx + 1);
        self.nesting.remove(pair_idx + 1);
    }

    fn split_leftmost(&mut self) -> bool {
        for (i, v) in self.values.iter().enumerate() {
            if *v >= 10 {
                self.split_at(i);
                return true;
            }
        }
        false
    }

    fn explode_leftmost(&mut self) -> bool {
        for (i, n) in self.nesting.iter().enumerate() {
            if *n >= 5 {
                self.explode_at(i);
                return true;
            }
        }
        false
    }

    fn reduce(&mut self) {
        loop {
            if self.explode_leftmost() {
                continue;
            }
            if self.split_leftmost() {
                continue;
            }
            break;
        }
    }

    fn add_from_input(&mut self, input: &mut std::slice::Iter<u8>) {
        for n in &mut self.nesting {
            *n += 1;
        }
        let start_nest = if self.values.is_empty() { 0 } else { 1 };
        let mut curr_nest = start_nest;
        loop {
            match input.next().unwrap() {
                b',' => (),
                b'[' => curr_nest += 1,
                b']' => curr_nest -= 1,
                c => {
                    self.nesting.push(curr_nest);
                    self.values.push((*c - 48) as u32);
                }
            };
            if curr_nest == start_nest {
                break;
            }
        }
        self.reduce();
    }
}

fn run(input: &[u8]) -> u32 {
    let mut iter = input.iter();
    let mut number = JellyfishNumber::empty();
    number.add_from_input(&mut iter);
    loop {
        match iter.next() {
            None => break,
            Some(b'\n') => (),
            _ => panic!("Wrong input"),
        }
        number.add_from_input(&mut iter);
    }
    number.magnitude()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn parse(data: &str) -> JellyfishNumber {
        let mut iter = data.as_bytes().iter();
        let mut jf = JellyfishNumber::empty();
        jf.add_from_input(&mut iter);
        jf
    }

    #[test]
    fn parse_add() {
        let left = "[1,2]";
        let right = "[[3,4],5]";
        let mut jf = parse(left);
        jf.add_from_input(&mut right.as_bytes().iter());
        assert_eq!(jf, parse("[[1,2],[[3,4],5]]"))
    }

    #[test]
    fn magnitude() {
        assert_eq!(parse("[6,6]").magnitude(), 30);
        assert_eq!(parse("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude(), 445);
        assert_eq!(
            parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude(),
            3488
        );
        assert_eq!(parse("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude(), 1137);
    }

    #[test]
    fn split() {
        let mut left = JellyfishNumber {
            values: vec![0, 7, 4, 15, 0, 13, 1, 1],
            nesting: vec![4, 4, 3, 3, 4, 4, 2, 2],
        };
        left.split_at(3);
        let right = JellyfishNumber {
            values: vec![0, 7, 4, 7, 8, 0, 13, 1, 1],
            nesting: vec![4, 4, 3, 4, 4, 4, 4, 2, 2],
        };
        assert_eq!(left, right);
        left.split_at(6);
        let right = JellyfishNumber {
            values: vec![0, 7, 4, 7, 8, 0, 6, 7, 1, 1],
            nesting: vec![4, 4, 3, 4, 4, 4, 5, 5, 2, 2],
        };

        assert_eq!(left, right);
    }

    #[test]
    fn run_test() {
        assert_eq!(
            run("[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"
                .as_bytes()),
            4140
        )
    }
}
