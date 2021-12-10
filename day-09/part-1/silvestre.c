#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

const short NUM_LINES = 100;
const short LINE_LENGTH = 100+1;

bool is_low_point(char* s, unsigned short* p_cursor, unsigned short* p_col) {
    return (*p_cursor < LINE_LENGTH || s[*p_cursor] < s[*p_cursor - LINE_LENGTH]) &&
        (*p_cursor >  LINE_LENGTH * (NUM_LINES - 1) || s[*p_cursor] < s[*p_cursor + LINE_LENGTH]) &&
        (*p_col == 1 || s[*p_cursor] < s[*p_cursor - 1]) &&
        (*p_col == LINE_LENGTH - 1 || s[*p_cursor] < s[*p_cursor + 1]);
}

unsigned long run(char* s) {
    // Your code goes here
    unsigned long counter = 0;
    unsigned short cursor = 0;
    unsigned short col = 1;
    while (cursor < NUM_LINES * LINE_LENGTH - 1) {
        if (s[cursor] == '\n') {
            col = 0;
        } else if (is_low_point(s, &cursor, &col)) {
            counter += (unsigned long)(s[cursor] - '0' + 1);
        }
        cursor++;
        col++;

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
