import functools
from typing import Iterable, List, NamedTuple, Union
from tool.runners.python import SubmissionPy


HEX_MAP = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
}


class Tokenizer:
    def __init__(self, s: str):
        self.s = s
        self.pos = 0
        self.hexrem = 4

    def hexpos(self) -> int:
        return 4 * self.pos + 4 - self.hexrem

    def peek(self, n: int) -> int:
        if self.hexpos() + n > 4 * len(self.s):
            raise IndexError
        res = 0
        pos = self.pos
        hexrem = self.hexrem
        while n > 0:
            d = min(n, hexrem)
            n -= d
            mask = (1 << hexrem) - 1
            v = HEX_MAP[self.s[pos]] & mask
            hexrem -= d
            v >>= hexrem
            v <<= n
            res += v
            if hexrem == 0:
                hexrem = 4
                pos += 1
        return res

    def next(self, n: int) -> int:
        res = self.peek(n)
        q, r = divmod(self.hexrem - n - 1, 4)
        self.hexrem = r + 1
        self.pos -= q
        return res

    def __str__(self) -> str:
        return "".join("{:0>4}".format(bin(HEX_MAP[c])[2:]) for c in self.s)


class Operator(NamedTuple):
    version: int
    type_id: int
    length_type_id: int
    length: int
    packets: List["Packet"]  # type: ignore


class LiteralValue(NamedTuple):
    version: int
    type_id: int
    value: int


Packet = Union[Operator, LiteralValue]  # type: ignore


def parse_literal(tokenizer: Tokenizer, version: int, type_id: int) -> LiteralValue:
    next_mask = 0b10000
    val_mask = 0b01111
    res = 0
    while (block := tokenizer.next(5)) & next_mask:
        res <<= 4
        res += block & val_mask
    res <<= 4
    res += block
    return LiteralValue(version, type_id, res)


def parse_operator(tokenizer: Tokenizer, version: int, type_id: int) -> Operator:
    length_type_id = tokenizer.next(1)
    packets = []
    if length_type_id == 0:
        length = tokenizer.next(15)
        init_pos = tokenizer.hexpos()
        while tokenizer.hexpos() - init_pos < length:
            next_packet = parse_packet(tokenizer)
            packets.append(next_packet)
    elif length_type_id == 1:
        length = tokenizer.next(11)
        for _ in range(length):
            next_packet = parse_packet(tokenizer)
            packets.append(next_packet)
    return Operator(version, type_id, length_type_id, length, packets)


def parse_packet(tokenizer: Tokenizer) -> Packet:
    version = tokenizer.next(3)
    type_id = tokenizer.next(3)
    if type_id == 4:
        return parse_literal(tokenizer, version, type_id)
    return parse_operator(tokenizer, version, type_id)


def iterate_packet(packet: Packet) -> Iterable[Packet]:
    yield packet
    if isinstance(packet, Operator):
        for sub_packet in packet.packets:
            yield from iterate_packet(sub_packet)


def evaluate(packet: Packet) -> int:
    if isinstance(packet, LiteralValue):
        return packet.value
    elif isinstance(packet, Operator):
        if packet.type_id == 0:
            return sum(evaluate(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 1:
            return functools.reduce(lambda x, y: x * y, (evaluate(sub_packet) for sub_packet in packet.packets))
        elif packet.type_id == 2:
            return min(evaluate(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 3:
            return max(evaluate(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 5:
            left, right = packet.packets
            return 1 if evaluate(left) > evaluate(right) else 0
        elif packet.type_id == 6:
            left, right = packet.packets
            return 1 if evaluate(left) < evaluate(right) else 0
        elif packet.type_id == 7:
            left, right = packet.packets
            return 1 if evaluate(left) == evaluate(right) else 0
    raise ValueError


def parse(s: str) -> Tokenizer:
    return Tokenizer(s.strip())


class SkaschSubmission(SubmissionPy):
    def run(self, s: str) -> int:
        """
        :param s: input in string format
        :return: solution flag
        """
        # Your code goes here
        t = Tokenizer(s)
        return evaluate(parse_packet(t))


def test_skasch() -> None:
    """
    Run `python -m pytest ./day-16/part-2/skasch.py` to test the submission.
    """
    for s, expect in [
        ("C200B40A82", 3),
        ("04005AC33890", 54),
        ("880086C3E88112", 7),
        ("CE00C43D881120", 9),
        ("D8005AC2A8F0", 1),
        ("F600BC2D8F", 0),
        ("9C005AC2F8F0", 0),
        ("9C0141080250320F1802104A08", 1),
    ]:
        assert SkaschSubmission().run(s.strip()) == expect
