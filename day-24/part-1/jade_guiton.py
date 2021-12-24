from tool.runners.python import SubmissionPy

from math import trunc
from time import perf_counter

def inter_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def inter_mul(a, b):
    (a1, a2), (b1, b2) = a, b
    if a1 >= 0 and b1 >= 0:
        return (a1*b1, a2*b2)
    bounds = [ax*bx for ax in a for bx in b]
    return (min(bounds), max(bounds))

def inter_idiv(a, b):
    if b == (1, 1): return a
    assert b == (26, 26)
    return (trunc(a[0] / 26), trunc(a[1] / 26))

def inter_mod(a, b):
    a1, a2 = a
    assert b == (26, 26) and a1 >= 0
    if a2-a1 + 1 >= 26 or a1 % 26 > a2 % 26:
        return (0, 25)
    else:
        return (a1 % 26, a2 % 26)

def inter_eql(a, b):
    (a1, a2), (b1, b2) = a, b
    if a2 < b1 or b2 < a1: # no overlap
        return (0, 0)
    elif a1 == a2 == b1 == b2:
        return (1, 1)
    else:
        return (0, 1)

def inter_contains(i, x):
    return i[0] <= x <= i[1]

def cst(x):
    return (x, x)

def parse_input(src):
    instr = []
    for line in src.strip().split("\n"):
        words = line.split(" ")
        op, out = words[0], words[1]
        arg = None
        if len(words) == 3:
            arg = words[2]
            arg = arg if arg in "xyzw" else cst(int(arg))
        instr.append((op, out, arg))
    return instr

inter_ops = {
    "add": inter_add,
    "mul": inter_mul,
    "div": inter_idiv,
    "mod": inter_mod,
    "eql": inter_eql,
}

def can_be_valid(instr, digits):
    next_digit = 0
    memory = {"x": cst(0), "y": cst(0), "z": cst(0), "w": cst(0)}
    for op, out, arg in instr:
        if isinstance(arg, str):
            arg = memory[arg]
        if op == "inp":
            memory[out] = digits[next_digit]
            next_digit += 1
        else:
            memory[out] = inter_ops[op](memory[out], arg)
    
    return inter_contains(memory["z"], 0)

def find_valid(instr, step, prefix=()):
    start, stop = (1, 10) if step == 1 else (9, 0)
    for digit in range(start, stop, step):
        new_prefix = (*prefix, cst(digit))
        if can_be_valid(instr, new_prefix + ((1,9),) * (14-len(new_prefix))):
            if len(new_prefix) == 14:
                return int("".join(str(start) for (start, stop) in new_prefix))
            res = find_valid(instr, step, new_prefix)
            if res == None: continue
            return res

class JadeGuitonSubmission(SubmissionPy):
    def run(self, s):
        return find_valid(parse_input(s), -1)

example = "inp w; mul x 0; add x z; mod x 26; div z 1; add x 12; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 7; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 1; add x 13; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 8; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 1; add x 13; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 10; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -2; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 4; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -10; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 4; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 1; add x 13; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 6; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -14; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 11; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -5; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 13; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 1; add x 15; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 1; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 1; add x 15; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 8; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -14; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 4; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 1; add x 10; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 13; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -14; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 4; mul y x; add z y; inp w; mul x 0; add x z; mod x 26; div z 26; add x -5; eql x w; eql x 0; mul y 0; add y 25; mul y x; add y 1; mul z y; mul y 0; add y w; add y 14; mul y x; add z y"
example = "\n".join(example.strip().split("; "))

def test_jade_guiton():
    """
    Run `python -m pytest ./day-24/part-1/jade_guiton.py` to test the submission.
    """
    assert JadeGuitonSubmission().run(example) == 79197919993985
