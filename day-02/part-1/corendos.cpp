#include <iostream>
#include <string>
#include <ctime>
#include <cstdio>
#include <cstdint>
#include <cstdlib>


typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;

typedef int64_t i64;
typedef int32_t i32;
typedef int16_t i16;
typedef int8_t i8;

typedef size_t usize;

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

struct Context {
    u64 depth;
    u64 hpos;
};

inline void parse_line(Iterator *it, Context *context) {
    char instruction = it->current[0];
    skip_to(it, '\n');

    switch (instruction) {
        case 'f':
        context->hpos += it->current[-1] - 48;
        break;
        case 'd':
        context->depth += it->current[-1] - 48;
        break;
        case 'u':
        context->depth -= it->current[-1] - 48;
        break;
    }
}

u64 run(std::string &s) {
    Input input = make_input_from_string(s);
    
    Iterator it = make_iterator(&input);
    Context context = {0};
    
    while (is_valid(&it)) {
        parse_line(&it, &context);
        it.current++;
    }
    
    return context.depth * context.hpos;
}

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cout << "Missing one argument" << std::endl;
        exit(1);
    }
    
    std::string input{argv[1]};
    
    clock_t start = clock();
    auto answer = run(input);
    float duration = float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC;
    
    std::cout << "_duration:" << duration << "\n";
    std::cout << answer << "\n";
    return 0;
}
