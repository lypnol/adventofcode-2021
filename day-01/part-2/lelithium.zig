const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

fn run(input: [:0]u8) u64 {
    var all_lines_it = std.mem.tokenize(input, "\n");
    var increases: u64 = 0;

    // three-wide sliding window <=> l[i] <= l[l]
    var li: u32 = std.fmt.parseInt(u32, all_lines_it.next().?, 10) catch unreachable;
    var lj: u32 = std.fmt.parseInt(u32, all_lines_it.next().?, 10) catch unreachable;
    var lk: u32 = std.fmt.parseInt(u32, all_lines_it.next().?, 10) catch unreachable;
    var ll: u32 = 0;

    while (all_lines_it.next()) |line| {
        ll = std.fmt.parseInt(u32, line, 10) catch unreachable;
        if (ll > li) {
            increases += 1;
        }
        li = lj;
        lj = lk;
        lk = ll;
    }
    return increases;
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
        \\199
        \\200
        \\208
        \\210
        \\200
        \\207
        \\240
        \\269
        \\260
        \\263
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 5);
}
