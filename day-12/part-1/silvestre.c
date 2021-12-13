#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

#define END 1
#define START 0
#define N_NODES 16 // short
#define MAX_NODE_NAME_LENGHT 6
#define MAX_SIMULTANEOUS_PATHS 30

bool str_eq(char* curr, char* end, char* other) {
    while (curr < end && *other) {
        if (*curr != *other) {
            return false;
        }
        curr++; other++;
    }
    return curr == end && *other == '\0';
}

void next_node(char** p_s, char** p_start, char** p_end) {
    *p_start = *p_s;
    while (**p_s != '-' && **p_s != '\n' && **p_s) {(*p_s)++;}
    *p_end = *p_s;
}

struct graph {
    bool adjency_matrix[N_NODES][N_NODES];
    bool small_caves[N_NODES];
    char ids[N_NODES][MAX_NODE_NAME_LENGHT];
    unsigned short n_caves;
};

void init_graph(struct graph* graph) {
    for (unsigned short i=0; i < N_NODES; i++) {
        for (unsigned short j=0; j < N_NODES; j++) {
            graph->adjency_matrix[i][j] = 0;
        }
        graph->small_caves[i] = (i == START) || (i == END);
        for (unsigned short j=0; j < MAX_NODE_NAME_LENGHT; j++) {
            graph->ids[i][j] = '\0';
        }
    }
    char* lit_start = "start";
    char* lit_end = "end";
    for (unsigned short j=0; j<6; j++) {graph->ids[START][j] = lit_start[j];}
    for (unsigned short j=0; j<4; j++) {graph->ids[END][j] = lit_end[j];}
    graph->n_caves = 2;
}

short get_id(struct graph* graph, char* start, char* end) {
    for (unsigned short idx = 0; idx < graph->n_caves; idx++) {
        if (str_eq(start, end, graph->ids[idx])) {
            return idx;
        }
    }
    for (unsigned short idx = 0; idx < (end - start); idx++) {
        graph->ids[graph->n_caves][idx] = *(start+idx);
    }
    (graph->n_caves)++;
    return graph->n_caves - 1;
}

void parse_graph(char* s, struct graph* graph) {
    char* left_start; 
    char* left_end;
    char* right_start;
    char* right_end;
    short id_left, id_right;
    while (*s) {
        next_node(&s, &left_start, &left_end);
        s++;
        next_node(&s, &right_start, &right_end);
        id_left = get_id(graph, left_start, left_end);
        id_right = get_id(graph, right_start, right_end);
        graph->adjency_matrix[id_left][id_right] = true;
        graph->adjency_matrix[id_right][id_left] = true;
        graph->small_caves[id_left] = (*left_start > 'Z');
        graph->small_caves[id_right] = (*right_start > 'Z');
        if (*s) s++;
    }
}

struct path {
    unsigned short current;
    bool visited[N_NODES];
};

unsigned long run(char* s) {
    struct graph graph;
    init_graph(&graph);
    parse_graph(s, &graph);

    unsigned long counter = 0;
    struct path paths[MAX_SIMULTANEOUS_PATHS];
    unsigned short len, path_idx;
    len = 0;
    paths[len].current = START;
    for (unsigned short idx = 0; idx < graph.n_caves; idx++) {
        paths[len].visited[idx] = (idx == START);
    }
    len++;
    while (len) {
        // pop
        path_idx = len-1;
        for (unsigned short next=0; next < graph.n_caves; next++) {
            if (graph.adjency_matrix[paths[path_idx].current][next]) {
                if (paths[path_idx].visited[next]) {continue;}
                if (next == END) {
                    counter++;
                    continue;
                }
                // push
                paths[len].current = next;
                for (unsigned short idx = 0; idx < graph.n_caves; idx++) {
                    paths[len].visited[idx] = paths[path_idx].visited[idx];
                }
                paths[len].visited[next] = graph.small_caves[next];
                len++;
            }
        }
        len--;
        if (path_idx < len) {
            paths[path_idx].current = paths[len].current;
            for (unsigned short idx = 0; idx < graph.n_caves; idx++) {
                paths[path_idx].visited[idx] = paths[len].visited[idx];
            }
        }   
    }
    return counter;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    unsigned long answer = run(argv[1]);
    
    printf("_duration:%f\n%lu\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
