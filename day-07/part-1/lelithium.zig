const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const INPUT_SIZE: u16 = 1000;

fn median(l: [INPUT_SIZE]u16, k: u16, input_len: u16) u16 {
    // for (l)|elt|{
    //     std.debug.print("{},", .{elt});
    // }
    //std.debug.print("\n", .{});
    if (k == 1)
        return l[0];
    const pivot: u16 = l[k];
    //std.debug.print("Using pivot [{}]{}\n",.{k/3, pivot});

    var lows = [_]u16{0} ** INPUT_SIZE;
    var highs = [_]u16{0} ** INPUT_SIZE;

    var low_count: u16 = 0;
    var high_count: u16 = 0;
    var pivot_count: u16 = 0;

    var idx: u16 = 0;
    while (idx < input_len) : (idx += 1) {
        //std.debug.print("Working on value {}\n", .{l[idx]});
        if (l[idx] < pivot) {
            //std.debug.print("\tAdding to lows\n", .{});
            lows[low_count] = l[idx];
            low_count += 1;
        } else if (l[idx] > pivot) {
            //std.debug.print("\tAdding to highs\n", .{});
            highs[high_count] = l[idx];
            high_count += 1;
        } else {
            //std.debug.print("\tAdding to pivots\n", .{});
            pivot_count += 1;
        }
    }
    if (k < low_count) {
        return median(lows, k, low_count);
    } else if (k < low_count + pivot_count) {
        return pivot;
    } else {
        return median(highs, k - low_count - 1, high_count);
    }
}

fn run(input: [:0]u8) u32 {
    var crabs = [_]u16{0} ** INPUT_SIZE;
    var last_crab_idx: u16 = 0;
    var crabos_it = std.mem.tokenize(input, ",\n");

    while (crabos_it.next()) |crabos| : (last_crab_idx += 1) {
        var crabval: u16 = std.fmt.parseInt(u16, crabos, 10) catch unreachable;
        crabs[last_crab_idx] = crabval;
    }

    const crab_median = median(crabs, INPUT_SIZE / 2, INPUT_SIZE);

    std.debug.print("crab median {}\n", .{crab_median});

    var fuel: u32 = 0;

    for (crabs) |crab| {
        if (crab > crab_median) {
            fuel += crab - crab_median;
        } else {
            fuel += crab_median - crab;
        }
    }
    return fuel;
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
        \\16,1,2,0,4,2,7,1,2,14
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 37);
}
