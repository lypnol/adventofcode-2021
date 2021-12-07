use std::collections::HashMap;
use std::env::args;
use std::num::ParseIntError;
use std::str::FromStr;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut sections = input.split("\n\n");
    let numbers = sections
        .next()
        .unwrap()
        .split(",")
        .map(|x| x.parse::<usize>().unwrap());

    let mut boards: Vec<Board> = sections.map(|s| Board::from_str(s).unwrap()).collect();

    for number in numbers {
        for board in &mut boards {
            if board.mark_number(number) && board.won {
                return board.score * number;
            }
        }
    }

    0
}

struct Board {
    score: usize,
    index: HashMap<usize, (usize, usize)>,
    col_remainings: [usize; 5],
    row_remainings: [usize; 5],
    won: bool,
}

impl FromStr for Board {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut score = 0;
        let mut index = HashMap::new();
        let col_remainings = [5; 5];
        let row_remainings = [5; 5];

        let mut lines = s.lines();
        for i in 0..5 {
            let line = lines.next().unwrap();
            let mut numbers = line.split_whitespace();
            for j in 0..5 {
                let n = numbers.next().unwrap().parse()?;
                score += n;
                index.insert(n, (i, j));
            }
        }

        Ok(Board {
            score,
            index,
            col_remainings,
            row_remainings,
            won: false,
        })
    }
}

impl Board {
    fn mark_number(&mut self, n: usize) -> bool {
        match self.index.get(&n) {
            Some((i, j)) => {
                self.score -= n;
                self.row_remainings[*i] -= 1;
                if self.row_remainings[*i] == 0 {
                    self.won = true;
                }
                self.col_remainings[*j] -= 1;
                if self.col_remainings[*j] == 0 {
                    self.won = true
                }
                true
            }
            None => false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(
                "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
8  2 23  4 24
21  9 14 16  7
6 10  3 18  5
1 12 20 15 19

3 15  0  2 22
9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
2  0 12  3  7"
            ),
            4512
        )
    }
}
