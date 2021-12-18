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
    let mut hw = Homework::default();
    let mut lines = input.lines();
    let mut f = hw.parse_fish(lines.next().unwrap());
    for l in lines {
        let f2 = hw.parse_fish(l);
        f = hw.addition(f, f2);
        hw.reduce(f);
    }
    hw.magnitude(f)
}

type SnailFishId = usize;

#[derive(Debug, Clone, Copy, Default)]
struct SnailFish {
    left: SnailFishId,
    right: SnailFishId,
    parent: SnailFishId,
}

impl SnailFish {
    fn is_number(&self) -> bool {
        self.right == usize::MAX
    }
    fn has_parent(&self) -> bool {
        self.parent != usize::MAX
    }
    fn get_number(&self) -> u8 {
        assert!(self.is_number());
        self.left as u8
    }
    #[allow(unused)]
    fn get_left<'a>(&self, hw: &'a Homework) -> &'a SnailFish {
        &hw.arena[self.left]
    }
    #[allow(unused)]
    fn get_right<'a>(&self, hw: &'a Homework) -> &'a SnailFish {
        &hw.arena[self.right]
    }
    #[allow(unused)]
    fn get_left_mut<'a>(&self, hw: &'a mut Homework) -> &'a mut SnailFish {
        &mut hw.arena[self.left]
    }
    #[allow(unused)]
    fn get_right_mut<'a>(&self, hw: &'a mut Homework) -> &'a mut SnailFish {
        &mut hw.arena[self.right]
    }
}

#[derive(Default)]
struct Homework {
    arena: Vec<SnailFish>,
}

impl Homework {
    fn parse_fish(&mut self, line: &str) -> SnailFishId {
        let mut stack: Vec<(SnailFishId, SnailFishId)> = Vec::new();
        let mut last_id = usize::MAX;
        for c in line.as_bytes() {
            match c {
                b'[' => stack.push((usize::MAX, usize::MAX)),
                b']' => {
                    let mut pair = stack.pop().unwrap();
                    pair.1 = last_id;
                    let f = SnailFish {
                        left: pair.0,
                        right: pair.1,
                        parent: usize::MAX,
                    };
                    last_id = self.alloc(f);
                    self.arena[pair.0].parent = last_id;
                    self.arena[pair.1].parent = last_id;
                }
                b',' => stack.last_mut().unwrap().0 = last_id,
                x => {
                    let v = x - b'0';
                    let f = SnailFish {
                        left: v as usize,
                        right: usize::MAX,
                        parent: usize::MAX,
                    };
                    last_id = self.alloc(f);
                }
            }
        }
        assert!(stack.is_empty());
        last_id
    }

    fn alloc(&mut self, fish: SnailFish) -> SnailFishId {
        self.arena.push(fish);
        self.arena.len() - 1
    }

    fn addition(&mut self, left: SnailFishId, right: SnailFishId) -> SnailFishId {
        let fish = SnailFish {
            left,
            right,
            parent: usize::MAX,
        };
        let id = self.alloc(fish);
        self.arena[left].parent = id;
        self.arena[right].parent = id;
        id
    }

    fn reduce(&mut self, root: SnailFishId) {
        loop {
            match self.find_explode_reduce(root) {
                (Some(f), _) => self.explode(f),
                (None, Some(s)) => self.split(s),
                (None, None) => break,
            }
        }
    }

    fn find_explode_reduce(&self, root: SnailFishId) -> (Option<SnailFishId>, Option<SnailFishId>) {
        let mut stack = vec![(0, root)];
        let mut to_split = None;
        while let Some((depth, nid)) = stack.pop() {
            let f = self.arena[nid];
            if !f.is_number() {
                if depth >= 4 {
                    return (Some(nid), to_split);
                } else {
                    stack.push((depth + 1, f.right));
                    stack.push((depth + 1, f.left));
                }
            } else if to_split.is_none() && f.get_number() >= 10 {
                to_split = Some(nid);
            }
        }
        (None, to_split)
    }

