#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

const unsigned short N_STEPS = 100;
const unsigned short N_LINES = 10;
const unsigned short N_COLS = 11;
const unsigned short N_CARAC = N_LINES * (N_COLS);

struct stack {
    unsigned short array[256];
    unsigned short length;
};

void push(struct stack* s, unsigned short value) {
    s->length++; s->array[s->length-1] = value; 
}

unsigned short pop(struct stack* s) {
    s->length--; 
    return s->array[s->length]; 
}

void reset(char* s, bool* flashed, unsigned long* p_counter) {
    for (unsigned short cursor=0; cursor < N_CARAC; cursor++) {
        if (flashed[cursor]) {
            (*p_counter)++;
            flashed[cursor] = false;
            s[cursor] = '0';
        }
    }
}

void update_add(unsigned short cursor, char* s, bool* flashed, struct stack* to_visit) {
    s[cursor]++; 
    if (s[cursor] > '9' && !flashed[cursor]) {
        flashed[cursor] = true;
        push(to_visit, cursor);
    }
}

void init_step(char* s, bool* flashed, struct stack* to_visit) {
    for (unsigned short cursor=0; cursor < N_CARAC; cursor++) {
        if (s[cursor] != '\n') {
            update_add(cursor, s, flashed, to_visit);
        }
    }
}

unsigned long run(char* s) {
    unsigned long counter = 0;
    bool flashed[110] = {false};
    struct stack to_visit;
    to_visit.length = 0;
    unsigned short cursor, col;
    bool first_line, last_line, first_col, last_col;
    for (unsigned short step = 0; step < N_STEPS; step++) {
        init_step(s, flashed, &to_visit);
        while (to_visit.length) {
            cursor = pop(&to_visit);
            col = cursor % N_COLS;
            first_line = cursor < N_COLS;
            first_col = !col;
            last_line = cursor >= (N_COLS * (N_LINES -1));
            last_col = col == (N_COLS-2);
            if (!first_line && !first_col) {update_add(cursor-N_COLS-1, s, flashed, &to_visit);}
            if (!first_line) {update_add(cursor-N_COLS, s, flashed, &to_visit);}
            if (!first_line && !last_col) {update_add(cursor-N_COLS+1, s, flashed, &to_visit);}
            if (!first_col) {update_add(cursor-1, s, flashed, &to_visit);}
            if (!last_col) {update_add(cursor+1, s, flashed, &to_visit);}
            if (!last_line && !first_col) {update_add(cursor+N_COLS-1, s, flashed, &to_visit);}
            if (!last_line) {update_add(cursor+N_COLS, s, flashed, &to_visit);}
            if (!last_line && !last_col) {update_add(cursor+N_COLS+1, s, flashed, &to_visit);}
        }
        reset(s, flashed, &counter);
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
