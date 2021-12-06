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

struct Context {
    u64 fish_count;
    u64 bins[9];
};

static Context global_context = {0};

void print_bins(Context *context) {
    for (u8 i = 0;i < 9;i++) {
        print("[%d]: %3d\n", i, context->bins[i]);
    }
    print("\nfish count: %3d\n", context->fish_count);
}

inline void do_generation(Context *context) {
    u64 recycling = context->bins[0];
    context->bins[0] = context->bins[1];
    context->bins[1] = context->bins[2];
    context->bins[2] = context->bins[3];
    context->bins[3] = context->bins[4];
    context->bins[4] = context->bins[5];
    context->bins[5] = context->bins[6];
    context->bins[6] = context->bins[7] + recycling;
    context->bins[7] = context->bins[8];
    context->bins[8] = recycling;
    context->fish_count += recycling;
}

u64 run(std::string &s) {
    Input input = make_input_from_string(s);
    
    Iterator it = make_iterator(&input);
    
    while (is_valid(&it)) {
        global_context.bins[it.current[0] - '0']++;
        global_context.fish_count++;
        it.current += 2;
    }
    
    print_bins(&global_context);
    for (u16 i = 0;i < 256;++i) {
        do_generation(&global_context);
    }
    print_bins(&global_context);
    return global_context.fish_count;
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
