use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn parse<'a>(input: &'a str) -> impl Iterator<Item = isize> + 'a {
    input.lines().filter_map(|l| l.parse::<isize>().ok())
}

fn run(input: &str) -> isize {
    // Your code goes here
    parse(input)
        .fold((None, 0), |(prev, total), next| match prev {
            None => (Some(next), total),
            Some(prev) => (Some(next), total + if prev < next { 1 } else { 0 }),
        })
        .1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("199
200
208
210
200
207
240
269
260
263"),
            7
        )
    }
}
