#include <stdio.h>
#include <time.h>
#include <stdlib.h>

typedef struct {
    short xs;
    short xe;
    short ys;
    short ye;
} area;

area parse(char *s) {
    area area;
    short mode = 0;
    short acc = 0;
    short sign = 1;
    s+=15;
    while (*s)  {
        switch (*s)
        {
        case '-':
            sign = -1;
            break;
        case '.':
            if (mode == 0) {
                area.xs = sign * acc;
                sign = 1;
                mode = 1;
            } else { 
                area.ys = sign * acc;
                sign = 1;
            }
            acc = 0;
            s++;
            break;
        case ',':
            area.xe = acc;
            sign = 1;
            acc = 0;
            s+=3;
            break;
        default:
            acc = 10 * acc + (short)(*s - '0');
            break;
        }
        s++;
    }
    area.ye = sign * acc;
    return area;
}

short run(char* s) {
    area area = parse(s);
    return (area.ys + 1) * area.ys / 2;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    short answer = run(argv[1]);
    
    printf("_duration:%f\n%u\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
