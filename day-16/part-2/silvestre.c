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

ulong next_packet_value(void) {
    next(NULL, 3); // version
    ushort type_id = next(NULL, 3);
    if (type_id == 4) {
        // handle litteral values
        ulong acc = 0;
        while (next(NULL, 1)) {
            acc = acc << 4 | next(NULL, 4);
        }
        acc = acc << 4 | next(NULL, 4);
        //printf("litteral %lu\n", acc);
        return acc;
    } else {
        ulong length_type_id = next(NULL, 1);
        ulong n = next(NULL, length_type_id ? 11 : 15);
        ulong b = nb_bit_read;
        ulong acc = next_packet_value();
        ulong p = 1;
        //printf("type_id = %lu, length_type_id=%lu, n=%lu\n", type_id, length_type_id, n);
        ulong new;
        while ( ((!length_type_id) && (nb_bit_read < b + n)) || ((length_type_id) && (p < n))) {
            switch (type_id) {
            case 0:
                acc += next_packet_value();
                break;
            case 1:
                acc *= next_packet_value();
                break;
            case 2:
                new = next_packet_value();
                acc = new < acc ? new : acc;
                break; 
            case 3:
                new = next_packet_value();
                acc = new > acc ? new : acc;
                break; 
            case 5:
                new = next_packet_value();
                acc = acc > new ? 1 : 0;
                break;  
            case 6:
                new = next_packet_value();
                acc = acc < new ? 1 : 0;
                break; 
            case 7:
                new = next_packet_value();
                acc = acc == new ? 1 : 0;
                break; 
            }
            p++;
        }
        return acc;
    }
}

ulong run(char* s) {
    // Your code goes here
    next(s, 0); // init stream reader
    return next_packet_value();
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
