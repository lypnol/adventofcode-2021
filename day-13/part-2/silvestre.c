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

void init_display_bounds(ushort coord[MAX_COORDS][2], ushort n_coord, ushort* x_max, ushort* y_max) {
    *x_max = 0;
    *y_max = 0;
    for (ushort coord_idx=0; coord_idx < n_coord; coord_idx++){
        *x_max = coord[coord_idx][1] > *x_max ? coord[coord_idx][1] : *x_max;
        *y_max = coord[coord_idx][0] > *y_max ? coord[coord_idx][0] : *y_max; 
    }
    (*x_max)+= 3; // + 2 because of line feed and parser requirements
    (*y_max)++;
}

void init_result(char* result, ushort coord[MAX_COORDS][2], ushort n_coord, ushort x_max, ushort y_max) {
    for (ushort i=0; i < y_max; i++) {
        for (ushort j=0; j < x_max-1; j++) {result[i*x_max+j] = '.';}
        result[i*x_max+(x_max-1)] = '\n';
    }
    for (ushort coord_idx=0; coord_idx<n_coord; coord_idx++) {
        result[coord[coord_idx][0] * x_max + coord[coord_idx][1]] = '#';
    }
}

char* run(char* s) {
    // Your code goes here
    ushort coord[MAX_COORDS][2];
    ushort folds[MAX_FOLDS][2];
    ushort n_coord = 0;
    ushort n_folds = 0;
    parse_input(s, coord, &n_coord, folds, &n_folds);
    for (ushort fold_idx=0; fold_idx<n_folds; fold_idx++) {
        apply_fold(n_coord, coord, folds[fold_idx][0], folds[fold_idx][1]);
    }
    ushort x_max = 0;
    ushort y_max = 0;
    init_display_bounds(coord, n_coord, &x_max, &y_max);
    //printf("x_max=%d, y_max=%d", x_max, y_max);
    char* result = (char *) malloc(x_max * y_max * sizeof(char));
    init_result(result, coord, n_coord, x_max, y_max);
    return result;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    char* answer = run(argv[1]);
    
    printf("_duration:%f\n_parse\n%s\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