    fn explode(&mut self, id: SnailFishId) {
        let f = self.arena[id];
        let l = self.arena[f.left];
        let lv = l.get_number();
        self.propagate_left(id, lv);
        let r = self.arena[f.right];
        let rv = r.get_number();
        self.propagate_right(id, rv);
        let p = &mut self.arena[id];
        p.right = usize::MAX;
        p.left = 0;
    }

    fn propagate_left(&mut self, mut id: SnailFishId, v: u8) {
        // up.clone()
        while self.arena[id].has_parent() {
            let f = self.arena[id];
            let parent = self.arena[f.parent];
            if parent.left == id {
                id = f.parent;
            } else {
                id = parent.left;
                break;
            }
        }
        if !self.arena[id].has_parent() {
            return;
        }
        // down
        while id != usize::MAX {
            let f = &mut self.arena[id];
            if f.is_number() {
                f.left += v as usize;
                return;
            } else {
                id = f.right
            }
        }
    }

    fn propagate_right(&mut self, mut id: SnailFishId, v: u8) {
        // up
        while self.arena[id].has_parent() {
            let f = self.arena[id];
            let parent = self.arena[f.parent];
            if parent.right == id {
                id = f.parent;
            } else {
                id = parent.right;
                break;
            }
        }
        // down
        if !self.arena[id].has_parent() {
            return;
        }
        while id != usize::MAX {
            let f = &mut self.arena[id];
            if f.is_number() {
                f.left += v as usize;
                return;
            } else {
                id = f.left
            }
        }
    }

    fn split(&mut self, id: SnailFishId) {
        let v = self.arena[id].get_number();
        let l = SnailFish {
            left: (v / 2) as usize,
            right: usize::MAX,
            parent: id,
        };
        let r = SnailFish {
            left: ((v + 1) / 2) as usize,
            right: usize::MAX,
            parent: id,
        };
        let l_id = self.alloc(l);
        let r_id = self.alloc(r);
        let f = &mut self.arena[id];
        f.left = l_id;
        f.right = r_id;
    }

    #[allow(unused)]
    fn to_string(&self, root: SnailFishId) -> String {
        let f = self.arena[root];
        if f.is_number() {
            f.left.to_string()
        } else {
            let mut res = String::new();
            res.push('[');
            // res.push('#');
            // res.push_str(&root.to_string());
            // res.push(':');
            res.push_str(&self.to_string(f.left));
            res.push(',');
            res.push_str(&self.to_string(f.right));
            res.push(']');
            res
        }
    }

    fn magnitude(&self, root: SnailFishId) -> usize {
        let f = self.arena[root];
        if f.is_number() {
            f.get_number() as usize
        } else {
            3 * self.magnitude(f.left) + 2 * self.magnitude(f.right)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]"),
            1384
        );
        assert_eq!(
            run("[1,1]
[2,2]
[3,3]
[4,4]"),
            445
        );
        assert_eq!(
            run("[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"),
            791
        );
        assert_eq!(
            run("[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]"),
            1137
        );
        assert_eq!(
            run("[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"),
            4140
        );
    }

