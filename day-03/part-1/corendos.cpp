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
    u16 counter[12];
    u16 line_count;
};

inline void process_line(Iterator *it, Context *context) {
    context->counter[11] += (it->current[0 ] - 48);
    context->counter[10] += (it->current[1 ] - 48);
    context->counter[ 9] += (it->current[2 ] - 48);
    context->counter[ 8] += (it->current[3 ] - 48);
    context->counter[ 7] += (it->current[4 ] - 48);
    context->counter[ 6] += (it->current[5 ] - 48);
    context->counter[ 5] += (it->current[6 ] - 48);
    context->counter[ 4] += (it->current[7 ] - 48);
    context->counter[ 3] += (it->current[8 ] - 48);
    context->counter[ 2] += (it->current[9 ] - 48);
    context->counter[ 1] += (it->current[10] - 48);
    context->counter[ 0] += (it->current[11] - 48);
    context->line_count++;
    it->current += 12;
}

u64 run(std::string &s) {
    Input input = make_input_from_string(s);
    
    Iterator it = make_iterator(&input);
    Context context = {0};
    
    while (is_valid(&it)) {
        process_line(&it, &context);
        skip_to_first_after(&it, '\n');
    }
    
    u64 gamma_rate = 0;
    for (u32 i = 0;i < 12;i++) {
        gamma_rate += ((context.counter[i] > (context.line_count >> 1) ? 1 : 0) << i);
    }
    
    u64 epsilon_rate = ~gamma_rate & 0b111111111111;
    
    return gamma_rate * epsilon_rate;
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
