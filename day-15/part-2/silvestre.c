#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <limits.h>
#include <stdbool.h>

typedef unsigned short ushort;
typedef unsigned long ulong;
typedef unsigned long risk;
#define RISKMAX ULONG_MAX

#define INPUT_N_LINES 100
#define INPUT_N_COLS 100
#define N_LINES 500
#define N_COLS 500

#define set_matrix(array, n_rows, n_cols, value)                 \
  for (ushort i=0; i<n_rows; i++) {                              \
      for (ushort j=0; j<n_cols; j++) {                          \
          array[i][j] = value;                                   \
      }                                                          \
  }                                                              \

#define min(a, b)  ((a) < (b) ? (a) : (b))
#define swap(a, b, tmp) do {tmp = a; a = b; b = tmp;} while (0)

typedef struct {
    ushort row;
    ushort col;
    risk risk;
} Node;

typedef struct {
    Node array[100000];
    ulong len;
} MinHeap;
#define left_child(idx) (2 * idx + 1)
#define right_child(idx) (2 * idx + 2)
#define parent(idx) (idx-1)/2

void init(MinHeap *heap) {heap->len = 0;}

void add(MinHeap *heap, Node node) {
    ulong idx = heap->len;
    Node tmp;
    heap->array[idx] = node;
    heap->len++;
    while (idx && heap->array[idx].risk < heap->array[parent(idx)].risk) {
        swap(heap->array[idx], heap->array[parent(idx)], tmp);
        idx = parent(idx);
    }
}

Node extract_min(MinHeap *heap) {
    Node tmp;
    swap(heap->array[0], heap->array[heap->len - 1], tmp);
    heap->len--;
    // heapify
    risk crisk;
    risk lrisk; 
    risk rrisk;
    ulong idx = 0;
    while (left_child(idx) < heap->len) {
        crisk = heap->array[idx].risk;
        lrisk = heap->array[left_child(idx)].risk;
        if (right_child(idx) >= heap->len) { // no right child
            if (crisk > lrisk) {
                swap(heap->array[idx], heap->array[left_child(idx)], tmp);
                idx = left_child(idx);
            } else {break;}
        } else {
            rrisk = heap->array[right_child(idx)].risk;
            if (crisk > lrisk) {
                if (lrisk > rrisk) {
                    swap(heap->array[idx], heap->array[right_child(idx)], tmp);
                    idx = right_child(idx);
                } else {
                    swap(heap->array[idx], heap->array[left_child(idx)], tmp);
                    idx = left_child(idx);
                }
            } else {
                if (crisk > rrisk) {
                    swap(heap->array[idx], heap->array[right_child(idx)], tmp);
                    idx = right_child(idx);
                } else {break;}
            }
        }
    }
    return heap->array[heap->len];
}

void parse_input(char *s, risk map[N_LINES][N_COLS]) {
    ushort i = 0;
    ushort j = 0;
    risk r = 0;
    while (*s) {
        switch (*s) {
            case '\n':
                i++;
                j = 0;
                break;
            default:
                r = (risk)(*s - '0');
                for (ushort row=0; row<5; row++) {
                    for (ushort col=0; col<5; col++) {
                        map[(row*INPUT_N_LINES)+i][(col*INPUT_N_COLS)+j] = r + row + col < 10 ? r + row + col : (r + row + col) % 10 + 1;
                    }
                }
                j++;
                break;
        }
        s++;
    }
}

risk dijkstra(risk map[N_LINES][N_COLS]) {
    // variables
    Node current = {0, 0, 0};
    Node tmp;
    risk distmap[N_LINES][N_COLS];
    set_matrix(distmap, N_LINES, N_COLS, RISKMAX);
    distmap[current.row][current.col] = 0;
    risk new_risk;
    bool visited[N_LINES][N_COLS] = {false}; // all false;
    MinHeap heap;
    init(&heap);
    add(&heap, current);
    while (heap.len /* !visited[N_LINES-1][N_COLS-1]*/) {
        current = extract_min(&heap);

        if (current.risk != distmap[current.row][current.col]) {continue;}
        if (visited[current.row][current.col]) {continue;}

        visited[current.row][current.col] = true;

        if (current.row && !visited[current.row-1][current.col]) {
            // visit up
            new_risk = distmap[current.row][current.col] + map[current.row-1][current.col];
            if (new_risk < distmap[current.row-1][current.col]) {
                distmap[current.row-1][current.col] = new_risk;
                tmp.row = current.row-1; tmp.col = current.col; tmp.risk = new_risk;
                add(&heap, tmp);
            }
        }
        if (current.col && !visited[current.row][current.col-1]) {
            // visit left
            new_risk = distmap[current.row][current.col] + map[current.row][current.col-1];
            if (new_risk < distmap[current.row][current.col-1]) {
                distmap[current.row][current.col-1] = new_risk;
                tmp.row = current.row; tmp.col = current.col-1; tmp.risk = new_risk;
                add(&heap, tmp);
            }
        }
        if (current.row < (N_LINES-1) && !visited[current.row+1][current.col]) {
            // visit down
            new_risk = distmap[current.row][current.col] + map[current.row+1][current.col];
            if (new_risk < distmap[current.row+1][current.col]) {
                distmap[current.row+1][current.col] = new_risk;
                tmp.row = current.row+1; tmp.col = current.col; tmp.risk = new_risk;
                add(&heap, tmp);
            }
        }
        if (current.col < (N_COLS-1) && !visited[current.row][current.col+1]) {
            // visit right
            new_risk = distmap[current.row][current.col] + map[current.row][current.col+1];
            if (new_risk < distmap[current.row][current.col+1]) {
                distmap[current.row][current.col+1] = new_risk;
                tmp.row = current.row; tmp.col = current.col+1; tmp.risk = new_risk;
                add(&heap, tmp);
            }
        }
    }
    return distmap[N_LINES-1][N_COLS-1];
}

risk run(char* s) {
    risk map[N_LINES][N_COLS];
    parse_input(s, map);
    return dijkstra(map);
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    risk answer = run(argv[1]);
    
    printf("_duration:%f\n%lu\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
