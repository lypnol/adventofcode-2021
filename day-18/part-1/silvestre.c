#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

/*
Intuition 
We represent the fish's numbers with a tree implemented with an array (like a heap). 
As the tree is not complete, we use a field 'status' to mark if a node is a LEAF, EMPTY or DEFAULT (a node which is not a leaf).
The heap representation let us know several things.
- if the index is 2, 6, 14, 30 (or 62), the current node has no right neighbors.
- if the index is 1, 3, 7, 15 (or 31), the current node has no left neighbors.
*/

enum STATUS {EMPTY, LEAF, DEFAULT};

typedef struct {
    enum STATUS status;
    char value;
} Node;
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
            next[idx].status = DEFAULT;
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
            next[idx].status = LEAF;
            next[idx].value = (**s - '0');
            break;
        }
        (*s)++;
    }
}

bool explode(Node current[64]) {
    size_t idx2;
    for (size_t idx=15; idx<31; idx++) /* iterate through 4th depth */ {
        if (current[idx].status == DEFAULT) {
            // explode
            current[left_child(idx)].status = EMPTY;
            current[right_child(idx)].status = EMPTY;
            
            if (idx != 15) /* has_left_leaf */ {
                idx2 = left_child(idx)-1;
                while (current[idx2].status != LEAF) {
                    idx2 = parent(idx2);
                }
                current[idx2].value += current[left_child(idx)].value;
            }
            if (idx != 30) /* has_right_leaf */ {
                idx2 = right_child(idx) + 1;
                while (current[idx2].status != LEAF) {
                    idx2 = parent(idx2);
                }
                current[idx2].value += current[right_child(idx)].value;
            }
            current[idx].value = 0;
            current[idx].status = LEAF;
            return true;
        }
    }
    return false;
}

bool split(Node current[64]) {
    char half;
    size_t idx = 15;
    while (true) {
        switch (current[idx].status) {
        case LEAF:
            if (current[idx].value > 9) {
                // split
                current[idx].status = DEFAULT;
                half = current[idx].value >> 1;
                current[left_child(idx)].status = LEAF;
                current[left_child(idx)].value = half;
                current[right_child(idx)].status = LEAF;
                current[right_child(idx)].value = half;
                if (half << 1 != current[idx].value) {current[right_child(idx)].value++;}
                return true;
            } else if (idx == 30 || idx == 14 || idx == 6 || idx == 2) {
                return false;
            } else {idx++;}
            break;
        case EMPTY:
            idx = parent(idx);
            break;
        default:
            idx = left_child(idx);
            break;
        }
    }
    //return false;
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

    current[0].status = DEFAULT;
    reduce(current);
}

int magnitude(Node current[64], size_t idx) {
    if (current[idx].status == LEAF) return current[idx].value;
    return 3 * magnitude(current, left_child(idx)) + 2 * magnitude(current, right_child(idx));
}

int run(char* s) {
    Node current[64] = {0};
    Node next[64] = {0};
    parse_line(&s, current);
    while (*s) {
        parse_line(&s, next);
        add(current, next);
        memset(next, 0, 64 * sizeof(Node));
    }
    return magnitude(current, 0);
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
