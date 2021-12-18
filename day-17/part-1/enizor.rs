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
    let p = input.find('.').unwrap();
    let x1 = input[15..p].parse().unwrap();
    assert!(x1 > 0);
    let c = p + input[p..].find(',').unwrap();
    let x2 = input[p + 2..c].parse().unwrap();
    assert!(x2 > x1);
    let p2 = c + input[c..].find('.').unwrap();
    let y1: isize = input[c + 4..p2].parse().unwrap();
    assert!(y1 < 0);
    let y2 = input[p2 + 2..].parse().unwrap();
    assert!(y2 < 0);
    assert!(y1 < y2);
    if can_swish(x1, x2) {
        return y1 * (y1 + 1) / 2;
    }
    let mut vx = 2;
    // same loop as part 2
    let lobs = count_lobs(y1, y2);
    let mut max = 0;
    while vx <= x2 + 1 {
        let mut v = vx - 2;
        let mut x = vx + vx - 1;
        let mut k = 2;
        while x <= x2 && v >= 0 {
            if x >= x1 && x <= x2 && k >= 3 {
                // lob
                for &(k2, vy) in &lobs {
                    if k == k2 {
                        max = max.max(vy);
                    }
                }
            }
            x += v;
            v -= 1;
            k += 1;
        }
        vx += 1;
    }
    0
}

fn can_swish(x1: isize, x2: isize) -> bool {
    let mut n = 1;
    let mut k = 2;
    while n <= x2 {
        if n >= x1 {
            return true;
        }
        n += k;
        k += 1;
    }
    false
}

/// Vec of (nb steps, v0) for lobs
fn count_lobs(y1: isize, y2: isize) -> Vec<(usize, isize)> {
    // lobing and arriving at step k means
    let mut res = Vec::new();
    let mut vy = 1;
    while vy < y1.abs() {
        let mut v = vy - 2;
        let mut y = vy + vy - 1;
        let mut k = 2;
        while y >= y1 {
            if y <= y2 {
                res.push((k, vy));
            }
            y += v;
            v -= 1;
            k += 1;
        }
        vy += 1;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("target area: x=20..30, y=-10..-5"), 45)
    }

    #[test]
    fn test_helpers() {
        assert!(can_swish(20, 30));
        assert!(!can_swish(11, 14));
        assert!(!can_swish(16, 17));
    }
}
