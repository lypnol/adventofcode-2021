#include <iostream>
#include <string>
#include <ctime>
#include <cstdio>
#include <cstdint>
#include <cstdlib>
#include <cassert>


typedef uint64_t u64;
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;

typedef int64_t i64;
typedef int32_t i32;
typedef int16_t i16;
typedef int8_t i8;

typedef size_t usize;

void print_binary(u64 value, usize width) {
    for (usize i = width;i > 0;--i) {
        u64 temp = (1ull << (i - 1));
        printf("%c", (value & temp) > 0 ? '1' : '0');
    }
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
    u16 line_count;
    u32 vitals[4096];
};

void load_line(Iterator *it, Context *context) {
    u32 *line = context->vitals + context->line_count;
    for (u32 i = 0;i < 12;++i) {
        *line |= ((it->current[i] - 48) << (11 - i));
    }
    context->line_count++;
}

void load_vitals(Iterator *it, Context *context) {
    while (is_valid(it)) {
        load_line(it, context);
        skip_to_first_after(it, '\n');
    }
}

u32 partition(Context *context, u32 mask, u32 beg, u32 end) {
    while (beg < end) {
        if (!(context->vitals[beg] & mask)) {
            beg++;
        } else if ((context->vitals[end - 1] & mask)) {
            end--;
        } else {
            u32 temp = context->vitals[beg];
            context->vitals[beg] = context->vitals[end - 1];
            context->vitals[end - 1] = temp;
        }
    }
    
    return beg;
}

u32 partition_oxygen(Context *context, u32 mask, u32 beg, u32 end) {
    if (beg == end - 1) {
        return beg; 
    }
    
    u32 beg_backup = beg;
    u32 end_backup = end;
    while (beg < end - 1) {
        if (!(context->vitals[beg] & mask)) {
            beg++;
        } else if ((context->vitals[end - 1] & mask)) {
            end--;
        } else {
            u32 temp = context->vitals[beg];
            context->vitals[beg] = context->vitals[end - 1];
            context->vitals[end - 1] = temp;
        }
    }
    
    if ((beg - beg_backup) > ((end_backup - beg_backup) >> 1)) {
        return partition_oxygen(context, mask >> 1, beg_backup, beg);
    }
    
    return partition_oxygen(context, mask >> 1, beg, end_backup);
}

u32 partition_co2(Context *context, u32 mask, u32 beg, u32 end) {
    if (beg == end - 1) {
        return beg;
    }
    
    u32 beg_backup = beg;
    u32 end_backup = end;
    while (beg < end - 1) {
        if (!(context->vitals[beg] & mask)) {
            beg++;
        } else if ((context->vitals[end - 1] & mask)) {
            end--;
        } else {
            u32 temp = context->vitals[beg];
            context->vitals[beg] = context->vitals[end - 1];
            context->vitals[end - 1] = temp;
        }
    }
    
    assert(beg - beg_backup > 0);
    
    if ((beg - beg_backup) > ((end_backup - beg_backup) >> 1)) {
        return partition_co2(context, mask >> 1, beg, end_backup);
    }
    
    return partition_co2(context, mask >> 1, beg_backup, beg);
    
}

u64 run(std::string &s) {
    Input input = make_input_from_string(s);
    
    Iterator it = make_iterator(&input);
    Context context = {0};
    u32 mask = 1 << 11;
    
    load_vitals(&it, &context);
    u32 split = partition(&context, mask, 0, context.line_count);
    
    u32 oxygen_index = 0;
    u32 co2_index = 0;
    
    if (split > (context.line_count >> 1)) {
        oxygen_index = partition_oxygen(&context, mask >> 1, 0, split);
    } else {
        oxygen_index = partition_oxygen(&context, mask >> 1, split, context.line_count);
    }
    
    if (split <= (context.line_count >> 1)) {
        co2_index = partition_co2(&context, mask >> 1, 0, split);
    } else {
        co2_index = partition_co2(&context, mask >> 1, split, context.line_count);
    }
    
    return context.vitals[oxygen_index] * context.vitals[co2_index];
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
