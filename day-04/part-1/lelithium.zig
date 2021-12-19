const std = @import("std");

var a: *std.mem.Allocator = undefined;
const stdout = std.io.getStdOut().writer(); //prepare stdout to write in

const BINGO_GRID_SIZE: u8 = 5;

const STRIKED: u8 = 100; // numbers go up to 99
const INVALID: u8 = 101;

pub fn print_grid(grid: [25]u8) void {
    for (grid) |number, n_idx| {
        if (n_idx % 5 == 0) {
            std.debug.print("\n", .{});
        }
        if (number == STRIKED) {
            std.debug.print("XX ", .{});
        } else {
            std.debug.print("{:02} ", .{number});
        }
    }
    std.debug.print("\n", .{});
}

fn run(input: [:0]u8) u32 {
    var input_grid_splitter = std.mem.split(input, "\n\n");
    // Store input numbers, we'll deal with them once we've built the Grids
    var input_numbers = input_grid_splitter.next().?;

    // Store grids
    var grids = [_][25]u8{[_]u8{INVALID} ** 25} ** 100; // 100 in test input

    var grid_idx: u8 = 0; // 100 max

    while (input_grid_splitter.next()) |grid| : (grid_idx += 1) {
        // Split on both space and EOL
        var grid_splitter = std.mem.tokenize(grid, " \n");
        // Reset current index
        var cur_idx: u8 = 0;
        while (grid_splitter.next()) |raw_value| : (cur_idx += 1) {
            grids[grid_idx][cur_idx] = std.fmt.parseInt(u8, raw_value, 10) catch unreachable;
        }
    }

    // Deal with inputs

    var input_splitter = std.mem.tokenize(input_numbers, ",");
    var cur_grid_idx: u8 = 0;
    var drawn: u8 = 0;
    bingo_draw: while (input_splitter.next()) |raw_value| {
        drawn = std.fmt.parseInt(u8, raw_value, 10) catch unreachable;
        //std.debug.print("\nDRAWN {}\n", .{drawn});

        // Iterate over all stored grids
        cur_grid_idx = 0;
        while (cur_grid_idx < grid_idx) : (cur_grid_idx += 1) {
            //std.debug.print("GRID {}\n", .{cur_grid_idx});
            var cur_idx: u8 = 0;
            while (cur_idx < 25) : (cur_idx += 1) {
                if (grids[cur_grid_idx][cur_idx] == drawn) {
                    grids[cur_grid_idx][cur_idx] = STRIKED;
                    // Now check if there's a bingo
                    // Check current column
                    if (grids[cur_grid_idx][cur_idx % BINGO_GRID_SIZE] == STRIKED)
                        if (grids[cur_grid_idx][cur_idx % BINGO_GRID_SIZE + 1 * BINGO_GRID_SIZE] == STRIKED)
                            if (grids[cur_grid_idx][cur_idx % BINGO_GRID_SIZE + 2 * BINGO_GRID_SIZE] == STRIKED)
                                if (grids[cur_grid_idx][cur_idx % BINGO_GRID_SIZE + 3 * BINGO_GRID_SIZE] == STRIKED)
                                    if (grids[cur_grid_idx][cur_idx % BINGO_GRID_SIZE + 4 * BINGO_GRID_SIZE] == STRIKED)
                                        break :bingo_draw;
                    // check current line
                    var line_start: u8 = cur_idx - cur_idx % BINGO_GRID_SIZE;
                    // Can't unroll loop for some odd reason. Can do it manually though
                    if (grids[cur_grid_idx][line_start] == STRIKED)
                        if (grids[cur_grid_idx][line_start + 1] == STRIKED)
                            if (grids[cur_grid_idx][line_start + 2] == STRIKED)
                                if (grids[cur_grid_idx][line_start + 3] == STRIKED)
                                    if (grids[cur_grid_idx][line_start + 4] == STRIKED)
                                        break :bingo_draw;
                }
            }
            //print_grid(grids[cur_grid_idx]);
        }
    }

    var sum: u16 = 0;

    comptime var _i: u8 = 0;
    inline while (_i < BINGO_GRID_SIZE * BINGO_GRID_SIZE) : (_i += 1) {
        if (grids[cur_grid_idx][_i] != STRIKED) {
            sum += grids[cur_grid_idx][_i];
        }
    }

    return drawn * @as(u32, sum);
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
        \\7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1
        \\
        \\22 13 17 11  0
        \\ 8  2 23  4 24
        \\21  9 14 16  7
        \\ 6 10  3 18  5
        \\ 1 12 20 15 19
        \\
        \\ 3 15  0  2 22
        \\ 9 18 13 17  5
        \\19  8  7 25 23
        \\20 11 10 24  4
        \\14 21 16 12  6
        \\
        \\14 21 17 24  4
        \\10 16 15  9 19
        \\18  8 23 26 20
        \\22 11 13  6  5
        \\ 2  0 12  3  7
    ;
    var buf = input.*;
    try std.testing.expect(run(&buf) == 4512);
}
