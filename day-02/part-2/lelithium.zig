const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]u8) u64 {
    var all_lines_it = std.mem.split(input, "\n");
    var depth: u32 = 0; // unsigned because duh, can't climb out of the water
    var forward: u32 = 0; // no `backwards` instruction
    var aim: u32 = 0;

    while (all_lines_it.next()) |line| {
        var amount: u32 = @intCast(u32, line[line.len - 1]) - '0'; // single-digit char-to-int
        switch (line[0]) {
            'f' => {
                forward += amount;
                depth += (aim * amount);
            },
            'd' => {
                aim += amount;
            },
            'u' => {
                aim -= amount;
            },
            else => {
                @panic("Ruh roh scooby");
            },
        }
    }
    return depth * forward;
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
        \\forward 5
        \\down 5
        \\forward 8
        \\up 3
        \\down 8
        \\forward 2
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 900);
}
