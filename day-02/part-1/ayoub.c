#include <stdio.h>
#include <time.h>
#include <stdlib.h>

int run(char* s) {
    int i = -1;
    int h = 0, d = 0;

    while (s[++i]) {
        if (s[i] == '\n') continue;
        if (s[i] == 'f') {
            i += 8;
            h += (int)(s[i]-'0');
            i++;
        } else if (s[i] == 'u') {
            i += 3;
            d -= (int)(s[i]-'0');
            i++;
        } else if (s[i] == 'd') {
            i += 5;
            d += (int)(s[i]-'0');
            i++;
        }
    }

    return d*h;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    printf("sizeof: int=%d int32_t=%d uint64_t=%d\n", sizeof(int), sizeof(int32_t), sizeof(uint64_t));

    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
