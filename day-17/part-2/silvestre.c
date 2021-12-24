#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

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

bool reach_area(short vx, short vy, area *area) {
    short x, y;
    x = y = 0;
    while (x <= area->xe && y >= area->ys) {
        x += vx;
        y += vy;
        vx = vx == 0 ? 0 : vx - 1;
        vy--;
        if (x >= area->xs && x <= area->xe && y >= area->ys && y <= area->ye) {
            return true;
        }
    }
    return false;
}

short _sqrt(short a) { // newton method
    double x = a / 10;
    while (x*x - a > 0.01 || x*x - a < -0.01) {
        x = 0.5 * (x + a / x);
    }
    return (short) x;
}

short run(char* s) {
    area area = parse(s);
    short counter = 0;
    short vxmin = _sqrt(1 + 8 * area.xs) / 2;
    short vxmax = area.xe;
    short vymin = area.ys;
    short vymax = -1 * area.ys;
    for (short vx = vxmin; vx < vxmax + 1; vx++) {
        for (short vy = vymin; vy < vymax + 1; vy++) {
            counter += reach_area(vx, vy, &area);
        }
    }
    return counter;
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
