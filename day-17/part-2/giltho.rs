use std::env::args;
use std::time::Instant;

// This solution assumes that the zone is always under 0 vertically

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Zone {
    xs: i32,
    xe: i32,
    ys: i32,
    ye: i32,
}

impl Zone {
    fn velocity_ranges(&self) -> ((i32, i32), (i32, i32)) {
        let vxmin = ((((8 * self.xs + 1) as f32).sqrt() - 1.) / 2.).ceil() as i32;
        let vxmax = self.xe + 1;
        let vymin = self.ys;
        let vymax = -self.ys;
        ((vxmin, vxmax), (vymin, vymax))
    }
}

struct Projectile {
    x: i32,
    y: i32,
    vx: i32,
    vy: i32,
}

impl Projectile {
    fn step(&mut self) {
        self.x += self.vx;
        self.y += self.vy;
        self.vx = if self.vx == 0 { 0 } else { self.vx - 1 };
        self.vy -= 1;
    }

    fn reaches(&mut self, p: &Zone) -> bool {
        loop {
            if self.y < p.ys || (self.vx == 0 && self.x < p.xs) || self.x > p.xe {
                return false;
            }
            if self.x >= p.xs && self.y <= p.ye {
                return true;
            }
            self.step();
        }
    }
}

fn parse_number(input: &[u8]) -> (i32, usize) {
    let mut acc = 0;
    let mut sign = 1;
    let mut len = 0;
    for c in input {
        match c {
            b'-' => sign = -1,
            b'.' | b',' => break,
            c => acc = acc * 10 + (c - 48) as i32,
        }
        len += 1;
    }
    (acc * sign, len)
}

#[inline]
fn parse(input: &[u8]) -> Zone {
    let mut idx = 15;
    let (xs, xsl) = parse_number(&input[idx..]);
    idx += xsl + 2;
    let (xe, xel) = parse_number(&input[idx..]);
    idx += xel + 4;
    let (ys, ysl) = parse_number(&input[idx..]);
    idx += ysl + 2;
    let (ye, _) = parse_number(&input[idx..]);
    Zone { xs, xe, ys, ye }
}

fn run(input: &[u8]) -> i32 {
    let zone = parse(input);
    // There's probably a way to reduce a bit more the search space but well..
    // There's also probably ranges that we can know about.
    // If it's a bell throw that ends up vertically, and 2vx is in the range you don't have
    // to recompute or whatever equivalent
    let mut count = 0;
    let (rx, ry) = zone.velocity_ranges();
    for vx in rx.0..=rx.1 {
        for vy in ry.0..=ry.1 {
            if (Projectile { vx, vy, x: 0, y: 0 }).reaches(&zone) {
                count += 1;
            }
        }
    }
    count
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("target area: x=20..30, y=-10..-5".as_bytes()), 112);
    }
}
