const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

//const LENGTH = 5; // testing
const LENGTH = 12; // prod

fn run(input: [:0]u8) u32 {
    // Store the current bit position we're comparing
    var bit_pos: u8 = 0;

    // Stores bit counts to build final value.
    // Could be unrolled into 5 or 12 counters to gain some nanoseconds
    var bit_count = [_]u32{0} ** LENGTH;

    // Counts the number of lines in the input
    var line_count: u32 = 0;

    // Iterate over the full input
    for (input) |char| {
        //std.debug.print("char: {c}\n", .{char});
        switch (char) {
            '0' => bit_pos += 1, // Don't increase bit_count, increase bit_pos
            '1' => {
                bit_count[bit_pos] += 1; // Count that 1
                bit_pos += 1; // And increase bit_pos
            },
            '\n' => {
                line_count += 1; // EOL - count it
                bit_pos = 0; // and reset bit_count
            },
            else => unreachable,
        }
    }

    var gamma: u12 = 0; // showcase arbitrary bit length
    // var gamma: u5 = 0; // testing

    // comptime var to unroll
    comptime var _i: u8 = 0;
    // Unroll loop
    inline while (_i < LENGTH) : (_i += 1) {
        if (bit_count[_i] * 2 >= line_count) { // check if there's more 1s than 0s. Assuming >= based on part 2
            gamma += (@as(u12, 1) << (LENGTH - @intCast(u4, _i) - 1)); // we can only store gamma as epsilon = ~gamma (in u12)
            //gamma += (@as(u5, 1) << (LENGTH - @intCast(u3, _i) - 1)); // testing
        }
    }
    return @as(u32, gamma) * ~gamma; // preventively cast as u32 to avoid overflow
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
        \\00100
        \\11110
        \\10110
        \\10111
        \\10101
        \\01111
        \\00111
        \\11100
        \\10000
        \\11001
        \\00010
        \\01010
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 198);
}
