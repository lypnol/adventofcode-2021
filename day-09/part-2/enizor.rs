use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const GRID_SIZE: usize = 100;
type BasinId = u8;

/// Keeps track of current basins sizes
struct BasinsCollection {
    // basins: Vec<(BasinId, BasinId)>,
    basins: [usize; GRID_SIZE],
    best_3: [usize; 3],
    used_basins: u64,
}

impl BasinsCollection {
    fn new() -> Self {
        Self {
            basins: [0; GRID_SIZE],
            best_3: [0; 3],
            used_basins: 0,
        }
    }

    /// Adds a tile to the given basin
    fn add_tile(&mut self, b: BasinId) {
        // let p = self.find_basin(b);
        self.basins[b as usize] += 1;
        // p
    }

    /// Finds an available BasinId
    fn new_basin(&mut self) -> BasinId {
        let p = IterIntSet::from_set(!self.used_basins).next().unwrap();
        self.used_basins |= 1 << p;
        p as BasinId
    }

    /// Merges b2 into b1
    fn merge_basins(&mut self, b1: BasinId, b2: BasinId) {
        if b1 == b2 {
            return;
        }
        self.basins[b1 as usize] += self.basins[b2 as usize];
        self.basins[b2 as usize] = 0;
        self.used_basins &= !(1 << b2);
    }

    /// Consider as completed all basins that are not in new_basins
    fn cleanup(&mut self, new_basins: u64) {
        let dropped_basins = self.used_basins & !new_basins;
        for b in IterIntSet::from_set(dropped_basins) {
            self.update_best_3(self.basins[b]);
            self.basins[b] = 0;
            self.used_basins &= !(1 << b);
        }
    }

    fn update_best_3(&mut self, s: usize) {
        if s >= self.best_3[1] {
            self.best_3[0] = self.best_3[1];
            if s >= self.best_3[2] {
                self.best_3[1] = self.best_3[2];
                self.best_3[2] = s;
            } else {
                self.best_3[1] = s;
            }
        } else if s > self.best_3[0] {
            self.best_3[0] = s;
        }
    }

    fn score(&self) -> usize {
        self.best_3[0] * self.best_3[1] * self.best_3[2]
    }
}

/// Helper struct to iterate over a int set represented as a u64
struct IterIntSet {
    set: u64,
    pos: usize,
}
impl IterIntSet {
    fn from_set(s: u64) -> Self {
        Self { set: s, pos: 0 }
    }
}

impl Iterator for IterIntSet {
    type Item = usize;

    fn next(&mut self) -> Option<Self::Item> {
        if self.set >> self.pos == 0 {
            return None;
        }
        while self.pos < 64 && self.set & 1 << (self.pos) == 0 {
            if self.set & (0xff << self.pos) == 0 {
                self.pos += 8;
            } else {
                self.pos += 1;
            }
        }
        if self.pos >= 64 {
            None
        } else {
            self.pos += 1;
            Some(self.pos - 1)
        }
    }
}

fn run(input: &str) -> usize {
    let mut prev_line = [BasinId::MAX; GRID_SIZE + 1];
    let mut basins = BasinsCollection::new();
    for l in input.lines() {
        let mut new_basins = 0;
        for (i, &c) in l.as_bytes().iter().enumerate() {
            if c != b'9' {
                let up = prev_line[i + 1];
                let left = prev_line[i];
                let basin_id = if up != BasinId::MAX {
                    if left != BasinId::MAX && left != up {
                        basins.merge_basins(up, left);
                        // as left disappeared, we must replace it with up in the line
                        for v in &mut prev_line {
                            if *v == left {
                                *v = up;
                            }
                        }
                    }
                    up
                } else if left != BasinId::MAX {
                    left
                } else {
                    basins.new_basin()
                };
                basins.add_tile(basin_id);
                prev_line[i + 1] = basin_id;
                new_basins |= 1 << basin_id;
            } else {
                prev_line[i + 1] = BasinId::MAX;
            }
        }
        // basins.debug();
        basins.cleanup(new_basins);
    }
    // println!("{}", basins.basins.len());
    basins.cleanup(0);

    basins.score()
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
            1134
        )
    }
}
