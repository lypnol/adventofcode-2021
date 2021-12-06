use std::collections::HashMap;
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
    let mut n_lines_per_point = HashMap::new();

    for line in input.lines() {
        let (p1, p2) = line.split_once(" -> ").unwrap();
        let (p1, p2) = (Point::from_str(p1), Point::from_str(p2));

        if p1.0 == p2.0 {
            let x = p1.0;
            for y in range(p1.1, p2.1) {
                *n_lines_per_point.entry((x, y)).or_insert_with(|| 0) += 1;
            }
        } else if p1.1 == p2.1 {
            let y = p1.1;
            for x in range(p1.0, p2.0) {
                *n_lines_per_point.entry((x, y)).or_insert_with(|| 0) += 1;
            }
        } else if (p1.0 - p2.0).abs() == (p1.1 - p2.1).abs() {
            for (x, y) in range(p1.0, p2.0).zip(range(p1.1, p2.1)) {
                *n_lines_per_point.entry((x, y)).or_insert_with(|| 0) += 1;
            }
        }
    }

    n_lines_per_point.values().filter(|&&x| x > 1).count()
}

#[derive(Debug)]
struct Point(isize, isize);

impl Point {
    fn from_str(s: &str) -> Self {
        let (x, y) = s.split_once(",").unwrap();
        let (x, y) = (x.parse().unwrap(), y.parse().unwrap());
        Self(x, y)
    }
}

fn range(from: isize, to: isize) -> Box<dyn Iterator<Item = isize>> {
    if to == from {
        return Box::new(0..0);
    } else if to > from {
        return Box::new(from..=to);
    } else {
        return Box::new((to..=from).rev());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"),
            12
        )
    }
}
