#include <stdio.h>
#include <time.h>
#include <stdlib.h>

unsigned int run(char* s) {
    size_t i = 0;
    unsigned long depth = 0;
    unsigned long forward = 0;
    unsigned long aim = 0;

    while (1) {
        if (s[i] == 'f')
        {
            forward += (s[i + 8] - '0');
            depth += (aim * (s[i + 8] - '0'));
            i += 9; // skip over number
        }
        else if (s[i] == 'u')
        {
            aim -= (s[i + 3] - '0');
            i += 4; // skip over number
        }
        else if (s[i] == 'd')
        {
            aim += (s[i + 5] - '0');
            i += 6;  // skip over number
        }
        if (s[i] == '\0'){
            break;
        }
        i++; // skip over \n
    }
    return depth * forward;
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
