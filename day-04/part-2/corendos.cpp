#include <iostream>
#include <string>
#include <chrono>
#include <ctime>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cstdarg>
#include <cmath>

typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;

typedef int64_t i64;
typedef int32_t i32;
typedef int16_t i16;
typedef int8_t i8;

typedef size_t usize;

#define NO_LOG 1

void print(const char *format, ...) {
#if !NO_LOG
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
#endif
}

struct Input {
    char *data;
    usize size;
};

Input make_input_from_string(std::string &s) {
    Input input = {s.data(), s.size()};
    return input;
}

struct Iterator {
    char *data;
    char *current;
    usize size;
};

Iterator make_iterator(Input *input) {
    Iterator it = {input->data, input->data, input->size};
    return it;
}

inline u32 is_valid(Iterator *it) {
    return (it->current - it->data) < it->size;
}

inline bool is_number(char c) {
    return c >= '0' && c <= '9';
}

inline void skip_to(Iterator* it, char c) {
    if (is_valid(it) && it->current[0] == c) return;
    while (is_valid(it)) {
        it->current++;
        if (it->current[0] == c) return;
    }
}

inline void skip_to_first_after(Iterator* it, char c) {
    skip_to(it, c);
    it->current++;
}

struct Grid {
    u8 lines[5][5];
    u8 columns[5][5];
};

struct Context {
    u8 drawing[128];
    u8 drawing_order[128];
    u8 drawing_count;
    u8 grid_count;
    u8 index_winning_grid;
    u8 drawing_win;
    Grid grids[128];
};

inline void skip_to_next_grid(Iterator* it) {
    if (is_valid(it) && (is_number(it->current[0]) || it->current[0] == ' ')) return;
    while (is_valid(it)) {
        it->current++;
        if (is_number(it->current[0]) || it->current[0] == ' ') return;
    }
}

inline u8 to_u8(u16 two_bytes) {
    u8 low = ((two_bytes & 0xFF00) >> 8) - '0';
    u8 high = (two_bytes & 0xFF) - '0';
    // NOTE(Corentin): Subtracting '0' will make the u8 to wrap
    high = high > '9' ? 0 : high * 10;
    return low + high;
}

inline void process_line(Iterator *it, Context *context) {}

void load_drawing(Iterator *it, Context *context) {
    u32 current_number = 0;
    while(is_valid(it) && it->current[0] != '\n') {
        if (is_number(it->current[0])) {
            current_number = current_number * 10 + (it->current[0] - 48);
        } else {
            context->drawing[context->drawing_count] = current_number;
            context->drawing_count++;
            context->drawing_order[current_number] = context->drawing_count;
            current_number = 0;
        }
        it->current++;
    }
    context->drawing[context->drawing_count] = current_number;
    context->drawing_count++;
    context->drawing_order[current_number] = context->drawing_count;
}

struct GridProcessing {
    u8 line_index_of_win[5];
    u8 column_index_of_win[5];
};

inline u8 grid_min(u8 a, u8 b, u8 c, u8 d, u8 e) {
    return std::min(std::min(std::min(a, b), std::min(c, d)), e);
}

void load_and_process_grid_line(Iterator *it, Context *context, GridProcessing *processing, u32 line_index) {
    for (u8 column = 0;column < 5;++column) {
        u8 number = to_u8(*(u16*)it->current);
        context->grids[context->grid_count].lines[line_index][column] = number;
        context->grids[context->grid_count].columns[column][line_index] = number;
        
        u8 order = context->drawing_order[number];
        
        processing->line_index_of_win[line_index] = std::max(processing->line_index_of_win[line_index], (u8)(order - 1));
        processing->column_index_of_win[column] = std::max(processing->column_index_of_win[column], (u8)(order - 1));
        
        it->current += 3;
    }
}

