#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define SIZE 12

int run(char* s) {
    int gamma = 0, epsilon = 0;
    size_t i = -1, k = -1;
    int zeros[SIZE] = {0}, ones[SIZE] = {0};

    while (s[++i]) {
        if (s[i] == '1') ones[++k]++;
        else if (s[i] == '0') zeros[++k]++;
        else k = -1;
    }

    for (k = 0; k < SIZE; k++) {
        gamma = gamma*2 + ((ones[k] > zeros[k])?1:0);
        epsilon = epsilon*2 + ((ones[k] < zeros[k])?1:0);
    }

    return gamma*epsilon;
}

int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    int answer = run(argv[1]);
    
    printf("_duration:%f\n%d\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
