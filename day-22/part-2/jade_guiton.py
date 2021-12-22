from tool.runners.python import SubmissionPy

import time
import bisect

"""
The state of the reactor core is stored as a tree with 3 levels, one for each axis X, Y, Z.
In each node, we store a sorted list of relevant coordinates along that axis.
- For the upper two levels (X and Y), we also store a list of child nodes,
  one "between" each pair of coordinates.
  The nodes are represented as (list of coordinates, list of child nodes).
- For the last level (Z), the coordinate list doubles as a list of "ON" intervals on the Z axis:
  E.g. [1,3,4,6] corresponds to the intervals [1,3) and [4,6).
Based on the position of an interval in the tree, we can figure out what cuboid in 3D space
it corresponds to.
"""

# This makes a deep copy of a node (faster than copy.deepcopy)
def copy_child_node(node, axis):
    if axis == 1: # 3rd level nodes only store coordinates, not child nodes
        return list(node)
    else:
        return (list(node[0]), [list(child) for child in node[1]])

# Adds 'coord' as a relevant coordinate in a 1st/2nd level node
def split_node(node, coord, axis):
    i = bisect.bisect_left(node[0], coord)
    # If the coordinate is not already in the list
    if i == len(node[0]) or node[0][i] != coord:
        node[0].insert(i, coord)
        if 0 <= i-1 < len(node[1]):
            # Split a child node in 2
            node[1].insert(i, copy_child_node(node[1][i-1], axis))
        elif len(node[0]) >= 2:
            # Add a new empty node at the start/end
            new_node = ([], []) if axis == 0 else []
            if i == 0:
                node[1].insert(0, new_node)
            elif i == len(node[0])-1:
                node[1].append(new_node)
    return i

# Finds the interval of child nodes that corresponds to the coordinates [x1, x2)
def find_interval(node, x1, x2, axis):
    i1 = split_node(node, x1, axis)
    i2 = split_node(node, x2, axis)
    return range(i1, i2)

# Adds an interval to a flat list of intervals
def add_interval(inter, start, stop):
    i1 = bisect.bisect_left(inter, start) // 2 * 2
    i2 = bisect.bisect_right(inter, stop)
    if i2 % 2 == 1: i2 += 1 # More efficient than using math.ceil(x / 2) * 2
    if i2 > i1:
        x1, x2 = inter[i1], inter[i2-1]
        if x1 < start:
            start = x1
        if x2 > stop:
            stop = x2
    inter[i1:i2] = [start, stop]

# Removes an interval from a flat list of intervals
def remove_interval(inter, start, stop):
    i1 = bisect.bisect_right(inter, start) // 2 * 2
    i2 = bisect.bisect_left(inter, stop)
    if i2 % 2 == 1: i2 += 1
    rep = []
    if i2 > i1:
        x1, x2 = inter[i1], inter[i2-1]
        if x1 < start:
            rep += [x1, start]
        if x2 > stop:
            rep += [stop, x2]
    inter[i1:i2] = rep

# Simplifies a node by merging identical adjacent child nodes
def simplify(node, interval):
    start, stop = interval.start - 1, interval.stop + 1 # Expand by 1
    i = max(0, start)
    i_end = min(stop, len(node[1]))
    while i+1 < i_end:
        if node[1][i] == node[1][i+1]:
            node[1].pop(i+1)
            node[0].pop(i+1)
            i_end -= 1
        else:
            i += 1

"""
Sets a cuboid to ON/OFF by:
- adding the relevant coordinates to the first 2 layers of the tree,
- adding/removing the appropriate intervals on the 3rd layer,
- simplifying the nodes on the first 2 layers.
"""
def set_cuboid(tree, xs, ys, zs, state):
    x_int = find_interval(tree, *xs, 0)
    for i1 in x_int:
        y_node = tree[1][i1]
        y_int = find_interval(y_node, *ys, 1)
        for i2 in y_int:
            z_node = y_node[1][i2]
            if state:
                add_interval(z_node, *zs)
            else:
                remove_interval(z_node, *zs)
        simplify(y_node, y_int)
    simplify(tree, x_int)

def parse_range(s):
    [a, b] = s.split("..")
    return (int(a), int(b) + 1)

# Iterates over each child of a node + the size of the interval it is in
def get_intervals(node):
    for i, child in enumerate(node[1]):
        yield (child, node[0][i+1] - node[0][i])

class JadeGuitonSubmission(SubmissionPy):
    def run(self, s):
        tree = ([], [])
        
        for i, line in enumerate(s.split("\n")):
            if len(line) == 0: continue
            state, cuboid = tuple(line.split(" "))
            state = True if state == "on" else False
            xs, ys, zs = tuple(parse_range(interval[2:]) for interval in cuboid.split(","))
            set_cuboid(tree, xs,ys,zs, state)
        
        total = 0
        for y_node, dx in get_intervals(tree):
            for z_node, dy in get_intervals(y_node):
                for z1, z2 in zip(z_node[::2], z_node[1::2]):
                    total += dx*dy*(z2-z1)
        return total

example = """
on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507
"""

def test_jade_guiton():
    """
    Run `python -m pytest ./day-22/part-2/jade_guiton.py` to test the submission.
    """
    assert (
        JadeGuitonSubmission().run(example) == 2758514936282235
    )
