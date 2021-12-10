#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

struct stack {
    unsigned short array[128];
    unsigned short length;
};

void push(struct stack* s, unsigned short value) {
    s->length++; s->array[s->length-1] = value; 
}

unsigned short pop(struct stack* s) {
    s->length--; 
    return s->array[s->length]; 
}

const short NUM_LINES = 100;
const short LINE_LENGTH = 100+1;

bool is_low_point(char* s, unsigned short* p_cursor, unsigned short* p_col) {
    return (*p_cursor < LINE_LENGTH || s[*p_cursor] < s[*p_cursor - LINE_LENGTH]) &&
        (*p_cursor >  LINE_LENGTH * (NUM_LINES - 1) || s[*p_cursor] < s[*p_cursor + LINE_LENGTH]) &&
        (*p_col == 1 || s[*p_cursor] < s[*p_cursor - 1]) &&
        (*p_col == LINE_LENGTH - 1 || s[*p_cursor] < s[*p_cursor + 1]);
}

unsigned long bassin_size(char* s, char* visited, struct stack* to_visit, unsigned short cursor) {
    unsigned long size = 0;
    unsigned short current;
    push(to_visit, cursor);
    while (to_visit->length) {
        current = pop(to_visit);
        if (!visited[current] &&  s[current] != '\n' && s[current] != '9') {
            size++;
            if (current >= LINE_LENGTH && !visited[current - LINE_LENGTH]) {
                push(to_visit, current - LINE_LENGTH);
            }
            if (current < LINE_LENGTH * (NUM_LINES - 1) && !visited[current + LINE_LENGTH]) {
                push(to_visit, current + LINE_LENGTH);
            }
            if (current < LINE_LENGTH * NUM_LINES - 2 && !visited[current + 1]) {
                push(to_visit, current + 1);
            }
            if (current > 0 && !visited[current - 1]) {
                push(to_visit, current - 1);
            }
        }
        visited[current] = 1;
    }
    return size;
}

unsigned long run(char* s) {
    // Your code goes here
    unsigned long top1, top2, top3, current;
    top1 = top2 = top3 = current = 0;
    char visited[100*101] = {0};
    struct stack to_visit;
    to_visit.length = 0;
    unsigned short cursor = 0;
    unsigned short col = 1;
    while (cursor < NUM_LINES * LINE_LENGTH - 1) {
        if (s[cursor] == '\n') {
            col = 0;
        } else if (is_low_point(s, &cursor, &col)) {
            current = bassin_size(s, visited, &to_visit, cursor);
            if (current > top1) {top3 = top2; top2 = top1; top1 = current;}
            else if (current > top2) {top3 = top2; top2 = current;}
            else if (current > top3) {top3 = current;}
        }
        cursor++;
        col++;

    }
    return top1 * top2 * top3;
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
