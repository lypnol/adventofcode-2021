const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

//const LENGTH = 5; // testing
const LENGTH = 12; // prod

fn run(input: [:0]u8) u32 {
    // Stores the current bit position
    var bit_pos: u8 = 0;
    // Stores the number of set bits for the current bit position
    var bit_count: u32 = 0;

    // Stores all lines. 1000 lines should be enough (input is 999 lines)
    var all_lines = [_][LENGTH]u8{[_]u8{0} ** LENGTH} ** 1000;

    // Stores all "valid" indexes (i.e. that match the criteria defined by the puzzle)
    // Let's use 1001 as SKIP and 1002 as END
    var valid_line_idx = [_]u16{1002} ** 1000;  // Initialize as "empty" (only END)

    // Stores the number of "valid" lines
    var line_count: u16 = 0;
    
    for (input) |char| {
        // std.debug.print("char: {c}\n", .{char});
        // Check if we are at the end of a line
        if (bit_pos == LENGTH) {
            bit_pos = 0;  // reset bit_pos
            line_count += 1;  // count new line
            continue;  // skip over tests
        }
        // Build the first bit count (for all valid lines) so we don't have to re-walk the entire array
        if (bit_pos == 0 and char == '1') {
            bit_count += 1; // 
        }
        // Store the line
        all_lines[line_count][bit_pos] = char;
        bit_pos += 1;
    }
    line_count += 1;  // don't forget the final line

    var full_line_count = line_count; // store full line count to rebuild valid_line_idx afterwards
    var full_bit_count = bit_count; // also store bit count for first iteration

    // Stores if the current valid value for a bit is 1
    var bit_choice: bool = false;

    // Stores both target values indexes
    var oxygen_idx: u16 = 0;
    var co2_idx: u16 = 0;

    // Used to unroll the processing loop.
    // Iteration 0 sets o2, and iteration 1 sets co2
    comptime var iterations: u2 = 0;
    inline while (iterations < 2) : (iterations += 1){
        // (re)build valid_line_idx
        var _i: u16 = 0;
        while (_i < full_line_count) : (_i += 1) {
            valid_line_idx[_i] = _i;
        }
        // Reset bit_pos
        bit_pos = 0;
        // Reset bit count to first version
        bit_count = full_bit_count;
        // Reset line count
        line_count = full_line_count;
        main: while (bit_pos < LENGTH) : (bit_pos += 1) {
            //std.debug.print("{} bits for {} lines\n", .{bit_count, line_count});
            bit_choice = bit_count * 2 >= line_count;
            if (iterations == 1){
                // Flip bit_choice to select least bit.
                bit_choice = !bit_choice;
            }
            //std.debug.print("Now working on bit_pos {} (choice {})\n", .{bit_pos, bit_choice});
            // Reset bit count (look-ahead)
            bit_count = 0;
            for (valid_line_idx) |idx| {
                // Check if we're on a valid index
                if (idx == 1001) {
                    continue; // skip on 1001
                }
                if (idx == 1002) {
                    break; // end on 1002
                }
                // If there's only one valid line left, pick it
                if (line_count == 1){
                    if (iterations == 0){
                        oxygen_idx = idx;
                    }
                    else{
                        co2_idx = idx;
                    }
                    // Break out of the main loop
                    break :main;
                }
                //std.debug.print("\tUsing index {}\n", .{idx});
                //std.debug.print("\tProcessing line {s}\n", .{all_lines[idx]});
                if (bit_choice) {
                    if (all_lines[idx][bit_pos] == '1') {
                        //std.debug.print("\t\t{s}: bit {c} pos {} is valid\n", .{all_lines[idx], all_lines[idx][bit_pos], bit_pos});
                        // If we're at bit_pos == LENGTH, this is the final bit to check.
                        // We return the current line, as, if the puzzle is well built, we know it is unique.
                        if (bit_pos == LENGTH - 1) {
                            if (iterations == 0){
                                oxygen_idx = idx;
                            }
                            else{
                                co2_idx = idx;
                            }
                            break;
                        }
                        // If we're not done yet, actualize the next bit_count
                        if (all_lines[idx][bit_pos + 1] == '1')
                            bit_count += 1;
                    } else {
                        // Invalid line. Remove it from valid_line_idx, and decrease the line count.
                        valid_line_idx[idx] = 1001;
                        line_count -= 1;
                    }
                } else {
                    // See comments above.
                    if (all_lines[idx][bit_pos] == '0') {
                        //std.debug.print("\t\t{s}: bit {c} pos {} is valid\n", .{all_lines[idx], all_lines[idx][bit_pos], bit_pos});
                        if (bit_pos == LENGTH - 1) {
                            if (iterations == 0){
                                oxygen_idx = idx;
                            }
                            else{
                                co2_idx = idx;
                            }
                            break;
                        }
                        if (all_lines[idx][bit_pos + 1] == '1')
                            bit_count += 1;
                    } else {
                        valid_line_idx[idx] = 1001;
                        line_count -= 1;
                    }
                }
            }
        }
    }

    // Actually parse both values. This is faster than moving
    // these parse operations in while loop, as it allows better unrolling.
    var oxygen = std.fmt.parseUnsigned(u16, all_lines[oxygen_idx][0..], 2) catch unreachable;
    var co2 = std.fmt.parseUnsigned(u16, all_lines[co2_idx][0..], 2) catch unreachable;

    return @as(u32, oxygen) * co2;  // Cast as u32 to get some more room
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
    try std.testing.expect(run(&buf) == 230);
}
