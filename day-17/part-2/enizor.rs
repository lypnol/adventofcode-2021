use std::collections::HashSet;
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
    let p = input.find('.').unwrap();
    let x1: isize = input[15..p].parse().unwrap();
    assert!(x1 > 0);
    let c = p + input[p..].find(',').unwrap();
    let x2: isize = input[p + 2..c].parse().unwrap();
    assert!(x2 > x1);
    let p2 = c + input[c..].find('.').unwrap();
    let y1: isize = input[c + 4..p2].parse().unwrap();
    assert!(y1 < 0);
    let y2 = input[p2 + 2..].parse().unwrap();
    assert!(y2 < 0);
    assert!(y1 < y2);
    let mut count = 0;
    let count_smash = count_smash(y1, y2);
    let count_lob = count_lobs(y1, y2);
    let mut vset = HashSet::new();
    let mut vx = 1;
    while vx <= x2 {
        let mut v = vx - 1;
        let mut x = vx;
        let mut k = 1;
        while x <= x2 && v >= 0 {
            if x >= x1 && x <= x2 {
                if v == 0 {
                    // swish
                    for &(k2, vy) in count_lob.iter().chain(&count_smash) {
                        if k <= k2 {
                            vset.insert(vy);
                        }
                    }
                    for &(k2, vy) in &count_smash {
                        if k <= k2 {
                            vset.insert(vy);
                        }
                    }
                } else if k == 1 {
                    for vy in y1..=y2 {
                        vset.insert(vy);
                    }
                } else {
                    if k >= 3 {
                        // lob
                        for &(k2, vy) in &count_lob {
                            if k == k2 {
                                vset.insert(vy);
                            }
                            if k2 > k {
                                break;
                            }
                        }
                    }
                    for &(k2, vy) in &count_smash {
                        if k == k2 {
                            vset.insert(vy);
                        }
                        if k2 > k {
                            break;
                        }
                    }
                }
            }
            x += v;
            v -= 1;
            k += 1;
        }
        count += vset.len();
        vset.clear();
        vx += 1;
    }
    count
}

/// Vec of (nb steps, v0) for lobs
fn count_lobs(y1: isize, y2: isize) -> Vec<(usize, isize)> {
    // lobing and arriving at step k means
    let mut res = Vec::new();
    let mut vy = 1;
    while vy <= y1.abs() {
        let mut v = vy - 3;
        let mut y = 3 * vy - 3;
        let mut k = 3;
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
    res.sort_unstable();
    res
}

/// Vec of (nb steps, v0) for smashs
fn count_smash(y1: isize, y2: isize) -> Vec<(usize, isize)> {
    let mut res = Vec::new();
    let mut vy = 0;
    while vy >= y1 {
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
        vy -= 1;
    }
    res.sort_unstable();
    res
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("target area: x=20..30, y=-10..-5"), 112)
    }
}