void load_and_process_grid(Iterator *it, Context *context) {
    GridProcessing processing = {0};
    for (u8 line = 0;line < 5;++line) {
        load_and_process_grid_line(it, context, &processing, line);
    }
    
    u8 line_index_of_win = grid_min(processing.line_index_of_win[0],
                                    processing.line_index_of_win[1],
                                    processing.line_index_of_win[2],
                                    processing.line_index_of_win[3],
                                    processing.line_index_of_win[4]);
    u8 column_index_of_win = grid_min(processing.column_index_of_win[0],
                                      processing.column_index_of_win[1],
                                      processing.column_index_of_win[2],
                                      processing.column_index_of_win[3],
                                      processing.column_index_of_win[4]);
    
    u8 grid_winning_index = std::min(line_index_of_win, column_index_of_win) + 1;
    if (grid_winning_index > context->drawing_win) {
        context->index_winning_grid = context->grid_count;
        context->drawing_win = grid_winning_index - 1;
    }
    context->grid_count++;
}

u32 compute_score(Iterator *it, Context *context) {
    Grid *winning_grid = context->grids + context->index_winning_grid;
    u32 unmarked_sum = 0;
    for (u8 y = 0;y < 5;++y) {
        for (u8 x = 0;x < 5;++x) {
            u8 number = winning_grid->lines[y][x];
            bool keep = context->drawing_order[number] - 1 > context->drawing_win;
            //print("Winning grid [%d][%d] = %d and is %s\n", y, x, number, keep ? "kept" : "ignored");
            unmarked_sum += keep ? number : 0;
        }
    }
    return unmarked_sum * context->drawing[context->drawing_win];
}

void print_grid_with_lines(Grid *grid) {
    print("%2d %2d %2d %2d %2d\n", grid->lines[0][0], grid->lines[0][1], grid->lines[0][2], grid->lines[0][3], grid->lines[0][4]);
    print("%2d %2d %2d %2d %2d\n", grid->lines[1][0], grid->lines[1][1], grid->lines[1][2], grid->lines[1][3], grid->lines[1][4]);
    print("%2d %2d %2d %2d %2d\n", grid->lines[2][0], grid->lines[2][1], grid->lines[2][2], grid->lines[2][3], grid->lines[2][4]);
    print("%2d %2d %2d %2d %2d\n", grid->lines[3][0], grid->lines[3][1], grid->lines[3][2], grid->lines[3][3], grid->lines[3][4]);
    print("%2d %2d %2d %2d %2d\n", grid->lines[4][0], grid->lines[4][1], grid->lines[4][2], grid->lines[4][3], grid->lines[4][4]);
}

void print_grid_with_columns(Grid *grid) {
    print("%2d %2d %2d %2d %2d\n", grid->columns[0][0], grid->columns[1][0], grid->columns[2][0], grid->columns[3][0], grid->columns[4][0]);
    print("%2d %2d %2d %2d %2d\n", grid->columns[0][1], grid->columns[1][1], grid->columns[2][1], grid->columns[3][1], grid->columns[4][1]);
    print("%2d %2d %2d %2d %2d\n", grid->columns[0][2], grid->columns[1][2], grid->columns[2][2], grid->columns[3][2], grid->columns[4][2]);
    print("%2d %2d %2d %2d %2d\n", grid->columns[0][3], grid->columns[1][3], grid->columns[2][3], grid->columns[3][3], grid->columns[4][3]);
    print("%2d %2d %2d %2d %2d\n", grid->columns[0][4], grid->columns[1][4], grid->columns[2][4], grid->columns[3][4], grid->columns[4][4]);
}

u64 run(std::string &s) {
    Input input = make_input_from_string(s);
    
    Iterator it = make_iterator(&input);
    Context context = {0};
    load_drawing(&it, &context);
    while (is_valid(&it)) {
        skip_to_next_grid(&it);
        load_and_process_grid(&it, &context);
        //print("Winning grid index: %d - Winning draw index: %d\n", context.index_winning_grid, context.drawing_win);
    }
    
    
    
    return compute_score(&it, &context);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Missing one argument" << std::endl;
        exit(1);
    }
    
    std::string input{argv[1]};
    
    auto start = std::chrono::steady_clock::now();
    auto answer = run(input);
    auto end = std::chrono::steady_clock::now();
    
    double duration = std::chrono::duration<double, std::milli>(end - start).count();
    
    std::cout << "_duration:" << duration << "\n";
    std::cout << answer << "\n";
    return 0;
}
