use std::collections::{HashMap, HashSet};
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
    let mut graph = HashMap::<&str, Vec<&str>>::new();

    for line in input.lines() {
        let (src, dst) = line.split_once('-').unwrap();

        if let Some(children) = graph.get_mut(src) {
            children.push(dst);
        } else {
            graph.insert(src, vec![dst]);
        }

        if let Some(children) = graph.get_mut(dst) {
            children.push(src);
        } else {
            graph.insert(dst, vec![src]);
        }
    }

    let mut visited = HashSet::<&str>::new();

    traverse(&graph, &mut visited, "start")
}

fn traverse<'a>(
    graph: &HashMap<&'a str, Vec<&'a str>>,
    visited: &mut HashSet<&'a str>,
    node: &'a str,
) -> usize {
    if node == "end" {
        return 1;
    }

    if node.chars().next().unwrap().is_lowercase() {
        visited.insert(node);
    }

    if let Some(children) = graph.get(node) {
        let children = children
            .iter()
            .filter(|&child| !visited.contains(child))
            .map(|child| *child)
            .collect::<Vec<&str>>();

        let mut count = 0;

        for child in children {
            count += traverse(graph, &mut visited.clone(), child);
        }

        count
    } else {
        0
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test_1() {
        let test_case = "start-A
start-b
A-c
A-b
b-d
A-end
b-end";

        assert_eq!(run(test_case), 10);
    }

    #[test]
    fn run_test_2() {
        let test_case = "dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc";
        assert_eq!(run(test_case), 19);
    }

    #[test]
    fn run_test_3() {
        let test_case = "fs-end
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
        assert_eq!(run(test_case), 226);
    }
}
