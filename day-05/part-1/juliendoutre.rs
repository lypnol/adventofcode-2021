use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const WIDTH: usize = 1000;

fn run(input: &str) -> usize {
    let mut map: Vec<usize> = vec![0; WIDTH * WIDTH];

    for line in input.lines() {
        let (origin, destination) = line.split_once(" -> ").unwrap();
        let origin = origin.split_once(',').unwrap();

        let (x_1, y_1) = (
            origin.0.parse::<usize>().unwrap(),
            origin.1.parse::<usize>().unwrap(),
        );

        let destination = destination.split_once(',').unwrap();
        let (x_2, y_2) = (
            destination.0.parse::<usize>().unwrap(),
            destination.1.parse::<usize>().unwrap(),
        );

        if x_1 == x_2 {
            for i in std::cmp::min(y_1, y_2)..=std::cmp::max(y_1, y_2) {
                map[x_1 + WIDTH * i] += 1;
            }
        }

        if y_1 == y_2 {
            for j in std::cmp::min(x_1, x_2)..=std::cmp::max(x_1, x_2) {
                map[j + WIDTH * y_1] += 1;
            }
        }
    }

    map.iter().filter(|n| **n >= 2).count()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let test_case = "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2";

        assert_eq!(run(test_case), 5)
    }
}
