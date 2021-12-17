use std::env::args;
use std::fmt::Debug;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let target = parse_target(input);
    assert!(target.xmin >= 0);

    let dxmin = (-1. + (1. + 8. * target.xmin as f32).sqrt() / 2.).ceil() as isize;
    let dxrange = dxmin..=target.xmax;
    let dymax = target.ymin.abs().max(target.ymax.abs());
    dxrange
        .flat_map(|dx| (-dymax..=dymax).map(move |dy| (dx, dy)))
        .filter_map(|(dx, dy)| match Probe::new(dx, dy).shoot(&target) {
            ProbeResult {
                hit_target: false,
                ymax: _,
            } => None,
            ProbeResult {
                hit_target: true,
                ymax,
            } => Some(ymax),
        })
        .max()
        .unwrap_or(0)
}

#[derive(Debug, PartialEq, Eq)]
struct Target {
    xmin: isize,
    xmax: isize,
    ymin: isize,
    ymax: isize,
}

fn parse_target(target_str: &str) -> Target {
    let (_, coordinates) = target_str.split_once(": ").unwrap();
    let (x_range, y_range) = coordinates.split_once(", ").unwrap();
    let (xmin_str, xmax_str) = x_range.split_once("..").unwrap();
    let (ymin_str, ymax_str) = y_range.split_once("..").unwrap();
    let xmin: isize = xmin_str.split_at(2).1.parse().unwrap();
    let xmax: isize = xmax_str.parse().unwrap();
    let ymin: isize = ymin_str.split_at(2).1.parse().unwrap();
    let ymax: isize = ymax_str.parse().unwrap();
    Target {
        xmin,
        xmax,
        ymin,
        ymax,
    }
}

#[derive(Debug)]
struct Probe {
    x: isize,
    y: isize,
    dx: isize,
    dy: isize,
}

#[derive(Debug, PartialEq, Eq)]
struct ProbeResult {
    hit_target: bool,
    ymax: isize,
}

impl Probe {
    fn new(dx: isize, dy: isize) -> Self {
        Self { x: 0, y: 0, dx, dy }
    }

    fn shoot(&mut self, target: &Target) -> ProbeResult {
        let mut ymax = self.y;
        while !self.in_target(&target) && !self.overshot_target(&target) {
            self.step();
            ymax = ymax.max(self.y);
        }

        ProbeResult {
            hit_target: self.in_target(&target),
            ymax,
        }
    }

    fn step(&mut self) {
        self.x += self.dx;
        self.y += self.dy;
        self.dx -= self.dx.signum();
        self.dy -= 1;
    }

    fn in_target(&self, target: &Target) -> bool {
        self.x >= target.xmin
            && self.x <= target.xmax
            && self.y >= target.ymin
            && self.y <= target.ymax
    }

    fn overshot_target(&self, target: &Target) -> bool {
        (self.dy <= 0 && self.y < target.ymin) || self.x > target.xmax
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("target area: x=20..30, y=-10..-5"), 45)
    }

    #[test]
    fn parse_target_test() {
        assert_eq!(
            parse_target("target area: x=20..30, y=-10..-5"),
            Target {
                xmin: 20,
                xmax: 30,
                ymin: -10,
                ymax: -5
            }
        )
    }

    #[test]
    fn shoot_test() {
        let test_cases = vec![
            (7, 2, true, 3),
            (6, 3, true, 6),
            (9, 0, true, 0),
            (17, -4, false, 0),
            (6, 9, true, 45),
        ];
        let t = Target {
            xmin: 20,
            xmax: 30,
            ymin: -10,
            ymax: -5,
        };
        for (dx, dy, hit_target, ymax) in test_cases {
            let mut p = Probe::new(dx, dy);
            assert_eq!(p.shoot(&t), ProbeResult { hit_target, ymax })
        }
    }
}
