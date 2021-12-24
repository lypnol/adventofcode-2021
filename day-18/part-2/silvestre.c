#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

// Intuition : the number is a tree, we will represent it with one array of struct.
//             each struct has two members : 
//             - the status of the node (empty, leaf, default)
//             - the value.

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
        //printf("idx=%lu, depth=%u, path[depth]=%u, **s=%c\n", idx, depth, path[depth], **s);
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
            //printf("explode at %lu -> ", idx);
            //print(current, "current");
            return true;
        }
    }
    return false;
}

bool split(Node current[64]) {
    char half;
    size_t idx = 15;
    //for (size_t idx=0; idx<63; idx++) {
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
                //printf("split at %lu -> ", idx);
                //print(current, "current");
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

void rec_print(Node arr[64], size_t idx) {
    if (arr[idx].status == LEAF) {
        printf("%d", arr[idx].value);
    } else {
        printf("[");
        rec_print(arr, left_child(idx));
        printf(",");
        rec_print(arr, right_child(idx));
        printf("]");
    }
}

void print(Node arr[64], char *name) {
    printf("%s=", name);
    rec_print(arr, 0);
    printf("\n");
}

int run(char* s) {
    Node numbers[100][64] = {0};
    Node current[64] = {0};
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