    #[test]
    fn parse_test() {
        let mut hw = Homework::default();
        let s = hw.parse_fish("[1,2]");
        let f = hw.arena[s];
        assert_eq!(f.get_left(&hw).get_number(), 1);
        assert_eq!(f.get_right(&hw).get_number(), 2);
        // [[1,2],3]
        // [9,[8,7]]
        // [[1,9],[8,5]]
        let s = hw.parse_fish("[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]");
        let f = hw.arena[s];
        assert_eq!(f.get_left(&hw).get_left(&hw).get_left(&hw).get_number(), 9);
        assert_eq!(
            f.get_left(&hw)
                .get_left(&hw)
                .get_right(&hw)
                .get_left(&hw)
                .get_number(),
            3
        );
        assert_eq!(
            f.get_left(&hw)
                .get_left(&hw)
                .get_right(&hw)
                .get_right(&hw)
                .get_number(),
            8
        );
        assert_eq!(
            f.get_left(&hw)
                .get_right(&hw)
                .get_left(&hw)
                .get_left(&hw)
                .get_number(),
            0
        );
        assert_eq!(
            f.get_left(&hw)
                .get_right(&hw)
                .get_left(&hw)
                .get_right(&hw)
                .get_number(),
            9
        );
        assert_eq!(
            f.get_left(&hw).get_right(&hw).get_right(&hw).get_number(),
            6
        );
        assert_eq!(
            f.get_right(&hw)
                .get_left(&hw)
                .get_left(&hw)
                .get_left(&hw)
                .get_number(),
            3
        );
        assert_eq!(
            f.get_right(&hw)
                .get_left(&hw)
                .get_left(&hw)
                .get_right(&hw)
                .get_number(),
            7
        );
        assert_eq!(
            f.get_right(&hw)
                .get_left(&hw)
                .get_right(&hw)
                .get_left(&hw)
                .get_number(),
            4
        );
        assert_eq!(
            f.get_right(&hw)
                .get_left(&hw)
                .get_right(&hw)
                .get_right(&hw)
                .get_number(),
            9
        );
        assert_eq!(f.get_right(&hw).get_right(&hw).get_number(), 3);

        assert_eq!(hw.to_string(s), "[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]");
    }

    #[test]
    fn test_explode() {
        let mut hw = Homework::default();
        let root = hw.parse_fish("[[[[[9,8],1],2],3],4]");
        hw.reduce(root);
        assert_eq!(hw.to_string(root), "[[[[0,9],2],3],4]");
        let root = hw.parse_fish("[7,[6,[5,[4,[3,2]]]]]");
        hw.reduce(root);
        assert_eq!(hw.to_string(root), "[7,[6,[5,[7,0]]]]");
        let root = hw.parse_fish("[[6,[5,[4,[3,2]]]],1]");
        hw.reduce(root);
        assert_eq!(hw.to_string(root), "[[6,[5,[7,0]]],3]");
        let root = hw.parse_fish("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]");
        hw.reduce(root);
        assert_eq!(hw.to_string(root), "[[3,[2,[8,0]]],[9,[5,[7,0]]]]");
    }

    #[test]
    fn test_add_reduce() {
        let mut hw = Homework::default();

        let mut root = hw.parse_fish("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]");
        let new = hw.parse_fish("[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]");
        root = hw.addition(root, new);
        hw.reduce(root);
        let new = hw.parse_fish("[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]");
        root = hw.addition(root, new);
        hw.reduce(root);
        let new = hw.parse_fish("[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]");
        root = hw.addition(root, new);
        hw.reduce(root);
        assert_eq!(
            hw.to_string(root),
            "[[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]]"
        );
    }

    #[test]
    fn test_magnitude() {
        let mut hw = Homework::default();
        let f = hw.parse_fish("[9,1]");
        assert_eq!(hw.magnitude(f), 29);
        let f = hw.parse_fish("[[1,2],[[3,4],5]]");
        assert_eq!(hw.magnitude(f), 143);
        let f = hw.parse_fish("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]");
        assert_eq!(hw.magnitude(f), 1384);
        let f = hw.parse_fish("[[[[1,1],[2,2]],[3,3]],[4,4]]");
        assert_eq!(hw.magnitude(f), 445);
        let f = hw.parse_fish("[[[[3,0],[5,3]],[4,4]],[5,5]]");
        assert_eq!(hw.magnitude(f), 791);
        let f = hw.parse_fish("[[[[5,0],[7,4]],[5,5]],[6,6]]");
        assert_eq!(hw.magnitude(f), 1137);
        let f = hw.parse_fish("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]");
        assert_eq!(hw.magnitude(f), 3488);
        let f = hw.parse_fish("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]");
        assert_eq!(hw.magnitude(f), 4140);
    }
}
