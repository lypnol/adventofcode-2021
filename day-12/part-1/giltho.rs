use std::collections::HashMap;
use std::env::args;
use std::time::Instant;

// This solution assumes that there is no more than 16 different nodes.
// This is very important for the memoization function

trait Set<T> {
    fn empty() -> Self;

    fn with(&self, node: T) -> Self;

    fn contains(&self, node: T) -> bool;

    fn fold<B, F>(&self, init: B, f: F) -> B
    where
        F: FnMut(B, T) -> B;
}

trait GraphForDay {
    type Node: Copy;
    type NodeSet: Set<Self::Node> + Copy;

    fn end(&self) -> Self::Node;

    fn is_start(&self, node: Self::Node) -> bool;

    fn is_big(&self, node: Self::Node) -> bool;

    fn from_input(input: &[u8]) -> Self;

    fn predecessors(&self, node: Self::Node) -> Self::NodeSet;

    fn memoize(&mut self, node: Self::Node, visited: Self::NodeSet, v: u32);

    fn memoized(&self, node: Self::Node, visited: Self::NodeSet) -> Option<&u32>;

    fn count_paths(&mut self, current: Self::Node, visited: Self::NodeSet) -> u32 {
        if self.is_start(current) {
            return 1;
        }
        if visited.contains(current) {
            return 0;
        }
        if let Some(u) = self.memoized(current, visited) {
            return *u;
        }
        let new_visited = if self.is_big(current) {
            visited
        } else {
            visited.with(current)
        };
        let res = self
            .predecessors(current)
            .fold(0, |acc, p| acc + self.count_paths(p, new_visited));
        self.memoize(current, visited, res);
        res
    }

    fn count_paths_to_end(&mut self) -> u32 {
        self.count_paths(self.end(), Self::NodeSet::empty())
    }
}

#[derive(Clone, Copy)]
struct NSet(u32);

impl Set<u32> for NSet {
    #[inline(always)]
    fn empty() -> Self {
        NSet(0)
    }

    #[inline(always)]
    fn contains(&self, node: u32) -> bool {
        node & self.0 == node
    }

    #[inline(always)]
    fn with(&self, node: u32) -> Self {
        NSet(node | self.0)
    }

    #[inline(always)]
    fn fold<B, F>(&self, init: B, mut f: F) -> B
    where
        F: FnMut(B, u32) -> B,
    {
        let mut x = self.0;
        let mut t = 1;
        let mut res = init;
        while x > 0 {
            if x % 2 == 1 {
                res = f(res, t)
            }
            x >>= 1;
            t <<= 1;
        }
        res
    }
}

struct Caves {
    mem: HashMap<u32, u32>,
    bigs: NSet,
    graph: [NSet; 16],
}

impl GraphForDay for Caves {
    type Node = u32;
    type NodeSet = NSet;

    fn end(&self) -> u32 {
        1
    }

    fn is_start(&self, x: u32) -> bool {
        x == 32768
    }

    fn is_big(&self, x: u32) -> bool {
        self.bigs.contains(x)
    }

    fn memoize(&mut self, node: Self::Node, visited: Self::NodeSet, v: u32) {
        self.mem.insert((node << 16) | visited.0, v);
    }

    fn memoized(&self, node: Self::Node, visited: Self::NodeSet) -> Option<&u32> {
        self.mem.get(&((node << 16) | visited.0))
    }

    fn predecessors(&self, mut node: Self::Node) -> Self::NodeSet {
        let mut idx = 0;
        while node > 0 {
            idx += 1;
            node >>= 1;
        }
        self.graph[idx - 1]
    }

    fn from_input(input: &[u8]) -> Self {
        let mut graph = [NSet::empty(); 16];
        let mut bigs = NSet::empty();
        let mut name_tbl = HashMap::with_capacity(256);
        name_tbl.insert("start".as_bytes(), (15, 32768));
        name_tbl.insert("end".as_bytes(), (0, 1));
        let mut curr_idx = 1;
        let mut curr_mask = 2;
        for line in input.split(|x| *x == b'\n') {
            let split_idx = line.iter().position(|x| *x == b'-').unwrap();
            let (from, to) = line.split_at(split_idx);
            let to = &to[1..];
            let (from_idx, from_mask) = match name_tbl.get(from) {
                None => {
                    let x = (curr_idx, curr_mask);
                    name_tbl.insert(from, x);
                    curr_mask <<= 1;
                    curr_idx += 1;
                    x
                }
                Some(u) => *u,
            };
            let (to_idx, to_mask) = match name_tbl.get(to) {
                None => {
                    let x = (curr_idx, curr_mask);
                    name_tbl.insert(to, x);
                    curr_mask <<= 1;
                    curr_idx += 1;
                    x
                }
                Some(u) => *u,
            };
            graph[from_idx] = graph[from_idx].with(to_mask);
            graph[to_idx] = graph[to_idx].with(from_mask);
            if from[0] < 96
            /* upper_case */
            {
                bigs = bigs.with(from_mask);
            }
            if to[0] < 96
            /* upper_case */
            {
                bigs = bigs.with(to_mask);
            }
        }
        Self {
            graph,
            mem: HashMap::with_capacity(256),
            bigs,
        }
    }
}

fn main() {
    let input = args().nth(1).expect("Please provide an input");
    let input = input.as_bytes();
    let now = Instant::now();
    let output = run(input);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &[u8]) -> u32 {
    Caves::from_input(input).count_paths_to_end()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn smallest() {
        assert_eq!(
            run("start-A
start-b
A-c
A-b
b-d
A-end
b-end"
                .as_bytes()),
            10
        )
    }

    #[test]
    fn medium() {
        assert_eq!(
            run("dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"
                .as_bytes()),
            19
        )
    }

    #[test]
    fn biggest() {
        assert_eq!(
            run("fs-end
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
start-RW"
                .as_bytes()),
            226
        )
    }
}
