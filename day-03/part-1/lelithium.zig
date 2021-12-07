const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

//const LENGTH = 5; // testing
const LENGTH = 12; // prod

//const MAJORITY_THRESHOLD = 6; // testing
const MAJORITY_THRESHOLD = 500; // prod

fn run(input: [:0]u8) u32 {
    // Store the current bit position we're comparing
    comptime var bit_pos: u8 = 0;

    // Stores bit counts to build final value.
    // Could be unrolled into 5 or 12 counters to gain some nanoseconds
    var bit_count = [_]u32{0} ** LENGTH;

    var line_count: u32 = 0;

    var gamma: u12 = 0; // showcase arbitrary bit length
    // var gamma: u5 = 0; // testing

    // Iterate over the full input
    var i: usize = 0;

    inline while (bit_pos < LENGTH) : (bit_pos += 1) {
        //std.debug.print("current bit pos: {}\n", .{bit_pos});
        i = bit_pos;
        while (i < input.len) {
            if (bit_count[bit_pos] >= MAJORITY_THRESHOLD or line_count > MAJORITY_THRESHOLD) {
                // Further operations won't change result
                break;
            }
            //std.debug.print("{c}\n", .{input[i]});
            if (input[i] == '1') {
                bit_count[bit_pos] += 1;
            }
            i += 13; //prod
            //i += 6; //test
        }
    }

    bit_pos = 0;
    inline while (bit_pos < LENGTH) : (bit_pos += 1) {
        if (bit_count[bit_pos] >= MAJORITY_THRESHOLD) { // check if there's more 1s than 0s. Assuming >= based on part 2
            gamma += (@as(u12, 1) << (LENGTH - @intCast(u4, bit_pos) - 1)); // we can only store gamma as epsilon = ~gamma (in u12)
            //gamma += (@as(u5, 1) << (LENGTH - @intCast(u3, bit_pos) - 1)); // testing
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
