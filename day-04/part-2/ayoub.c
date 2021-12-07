#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define N 100
#define BOARD_SIZE 5

typedef struct Position {
    int board;
    int row;
    int column;
} Position;

typedef struct PositionList {
    Position positions[N];
    int length;
} PositionList;

void add_position(PositionList *l, int b, int r, int c) {
    if (l->length == N) {
        printf("ERROR adding to a full list: %d %d %d", b, r, c);
        exit(0);
    }
    l->positions[l->length].board = b;
    l->positions[l->length].row = r;
    l->positions[l->length].column = c;
    l->length++;
}

int run(char* s) {
    int boards[N][BOARD_SIZE][BOARD_SIZE] = {0};
    int draws[N] = {0};
    int marked[N] = {0};
    int won[N] = {0};
    PositionList pos[N];
    int i = 0, k = 0, b = -1, r = 0, c = 0, j, complete, count_wins = 0;

    while (s[i]) {
        if (k < N) {
            if (s[i] == ',' || s[i] == '\n') {
                pos[k].length = 0;
                k++;
            }
            else draws[k] = draws[k]*10+(int)(s[i]-'0');
            i++;
            continue;
        }
        if (b == -1) {
            while (s[i] == '\n' || s[i] == ' ') i++;
            b = 0;
            continue;
        }
        if (s[i] == ' ') {
            while (s[i] == ' ') i++;
            add_position(pos + boards[b][r][c], b, r, c); 
            c++;
            continue;
        }
        if (s[i] == '\n') {
            while (s[i] == '\n' || s[i] == ' ') i++;
            add_position(pos + boards[b][r][c], b, r, c);
            if (r < BOARD_SIZE-1) {
                r++; c = 0;
                continue;
            }
            b++; r = 0; c = 0;
            continue;
        }
        boards[b][r][c] = boards[b][r][c]*10+(int)(s[i]-'0');
        i++;
    }
    if (c != 0) {
        add_position(pos + boards[b][r][c], b, r, c);
    }

    for (i = 0; i < N; i++) {
        marked[draws[i]] = 1;
        for (k = 0; k < pos[draws[i]].length; k++) {
            b = pos[draws[i]].positions[k].board;
            r = pos[draws[i]].positions[k].row;
            c = pos[draws[i]].positions[k].column;
            if (won[b]) continue;

            complete = 1;
            for (j = 0; j < BOARD_SIZE; j++) {
                if (!marked[boards[b][r][(c+j)%BOARD_SIZE]]) {
                    complete = 0;
                    break;
                }
            }
            if (!complete) {
                complete = 1;
                for (j = 0; j < BOARD_SIZE; j++) {
                    if (!marked[boards[b][(r+j)%BOARD_SIZE][c]]) {
                        complete = 0;
                        break;
                    }
                }
            }
            if (complete) {
                won[b] = 1; count_wins++;
            }
            
            if (complete && count_wins == N) {
                complete = 0;
                for (r = 0; r < BOARD_SIZE; r++)
                for (c = 0; c < BOARD_SIZE; c++)
                complete += (!marked[boards[b][r][c]])?boards[b][r][c]:0;
                return complete*draws[i];
            }
        }
    }

    return 0;
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
