use std::collections::HashSet;
use std::env::args;
use std::time::Instant;

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let now = Instant::now();
    let output = run(&input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

enum Instruction {
    Up(u16),
    Left(u16),
}

struct Origami {
    paper: HashSet<(u16, u16)>,
    instructions: Vec<Instruction>,
}

impl Origami {
    fn from_str(input: &str) -> Self {
        let mut input = input.split("\n\n");
        let paper_str = input.next().unwrap().split('\n');
        let mut paper = HashSet::with_capacity(1024);
        for line in paper_str {
            let mut it = line.split(',');
            let x = it.next().unwrap().parse::<u16>().unwrap();
            let y = it.next().unwrap().parse::<u16>().unwrap();
            paper.insert((x, y));
        }
        let mut instructions = Vec::with_capacity(13);
        for line in input.next().unwrap().split('\n') {
            let instr = match line.as_bytes().get(11) {
                Some(b'x') => Instruction::Left(line[13..].parse::<u16>().unwrap()),
                Some(b'y') => Instruction::Up(line[13..].parse::<u16>().unwrap()),
                _ => panic!("Wrong input"),
            };
            instructions.push(instr);
        }

        instructions.reverse();

        Self {
            paper,
            instructions,
        }
    }

    fn size(&self) -> usize {
        self.paper.len()
    }

    fn fold_along_left(&mut self, x: u16) {
        self.paper = self
            .paper
            .iter()
            .map(|(i, j)| if *i > x { (x - (*i - x), *j) } else { (*i, *j) })
            .collect();
    }

    fn fold_along_top(&mut self, y: u16) {
        self.paper = self
            .paper
            .iter()
            .map(|(i, j)| if *j > y { (*i, y - (*j - y)) } else { (*i, *j) })
            .collect();
    }

    fn fold_once(&mut self) -> bool {
        let next_instr = match self.instructions.pop() {
            None => return false,
            Some(i) => i,
        };
        match next_instr {
            Instruction::Up(y) => self.fold_along_top(y),
            Instruction::Left(x) => self.fold_along_left(x),
        }
        true
    }
}

fn run(input: &str) -> usize {
    let mut origami = Origami::from_str(input);
    origami.fold_once();
    origami.size()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"),
            17
        )
    }
}
