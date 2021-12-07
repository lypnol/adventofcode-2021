use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let mut numbers: Vec<isize> = input.split(",").map(|x| x.parse().unwrap()).collect();
    let encounter_point = median(&mut numbers);
    numbers.iter().map(|x| (x - encounter_point).abs()).sum()
}

fn median(array: &mut [isize]) -> isize {
    array.sort();
    if array.len() % 2 == 0 {
        (array[array.len() / 2 - 1] + array[array.len() / 2]) / 2
    } else {
        array[array.len() / 2]
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("16,1,2,0,4,2,7,1,2,14"), 37)
    }
}
