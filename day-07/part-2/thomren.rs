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
    let numbers: Vec<isize> = input.split(",").map(|x| x.parse().unwrap()).collect();
    let mean = mean(&numbers);
    transport(&numbers, mean.floor() as isize).min(transport(&numbers, mean.ceil() as isize))
}

fn mean(array: &[isize]) -> f32 {
    array.into_iter().sum::<isize>() as f32 / (array.len() as f32)
}

fn transport(numbers: &[isize], encounter_point: isize) -> isize {
    numbers
        .iter()
        .map(|x| (x - encounter_point).abs() * ((x - encounter_point).abs() + 1))
        .sum::<isize>()
        / 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("16,1,2,0,4,2,7,1,2,14"), 168)
    }
}
