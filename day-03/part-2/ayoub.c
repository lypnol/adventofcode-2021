#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define SIZE 12
#define REPORT_SIZE 1000
#define MASK 0x0FFF

typedef unsigned short Number;

const Number BIT_MASK[SIZE] = {
    0x0800, 0x0400, 0x0200, 0x0100,
    0x0080, 0x0040, 0x0020, 0x0010,
    0x0008, 0x0004, 0x0002, 0x0001
};

unsigned long run(char* s) {
    Number o2 = 0x0000, co2 = 0x0000, prefix = 0x0000;
    size_t i = -1, k = 0;
    int zeros[SIZE][MASK+1] = {0}, ones[SIZE][MASK+1] = {0};
    int count_with_prefix[SIZE][MASK+1] = {0};
    Number with_prefix[MASK+1] = {0};
    Number prefixes[SIZE] = {0};

    while (s[++i]) {
        if (s[i] == '1' || s[i] == '0') {
            if (s[i] == '1') ones[k][prefix]++;
            else zeros[k][prefix]++;
            prefix = prefix|((s[i] == '1')?BIT_MASK[k]:0x0000);
            prefixes[k] = prefix;
            count_with_prefix[k][prefix]++; 
            k++;
        } else {
            for (k = 0; k < SIZE; k++) {
                with_prefix[prefixes[k]] = prefix;
                prefixes[k] = 0x0000;
            }
            k = 0;
            prefix = 0x0000;
        }
    }

    if (k != 0) {
        for (k = 0; k < SIZE; k++) {
            with_prefix[prefixes[k]] = prefix;
            prefixes[k] = 0x0000;
        }
    }

    prefix = 0x0000;
    for (k = 0; k < SIZE; k++) {
        if (ones[k][prefix] != zeros[k][prefix]) {
            prefix = prefix|((ones[k][prefix] > zeros[k][prefix])?BIT_MASK[k]:0x0000);
        } else if (ones[k][prefix] == zeros[k][prefix]) {
            prefix = prefix|BIT_MASK[k];
        }
        if (count_with_prefix[k][prefix] == 1) {
            o2 = with_prefix[prefix];
            break;
        }
    }

    prefix = 0x0000;
    for (k = 0; k < SIZE; k++) {
        if (ones[k][prefix] != zeros[k][prefix]) {
            prefix = prefix|((ones[k][prefix] < zeros[k][prefix])?BIT_MASK[k]:0x0000);
        }
        if (count_with_prefix[k][prefix] == 1) {
            co2 = with_prefix[prefix];
            break;
        }
    }

    return ((unsigned long)o2)*((unsigned long)co2);
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    unsigned long answer = run(argv[1]);
    
    printf("_duration:%f\n%ld\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
