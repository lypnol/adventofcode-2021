use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("_parse");
    println!("{}", output);
}

fn fold_point(mut x: usize, mut size: usize, end_size: usize) -> usize {
    while x > end_size {
        if x > size / 2 {
            x = size - 1 - x;
        }
        size /= 2;
    }
    x
}

fn run(input: &str) -> String {
    // Your code goes here
    let (points, folds) = input.split_once("\n\n").unwrap();
    let mut start_y = 0;
    let mut start_x = 0;
    let mut end_y = 0;
    let mut end_x = 0;
    for l in folds.lines() {
        let n = l[13..].parse().unwrap();
        if l.as_bytes()[11] == b'x' {
            if start_x == 0 {
                start_x = n * 2 + 1;
            }
            end_x = n;
        } else {
            if start_y == 0 {
                start_y = n * 2 + 1;
            }
            end_y = n;
        };
    }
    let line_size = end_x + 1;
    let mut paper = vec![b'.'; line_size * end_y];
    for y in 0..end_y {
        paper[(y + 1) * line_size - 1] = b'\n';
    }
    for l in points.lines() {
        let (sx, sy) = l.split_once(',').unwrap();
        let x = fold_point(sx.parse().unwrap(), start_x, end_x);
        let y = fold_point(sy.parse().unwrap(), start_y, end_y);
        paper[y * line_size + x] = b'#';
    }
    String::from_utf8(paper).unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "6,10
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
fold along x=5
";
        let letter = "#####
#...#
#...#
#...#
#####
.....
.....
";
        assert_eq!(run(input), letter);
    }
}
