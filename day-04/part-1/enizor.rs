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
    let mut parts = input.split("\n\n");
    let draw = parts
        .next()
        .unwrap()
        .split(',')
        .map(|s| s.trim().parse().unwrap());
    let mut boards: Vec<Board> = parts.map(|s| s.parse().unwrap()).collect();
    for nb in draw {
        for b in &mut boards {
            if let Some(result) = b.insert_nb(nb) {
                return result;
            }
        }
    }
    0
}

type BoardNumber = u16;

#[derive(Clone, Default, Debug, PartialEq, Eq)]
struct Board {
    grid: [Option<BoardNumber>; 25],
    sum: usize,
}

impl Board {
    /// Inserts nb into the board and check the winning condition
    /// Returns the board's score when it wons
    fn insert_nb(&mut self, nb: BoardNumber) -> Option<usize> {
        let mut solutions = [true; 10];
        for (i, check) in self.grid.iter_mut().enumerate() {
            match *check {
                Some(x) if x == nb => {
                    *check = None;
                    self.sum -= nb as usize;
                }
                Some(_) => {
                    solutions[i / 5] = false;
                    solutions[5 + i % 5] = false;
                }
                None => {}
            }
        }
        if solutions.contains(&true) {
            Some(self.sum * nb as usize)
        } else {
            None
        }
    }
}

impl FromStr for Board {
    type Err = ParseIntError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let mut board = Board::default();
        for (i, nb_s) in s.split_whitespace().enumerate() {
            let nb: BoardNumber = nb_s.parse()?;
            board.sum += nb as usize;
            board.grid[i] = Some(nb);
        }
        Ok(board)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

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
    2  0 12  3  7";
        assert_eq!(run(input), 4512)
    }

    #[test]
    fn test_board() {
        let mut board: Board = "22 13 17 11  0
        8  2 23  4 24
    21  9 14 16  7
        6 10  3 18  5
        1 12 20 15 19"
            .parse()
            .unwrap();
        assert_eq!(
            board,
            Board {
                grid: [
                    Some(22),
                    Some(13),
                    Some(17),
                    Some(11),
                    Some(0),
                    Some(8),
                    Some(2),
                    Some(23),
                    Some(4),
                    Some(24),
                    Some(21),
                    Some(9),
                    Some(14),
                    Some(16),
                    Some(7),
                    Some(6),
                    Some(10),
                    Some(3),
                    Some(18),
                    Some(5),
                    Some(1),
                    Some(12),
                    Some(20),
                    Some(15),
                    Some(19)
                ],
                sum: 63 + 61 + 67 + 42 + 67
            }
        );
        for &i in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10].iter() {
            assert_eq!(board.insert_nb(i), None);
        }
        assert_eq!(board.insert_nb(16), Some(50 + 50 + 37));
    }
}
