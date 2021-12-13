#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define MAX_COORDS 1024
#define MAX_FOLDS 16

typedef unsigned short ushort;

void parse_input(char* s, ushort coord[MAX_COORDS][2], ushort* n_coord, ushort folds[MAX_FOLDS][2], ushort* n_folds) {
    int state = 0;
    *n_coord = 0;
    *n_folds = 0;
    ushort curr = 0;
    while (*s) {
        if (state == 0) {
            switch (*s) {
                case '\n':
                    coord[*n_coord][0] = curr;
                    (*n_coord)++;
                    curr = 0;
                    if (*(s+1) == '\n') {
                        state = 1;
                        s+=12;
                    }
                    break;
                case ',':
                    coord[*n_coord][1] = curr;
                    curr = 0;
                    break;
                default:
                    curr = 10 * curr + (ushort)(*s - '0');
                    break;
            }
            s++;
        }
        if (state == 1) {
            switch (*s)
            {
            case '\n':
                folds[*n_folds][1] = curr;
                (*n_folds)++;
                s+=12;
                curr = 0;
                break;
            case 'x':
                folds[*n_folds][0] = 1;
                s+=2;
                break;
            case 'y':
                folds[*n_folds][0] = 0;
                s+=2; 
                break;
            default:
                curr = 10 * curr + (ushort)(*s - '0');
                s++;
                break;
            }
        }
    }
    folds[*n_folds][1] = curr;
    (*n_folds)++;
}

void apply_fold(ushort len, ushort coord[MAX_COORDS][2], ushort axis, ushort fold) {
    for (ushort row=0; row<len; row++) {
        coord[row][axis] = coord[row][axis] + 2 * (fold - coord[row][axis]) * (coord[row][axis] > fold);
    }
}

unsigned long count_uniq(ushort len, ushort coord[MAX_COORDS][2]) {
    unsigned long counter = 0;
    for (ushort row1=0; row1<len-1; row1++) {
        for (ushort row2=row1+1; row2<len; row2++) {
            counter += (coord[row1][0] == coord[row2][0]) && (coord[row1][1] == coord[row2][1]);
        }
    }
    return len - counter;
}

unsigned long run(char* s) {
    // Your code goes here
    ushort coord[MAX_COORDS][2];
    ushort folds[MAX_FOLDS][2];
    ushort n_coord = 0;
    ushort n_folds = 0;
    parse_input(s, coord, &n_coord, folds, &n_folds);
    apply_fold(n_coord, coord, folds[0][0], folds[0][1]);
    return count_uniq(n_coord, coord);
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
