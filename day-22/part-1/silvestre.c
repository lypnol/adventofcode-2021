#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef unsigned short ushort;
typedef unsigned long ulong;
typedef short area[6];

void parse_line(char *s, area current, bool *on) {
    s++;
    *on = (*s == 'n') ? true: (s++, false);
    s += 4;
    size_t idx = 0;
    short sign = 1;
    short acc = 0;
    while (*s != '\n' && *s) {
        switch (*s) {
        case ',':
            current[idx] = (sign * acc) + 50;
            sign = 1;
            acc = 0;
            idx++;
            s += 3;
            break;
        case '.':
            current[idx] = (sign * acc) + 50;
            sign = 1;
            acc = 0;
            idx++;
            s += 2;
            break;
        case '-':
            sign = -1;
            s++;
            break;
        default:
            acc = 10 * acc + (short)(*s - '0');
            s++;
            break;
        }
    }
    current[idx] = (sign * acc) + 50;
}

void update_matrix(__int128 matrix[101][101], area current, bool on) {
    __int128 zmask = 1;
    zmask <<= current[5]-current[4]+1;
    zmask -= 1;
    zmask <<= current[4];
    for (size_t x =  current[0]; x < current[1]+1; x++) {
        for (size_t y = current[2]; y < current[3]+1; y++) {
            if (on) {
                matrix[x][y] |= zmask;
            } else {
                matrix[x][y] &= ~zmask;
            }
        }
    }
}

ulong non_zero(__int128 matrix[101][101]) {
    ulong counter = 0;
    __int128 value;
    for (size_t x = 0; x < 101; x++) {
        for (size_t y = 0; y < 101; y++) {
            value = matrix[x][y];
            for (ushort z = 0; z < 101; z++) {
                if (value & 1) {
                    counter++;
                } 
                value >>= 1;
            }
        }
    }
    return counter;
}

ulong run(char* s) {
    __int128 matrix[101][101] = {0};
    area current;
    bool on;
    bool skip = false;
    char *newline;
    while(s) {
        newline = strchr(s, '\n');
        parse_line(s, current, &on);
        for (size_t idx = 0; idx < 6; idx++) {
            if (current[idx] < 0 || current[idx] > 100) {skip = true;}
        }
        if (!skip) {
            update_matrix(matrix, current, on);
        }
        skip = false;
        s = newline ? newline + 1: NULL;
    }
    return non_zero(matrix);
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    ulong answer = run(argv[1]);
    
    printf("_duration:%f\n%lu\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
