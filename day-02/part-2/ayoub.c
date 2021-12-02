#include <stdio.h>
#include <time.h>
#include <stdlib.h>

long long run(char* s) {
    size_t i = -1;
    long long h = 0, d = 0, a = 0, x;

    while (s[++i]) {
        if (s[i] == '\n') continue;
        if (s[i] == 'f') {
            i += 8;
            x = (long long)(s[i]-'0');
            h += x;
            d += a*x;
            i++;
        } else if (s[i] == 'u') {
            i += 3;
            x = (long long)(s[i]-'0');
            a -= x;
            i++;
        } else if (s[i] == 'd') {
            i += 5;
            x = (long long)(s[i]-'0');
            a += x;
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

    clock_t start = clock();
    long long answer = run(argv[1]);
    
    printf("_duration:%f\n%lld\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
