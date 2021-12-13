const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]u8) u32 {
    var count: u32 = 0;

    var fish_it = std.mem.split(input, ",");
    while (fish_it.next()) |fish_raw| {
        count += @as(u32, switch (fish_raw[0]) {
            '0' => 1421,
            '1' => 1401,
            '2' => 1191,
            '3' => 1154,
            '4' => 1034,
            '5' => 950,
            '6' => 905,
            '7' => 779,
            else => 0,
        });
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
        \\3,4,3,1,2
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 5934);
}
