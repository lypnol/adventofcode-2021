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
    let cave: Vec<u8> = input
        .as_bytes()
        .into_iter()
        .filter(|&&x| x != b'\n')
        .map(|x| x - b'0')
        .collect();
    let width = input.lines().next().unwrap().len();
    let height = (input.trim().as_bytes().len() + 1) / (width + 1);

    let mut res = 0;
    for i in 0..height {
        for j in 0..width {
            if (i == 0 || cave[width * (i - 1) + j] > cave[width * i + j])
                && (j == 0 || cave[width * i + j - 1] > cave[width * i + j])
                && (i == (height - 1) || cave[width * (i + 1) + j] > cave[width * i + j])
                && (j == (width - 1) || cave[width * i + j + 1] > cave[width * i + j])
            {
                res += cave[width * i + j] as usize + 1;
            }
        }
    }

    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("2199943210
3987894921
9856789892
8767896789
9899965678"),
            15
        )
    }
}
