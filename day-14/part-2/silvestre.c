#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <limits.h>
/*
Intuition : there are 26 different letters, so we need 5 bits to represent one.
            So we can represent a pair of letters with a short (16-bits) using only the first 10 bits.
*/ 

#define MAPPING_SIZE 1024
#define RESET_MASK 1023                  // 11111 11111
#define SECOND_LETTER_MASK 31            // 00000 11111
#define FIRST_LETTER_MASK  (1023 - 31)   // 11111 00000
#define N_LETTERS 26
#define N_STEPS 40

typedef unsigned short ushort;
typedef unsigned long long ullong;

#define reset_array(array_ptr, len) for(ushort idx = 0; idx < len; idx++) {(*array_ptr)[idx] = 0;}

void init_counter(ullong counter[N_LETTERS+1], char* s) {
    reset_array(&counter, N_LETTERS+1);
    counter[(*s - 'A') + 1]++;
    while (*(s+1) != '\n') {s++;}
    counter[(*s - 'A') + 1]++;
}

void swap_ptr(void **ptr1, void **ptr2) {
    void *tmp = *ptr1; *ptr1 = *ptr2; *ptr2 = tmp;
}

void apply_step(ullong (*current)[MAPPING_SIZE], ullong (*next)[MAPPING_SIZE], ushort mapping[MAPPING_SIZE]) {
    for (ushort pair = 0; pair < MAPPING_SIZE; pair++) {
        (*next)[((pair & FIRST_LETTER_MASK) | mapping[pair])] += (*current)[pair];
        (*next)[((pair & SECOND_LETTER_MASK) | (mapping[pair] << 5))] += (*current)[pair];
    }
}

void parse_input(char *s, ushort mapping[MAPPING_SIZE], ullong (*current)[MAPPING_SIZE]) {
    ushort state = 0;
    ushort pair = 0;
    while (*s) {
        if (state == 0) {
            switch (*s) {
                case '\n':
                    state = 1;
                    pair = 0;
                    s++;
                    break;
                default:
                    pair = ((pair << 5) & RESET_MASK) | (*s - 'A' + 1);
                    if (pair > SECOND_LETTER_MASK) {
                        (*current)[pair]++;
                        //printf("here *s=%c, pair=%c%c (%u), (*current)[pair]=%d\n", *s, (char)((pair >> 5) + 'A' - 1), (char)((pair & 31) + 'A' - 1), pair, (*current)[pair]);
                    }
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

ullong run(char* s) {
    // variables
    ushort mapping[MAPPING_SIZE];
    ullong array1[MAPPING_SIZE], array2[MAPPING_SIZE];
    ullong (*current)[MAPPING_SIZE] = &array1;
    ullong (*next)[MAPPING_SIZE] = &array2;
    ullong counter[N_LETTERS+1];
    // 
    reset_array(&mapping, MAPPING_SIZE);
    reset_array(current, MAPPING_SIZE);
    reset_array(next, MAPPING_SIZE);
    parse_input(s, mapping, current);
    init_counter(counter, s);
    for (ushort step = 0; step < N_STEPS; step++) {
        apply_step(current, next, mapping);
        swap_ptr((void**) &current, (void**) &next);
        reset_array(next, MAPPING_SIZE);
    }
    for (ushort pair = 0; pair < MAPPING_SIZE; pair++) {
        counter[(pair & SECOND_LETTER_MASK)] += (*current)[pair];
        counter[(pair >> 5)] += (*current)[pair];
    }
    for (ushort counter_idx = 0; counter_idx < N_LETTERS + 1; counter_idx++) {
        counter[counter_idx] /= 2;
    }
    ullong min = ULLONG_MAX;
    ullong max = 0;
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
    ullong answer = run(argv[1]);
    
    printf("_duration:%f\n%llu\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
