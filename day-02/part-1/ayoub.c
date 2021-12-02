#include <stdio.h>
#include <time.h>
#include <stdlib.h>

long long run(char* s) {
    size_t i = -1;
    long long h = 0, d = 0;

    while (s[++i]) {
        if (s[i] == '\n') continue;
        if (s[i] == 'f') {
            i += 8;
            h += (long long)(s[i]-'0');
            i++;
        } else if (s[i] == 'u') {
            i += 3;
            d -= (long long)(s[i]-'0');
            i++;
        } else if (s[i] == 'd') {
            i += 5;
            d += (long long)(s[i]-'0');
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

    printf("sizeof: int=%lu long=%lu long long=%lu\n", sizeof(int), sizeof(long), sizeof(long long));

    clock_t start = clock();
    long long answer = run(argv[1]);
    
    printf("_duration:%f\n%lld\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
