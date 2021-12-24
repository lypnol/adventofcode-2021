#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef unsigned long ulong;
typedef unsigned short ushort;

static ulong nb_bit_read = 0;

ulong next(char *s, ushort n) {
    static char *stream = NULL;
    static ulong buffer = 0;
    static ushort leftover = 0;

    if (s != NULL){stream = s; leftover = 0; buffer = 0; nb_bit_read = 0;}

    while (leftover < n) {
        buffer = buffer << 4 | ((*stream - '0') * (*stream <= '9') + (*stream - 'A' + 10) * (*stream > '9'));
        stream++;
        leftover += 4;
    }
    nb_bit_read += n;
    leftover -= n;
    return (buffer >> leftover) & ((1 << n )- 1);
}

ulong sum_packet_versions(void) {
    ulong acc = next(NULL, 3);
    if (next(NULL, 3) == 4) {
        // handle litteral values
        while (next(NULL, 1)) {
            next(NULL, 4);
        }
        next(NULL, 4);
        return acc;
    } else {
        // handle operators
        if (next(NULL, 1)) {
            // handle length type 1
            ulong n_subpackets = next(NULL, 11);
            for (ulong idx = 0; idx < n_subpackets; idx++) {
                acc += sum_packet_versions();
            }
            return acc;
        } else {
            // handle length type 0
            ulong subpackets_length = next(NULL, 15);
            ulong current_idx = nb_bit_read;
            while (nb_bit_read < current_idx + subpackets_length) {
                acc += sum_packet_versions();
            }
            return acc;
        }
    }
}

ulong run(char* s) {
    // Your code goes here
    next(s, 0); // init stream reader
    return sum_packet_versions();
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
