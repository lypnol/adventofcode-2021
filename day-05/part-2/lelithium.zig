const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const GRID_SIZE: u16 = 1000;

fn run(input: [:0]u8) u32 {
    var grid = [_][GRID_SIZE]u16{[_]u16{0} ** GRID_SIZE} ** GRID_SIZE;

    var all_lines_it = std.mem.split(input, "\n");

    var count: u32 = 0;

    while (all_lines_it.next()) |line| {
        var line_it = std.mem.tokenize(line, ", ->");
        var x1 = std.fmt.parseInt(u16, line_it.next().?, 10) catch unreachable;
        var y1 = std.fmt.parseInt(u16, line_it.next().?, 10) catch unreachable;
        var x2 = std.fmt.parseInt(u16, line_it.next().?, 10) catch unreachable;
        var y2 = std.fmt.parseInt(u16, line_it.next().?, 10) catch unreachable;
        if (x1 == x2) {
            if (y2 >= y1) {
                while (y1 <= y2) : (y1 += 1) {
                    grid[y1][x1] += 1;
                    if (grid[y1][x1] == 2)
                        count += 1;
                }
            } else {
                while (y2 <= y1) : (y2 += 1) {
                    grid[y2][x1] += 1;
                    if (grid[y2][x1] == 2)
                        count += 1;
                }
            }
        } else if (y1 == y2) {
            if (x2 >= x1) {
                while (x1 <= x2) : (x1 += 1) {
                    grid[y1][x1] += 1;
                    if (grid[y1][x1] == 2)
                        count += 1;
                }
            } else {
                while (x2 <= x1) : (x2 += 1) {
                    grid[y1][x2] += 1;
                    if (grid[y1][x2] == 2)
                        count += 1;
                }
            }
        } else if (x1 < x2 and y1 < y2) {
            grid[y1][x1] += 1;
            if (grid[y1][x1] == 2)
                count += 1;
            while (x1 != x2) {
                x1 += 1;
                y1 += 1;
                grid[y1][x1] += 1;
                if (grid[y1][x1] == 2)
                    count += 1;
            }
        } else if (x1 < x2 and y1 > y2) {
            grid[y1][x1] += 1;
            if (grid[y1][x1] == 2)
                count += 1;
            while (x1 != x2) {
                x1 += 1;
                y1 -= 1;
                grid[y1][x1] += 1;
                if (grid[y1][x1] == 2)
                    count += 1;
            }
        } else if (x1 > x2 and y1 < y2) {
            grid[y1][x1] += 1;
            if (grid[y1][x1] == 2)
                count += 1;
            while (x1 != x2) {
                x1 -= 1;
                y1 += 1;
                grid[y1][x1] += 1;
                if (grid[y1][x1] == 2)
                    count += 1;
            }
        } else {
            grid[y1][x1] += 1;
            if (grid[y1][x1] == 2)
                count += 1;
            while (x1 != x2) {
                x1 -= 1;
                y1 -= 1;
                grid[y1][x1] += 1;
                if (grid[y1][x1] == 2)
                    count += 1;
            }
        }
    }
    return count;
}

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator); // create memory allocator for strings

    defer arena.deinit(); // clear memory

    var arg_it = std.process.args();

    _ = arg_it.skip(); // skip over exe name
    a = &arena.allocator; // get ref to allocator
    const input: [:0]u8 = try (arg_it.next(a)).?; // get the first argument

    const start: i128 = std.time.nanoTimestamp(); // start time
    const answer = run(input); // compute answer
    const elapsed_nano: f128 = @intToFloat(f128, std.time.nanoTimestamp() - start);
    const elapsed_milli: f64 = @floatCast(f64, @divFloor(elapsed_nano, 1_000_000));
    try stdout.print("_duration:{d}\n{}\n", .{ elapsed_milli, answer }); // emit actual lines parsed by AOC
}

test "ez" {
    const input =
        \\0,9 -> 5,9
        \\8,0 -> 0,8
        \\9,4 -> 3,4
        \\2,2 -> 2,1
        \\7,0 -> 7,4
        \\6,4 -> 2,0
        \\0,9 -> 2,9
        \\3,4 -> 1,4
        \\0,0 -> 8,8
        \\5,5 -> 8,2
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 12);
}
