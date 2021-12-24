#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

/* for Intuition see part-1 */ 
typedef unsigned char Node;
#define DEFAULT 255
#define EMPTY 254
#define is_leaf(value) (value < 254)
#define left_child(idx) (2 * idx + 1)
#define right_child(idx) (2 * idx + 2)
#define parent(idx) (idx-1)/2

void parse_line(char **s, Node next[64]) {
    size_t idx = 0;
    bool path[5] = {0}; // 5 bits used, 0 for left, 1 for right. first one is always zero.
    size_t depth = 0;
    while (**s) {
        switch (**s) {
        case '\n':
            (*s)++;
            return;
            break;
        case '[':
            next[idx] = DEFAULT;
            depth++;
            idx = left_child(idx) + path[depth];
            break;
        case ']':
            path[depth] = 0;
            depth--;
            idx = parent(idx);
            break;
        case ',':
            path[depth] = 1;
            idx++;
            break;
        default:
            next[idx] = (Node)(**s - '0');
            break;
        }
        (*s)++;
    }
}

bool explode(Node current[64]) {
    size_t idx2;
    for (size_t idx=15; idx<31; idx++) /* iterate through 4th depth */ {
        if (current[idx] == DEFAULT) {
            // explode
            if (idx != 15) /* has_left_leaf */ {
                idx2 = left_child(idx)-1;
                while (!is_leaf(current[idx2])) {
                    idx2 = parent(idx2);
                }
                current[idx2] += current[left_child(idx)];
            }
            if (idx != 30) /* has_right_leaf */ {
                idx2 = right_child(idx) + 1;
                while (!is_leaf(current[idx2])) {
                    idx2 = parent(idx2);
                }
                current[idx2] += current[right_child(idx)];
            }
            current[idx] = 0;
            current[left_child(idx)] = EMPTY;
            current[right_child(idx)] = EMPTY;
            return true;
        }
    }
    return false;
}

bool split(Node current[64]) {
    char half;
    size_t idx = 15;
    while (true) {
        if (is_leaf(current[idx])) {
            if (current[idx] > 9) {
                // split
                half = current[idx] >> 1;
                current[left_child(idx)] = half;
                current[right_child(idx)] = half;
                if (half << 1 != current[idx]) {current[right_child(idx)]++;}
                current[idx] = DEFAULT;
                return true;
            } else if (idx == 30 || idx == 14 || idx == 6 || idx == 2) {
                return false;
            } else {idx++;}
        } else if (current[idx] == DEFAULT) {
            idx = left_child(idx);
        } else {
            idx = parent(idx);
        }
    }
}


void reduce(Node current[64]) {
    while (true) {
        if (explode(current)) {continue;}
        if (split(current)) {continue;}
        break;
    }
}

void add(Node current[64], Node next[64]) {
    // depth = 4
    for (size_t idx=30; idx>=15; idx--) {
        current[idx+16] = current[idx];
        current[idx+32] = next[idx];        
    }
    // depth = 3
    for (size_t idx=14; idx>=7; idx--) {
        current[idx+8] = current[idx];
        current[idx+16] = next[idx];
    }
    // depth = 2
    for (size_t idx=6; idx>=3; idx--) {
        current[idx+4] = current[idx];
        current[idx+8] = next[idx];
    }
    // depth = 1
    for (size_t idx=2; idx>=1; idx--) {
        current[idx+2] = current[idx];
        current[idx+4] = next[idx];
    }
    // depth = 0
    current[1] = current[0];
    current[2] = next[0];

    current[0] = DEFAULT;
    reduce(current);
}

int magnitude(Node current[64], size_t idx) {
    if (is_leaf(current[idx])) return current[idx];
    return 3 * magnitude(current, left_child(idx)) + 2 * magnitude(current, right_child(idx));
}

int run(char* s) {
    Node numbers[100][64];
    memset(numbers, EMPTY, 100 * 64 * sizeof(Node));
    Node current[64];
    memset(current, EMPTY, 64 * sizeof(Node));
    size_t len = 0;
    while (*s) {
        parse_line(&s, numbers[len]);
        len++;
    }
    int max_magnitude = 0;
    int current_magnitude = 0;
    for (size_t i = 0; i < len-1; i++) {
        for (size_t j = i + 1; j < len; j++) {
            memcpy(current, numbers[i], sizeof(Node) * 64);
            add(current, numbers[j]);
            current_magnitude = magnitude(current, 0);
            if (current_magnitude > max_magnitude) {
                max_magnitude = current_magnitude;
            }  
        }
    }
    for (size_t i = 0; i < len-1; i++) {
        for (size_t j = i + 1; j < len; j++) {
            memcpy(current, numbers[j], sizeof(Node) * 64);
            add(current, numbers[i]);
            current_magnitude = magnitude(current, 0);
            if (current_magnitude > max_magnitude) {
                max_magnitude = current_magnitude;
            }
        }
    }
    return max_magnitude;
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
