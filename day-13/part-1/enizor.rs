use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn fold_x(points: &mut Vec<(u16, u16)>, x0: u16) {
    for (x, _y) in points {
        if *x > x0 {
            *x = 2 * x0 - *x
        }
    }
}

fn fold_y(points: &mut Vec<(u16, u16)>, y0: u16) {
    for (_x, y) in points {
        if *y > y0 {
            *y = 2 * y0 - *y
        }
    }
}

fn run(input: &str) -> usize {
    // Your code goes here
    let (points, folds) = input.split_once("\n\n").unwrap();
    let mut paper = Vec::new();
    for l in points.lines() {
        let (x, y) = l.split_once(',').unwrap();
        paper.push((x.parse().unwrap(), y.parse().unwrap()));
    }
    let l = folds.lines().next().unwrap();
    let n = l[13..].parse().unwrap();
    if l.as_bytes()[11] == b'x' {
        fold_x(&mut paper, n);
    } else {
        fold_y(&mut paper, n);
    };
    paper.sort_unstable();
    paper.dedup();
    paper.len()
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
