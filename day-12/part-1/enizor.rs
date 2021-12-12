use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[derive(Default, Clone, Copy)]
struct BitSet(usize);

impl BitSet {
    fn test(&self, pos: usize) -> bool {
        self.0 & (1 << pos) > 0
    }

    fn set(&mut self, pos: usize) {
        self.0 |= 1 << pos
    }
}

#[derive(Default, Clone, Copy)]
struct Cave(u64);

const SIZE_MASK: u64 = 1 << 63;
impl Cave {
    fn is_small(&self) -> bool {
        self.0 & SIZE_MASK > 0
    }
    fn set_small(&mut self) {
        self.0 |= SIZE_MASK;
    }
    fn connections(&self) -> IterIntSet {
        IterIntSet {
            set: self.0 & !SIZE_MASK,
            pos: 0,
        }
    }
    fn set_connection(&mut self, cave: usize) {
        self.0 |= 1 << cave;
    }
}

#[derive(Default, Clone, Copy)]
struct IterIntSet {
    set: u64,
    pos: usize,
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

struct CaveGraph {
    /// id => name
    /// 0 is always start and 1 is always end
    map_name: Vec<String>,
    /// id => cave
    caves: Vec<Cave>,
}

impl CaveGraph {
    fn new() -> Self {
        Self {
            map_name: vec!["start".into(), "end".into()],
            caves: vec![Cave::default(); 2],
        }
    }
    fn get_known_id(&self, id: &str) -> Option<usize> {
        self.map_name.iter().position(|s| *s == id)
    }
    fn new_id(&mut self, id: &str) -> usize {
        self.map_name.push(id.to_string());
        self.caves.push(Cave::default());
        self.map_name.len() - 1
    }
    fn get_id(&mut self, id: &str) -> usize {
        self.get_known_id(id).unwrap_or_else(|| self.new_id(id))
    }
    fn parse_line(&mut self, line: &str) {
        let (s1, s2) = line.split_once('-').unwrap();
        let id1 = self.get_id(s1);
        let id2 = self.get_id(s2);
        let c1 = &mut self.caves[id1];
        c1.set_connection(id2);
        if s1.as_bytes()[0] > b'Z' {
            c1.set_small();
        }
        let c2 = &mut self.caves[id2];
        c2.set_connection(id1);
        if s2.as_bytes()[0] > b'Z' {
            c2.set_small();
        }
    }

    fn search(&mut self) -> usize {
        self.search_aux(0, BitSet::default())
    }

    fn search_aux(&self, current_id: usize, mut visited: BitSet) -> usize {
        if current_id == 1 {
            // arrived at end
            return 1;
        }
        let current_cave = &self.caves[current_id];
        if current_cave.is_small() {
            visited.set(current_id);
        }
        let mut count = 0;
        for c in current_cave.connections() {
            if !visited.test(c) {
                count += self.search_aux(c, visited);
            }
        }
        count
    }
}

fn run(input: &str) -> usize {
    let mut cave_system = CaveGraph::new();
    for line in input.lines() {
        cave_system.parse_line(line);
    }
    cave_system.search()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_input = "start-A
start-b
A-c
A-b
b-d
A-end
b-end";
        let medium_input = "dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc";
        let large_input = "fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW";
        assert_eq!(run(small_input), 10);
        assert_eq!(run(medium_input), 19);
        assert_eq!(run(large_input), 226);
    }
}
