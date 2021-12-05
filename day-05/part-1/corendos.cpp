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
#define DIAGONAL 0
#define GRID_SIZE 1000

#if NO_LOG
#define print(format, ...)
#else
#define print(format, ...) printf((format) __VA_OPT__(,) __VA_ARGS__)
#endif

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

inline void skip_to_next_number(Iterator* it) {
    if (is_valid(it) && is_number(it->current[0])) return;
    while (is_valid(it)) {
        it->current++;
        if (is_number(it->current[0])) return;
    }
}

typedef u8 State;
enum {
    State_Empty,
    State_Once,
    State_Full,
};

struct Context {
    State overlaps[GRID_SIZE * GRID_SIZE];
    u32 overlap_count;
};

static Context global_context = {0};

void parse_and_process_coordinates(Iterator *it, Context *context) {
    i16 x1 = 0, y1 = 0;
    i16 x2 = 0, y2 = 0;
    
    // NOTE(Corentin): parse x1
    while (is_valid(it) && is_number(it->current[0])) {
        x1 = x1 * 10 + it->current[0] - '0';
        it->current++;
    }
    it->current++;
    
    // NOTE(Corentin): parse y1
    while (is_valid(it) && is_number(it->current[0])) {
        y1 = y1 * 10 + it->current[0] - '0';
        it->current++;
    }
    
    it->current += 4;
    
    // NOTE(Corentin): parse x2
    while (is_valid(it) && is_number(it->current[0])) {
        x2 = x2 * 10 + it->current[0] - '0';
        it->current++;
    }
    it->current++;
    
    // NOTE(Corentin): parse y2
    while (is_valid(it) && is_number(it->current[0])) {
        y2 = y2 * 10 + it->current[0] - '0';
        it->current++;
    }
    
    //print("x1: %3d - y1: %3d  -  x2: %3d - y2: %3d\n", x1, y1, x2, y2);
    
    i16 delta_x = (x1 == x2) ? 0 : (x1 < x2 ? 1 : -1);
    i16 delta_y = (y1 == y2) ? 0 : (y1 < y2 ? 1 : -1);
    u16 count = std::max(std::abs(x1 - x2), std::abs(y1 - y2));
#if !DIAGONAL
    if (delta_x != 0 && delta_y != 0) return;
#endif
    
    //print("delta_x: %3d - delta_x: %3d -  count: %3d\n\n", delta_x, delta_y, count);
    
    i16 x = x1, y = y1;
    for (u16 i = 0;i <= count;++i) {
        switch (context->overlaps[y * GRID_SIZE + x]) {
            case State_Empty:
            context->overlaps[y * GRID_SIZE + x] = State_Once;
            break;
            case State_Once:
            context->overlaps[y * GRID_SIZE + x] = State_Full;
            context->overlap_count++;
            break;
            default:
            break;
        }
        
        x += delta_x;
        y += delta_y;
    }
}

void print_grid(Context *context) {
    for (u16 y = 0;y < GRID_SIZE;++y) {
        for (u16 x = 0;x < GRID_SIZE;++x) {
            print("%3d ", context->overlaps[y * GRID_SIZE + x]);
        }
        print("\n");
    }
}

u64 run(std::string &s) {
    Input input = make_input_from_string(s);
    
    Iterator it = make_iterator(&input);
    
    while (is_valid(&it)) {
        parse_and_process_coordinates(&it, &global_context);
        skip_to_first_after(&it, '\n');
    }
    
    print_grid(&global_context);
    print("Overlap count: %d\n", global_context.overlap_count);
    
    return global_context.overlap_count;
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
