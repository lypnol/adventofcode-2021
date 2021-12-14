#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <limits.h>
/*
Intuition : there are 26 different letters, so we need 5 bits to represent one.
            So we can represent a pair of letters with a short (16-bits) using only the first 10 bits.

            N.B. : We'll use the bitmask 1023 (which has ones for its 10 first bits) to reset the other bits of the short.
*/ 

#define MAPPING_SIZE 1024
#define MAX_POLYMER_SIZE 1024 * 16
#define RESET_MASK 1023
#define N_LETTERS 26
#define N_STEPS 10

typedef unsigned short ushort;

void init_mapping(char mapping[MAPPING_SIZE]) {
    for (ushort idx = 0; idx < MAPPING_SIZE; idx++) {mapping[idx] = 0;}
}

void init_counter(ushort counter[N_LETTERS+1]) {
    for (ushort idx = 0; idx < N_LETTERS+1; idx++) {counter[idx] = 0;}
}

void swap_ptr(void **ptr1, void **ptr2) {
    void *tmp = *ptr1; *ptr1 = *ptr2; *ptr2 = tmp;
}

void apply_step(char (*current)[MAX_POLYMER_SIZE], ushort *current_size, char (*next)[MAX_POLYMER_SIZE], char mapping[MAPPING_SIZE]) {
    ushort pair = 0;
    ushort next_idx = 0;
    for (ushort current_idx = 0; current_idx < *current_size; current_idx++) {
        pair = ((pair << 5) & RESET_MASK) | (*current)[current_idx];
        (*next)[next_idx] = mapping[pair];
        next_idx += (mapping[pair] != 0);
        (*next)[next_idx] = (*current)[current_idx]; 
        next_idx++;
    }
    *current_size = next_idx;
}

void parse_input(char *s, char mapping[MAPPING_SIZE], char (*current)[MAX_POLYMER_SIZE], ushort *current_size) {
    ushort state = 0;
    ushort pair = 0;
    *current_size = 0;
    while (*s) {
        if (state == 0) {
            switch (*s) {
                case '\n':
                    state = 1;
                    s++;
                    break;
                default:
                    (*current)[*current_size] = (*s - 'A' + 1);
                    (*current_size)++;
            }
            s++;
        } else {
            switch (*s) {
                case '\n':
                    pair = 0;
                    state = 1;
                    s++;
                    break;
                case ' ':
                    state = 2;
                    s += 4;
                    break;
                default:
                    switch (state) {
                        case 1:
                            pair = ((pair << 5) & RESET_MASK) | (*s - 'A' + 1);
                            break;
                        case 2:
                            mapping[pair] = (*s - 'A' + 1);
                            break;
                    }
                    s++;
                    break;
            }
        }
    }
}

int run(char* s) {
    // variables
    char mapping[MAPPING_SIZE];
    char array1[MAX_POLYMER_SIZE], array2[MAX_POLYMER_SIZE];
    char (*current)[MAX_POLYMER_SIZE] = &array1;
    char (*next)[MAX_POLYMER_SIZE] = &array2;
    ushort current_size = 0;
    ushort counter[N_LETTERS+1];
    // 
    init_mapping(mapping);
    parse_input(s, mapping, current, &current_size);
    for (ushort step = 0; step < N_STEPS; step++) {
        apply_step(current, &current_size, next, mapping);
        swap_ptr((void**) &current, (void**) &next);
    }
    init_counter(counter);
    for (ushort current_idx = 0; current_idx < current_size; current_idx++) {
        counter[(ushort)(*current)[current_idx]]++;
    }
    ushort min = USHRT_MAX;
    ushort max = 0;
    for (ushort counter_idx = 0; counter_idx < N_LETTERS + 1; counter_idx++) {
        min = counter[counter_idx] < min && counter[counter_idx] ? counter[counter_idx] : min;
        max = counter[counter_idx] > max ? counter[counter_idx] : max;
    }
    return max - min;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
