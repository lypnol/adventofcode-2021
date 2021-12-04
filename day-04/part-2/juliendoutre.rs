use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u32 {
    let mut lines = input.lines().filter(|line| !line.is_empty());

    let draws: Vec<u32> = lines
        .next()
        .unwrap()
        .split(',')
        .map(|part| part.parse::<u32>().unwrap())
        .collect();

    let mut rank = 0;
    let mut score = 0;

    let mut board = [0; 25];
    let mut counters = [0; 10];

    while let Some(line) = lines.next() {
        let mut total = 0;
        let mut marked_sum = 0;
        for i in 0..10 {
            counters[i] = 0;
        }

        line.split(' ')
            .filter(|line| !line.is_empty())
            .map(|part| part.trim().parse::<u32>().unwrap())
            .enumerate()
            .for_each(|(j, n)| {
                board[j] = n;
                total += n;
            });

        for i in 1..5 {
            lines
                .next()
                .unwrap()
                .split(' ')
                .filter(|line| !line.is_empty())
                .map(|part| part.trim().parse::<u32>().unwrap())
                .enumerate()
                .for_each(|(j, n)| {
                    board[i * 5 + j] = n;
                    total += n;
                });
        }

        for (n, draw) in draws.iter().enumerate() {
            if let Some(idx) = board.iter().position(|i| i == draw) {
                let i = idx / 5;
                let j = idx % 5;

                counters[i] += 1;
                counters[5 + j] += 1;
                marked_sum += draw;

                if counters[i] == 5 || counters[5 + j] == 5 {
                    if n >= rank {
                        rank = n;
                        score = draw * (total - marked_sum);
                    }

                    break;
                }
            }
        }
    }

    score
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

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
        assert_eq!(run(test_case), 1924)
    }
}
