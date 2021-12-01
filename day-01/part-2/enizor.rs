use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output.unwrap_or_default());
}

fn run(input: &str) -> Option<usize> {
    let mut res = 0;
    let mut lines = input.lines();
    let mut window = [0u16; 4];
    for depth in &mut window {
        *depth = lines.next()?.parse().ok()?;
    }
    let mut offset = 3;
    for line in lines {
        if window[offset] > window[(offset + 1) % 4] {
            res += 1;
        }
        offset = (offset + 1) % 4;
        window[offset] = line.parse().ok()?;
    }
    if window[offset] > window[(offset + 1) % 4] {
        res += 1;
    }
    Some(res)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let example = r"199
200
208
210
200
207
240
269
260
263
";
        assert_eq!(run(example), Some(5))
    }
}
