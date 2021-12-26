#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

#define INITIAL_IMAGE_SIZE 100
#define N_STEPS 2
#define MAX_IMAGE_SIZE (INITIAL_IMAGE_SIZE+(N_STEPS+1)*2)

typedef unsigned long ulong;
typedef unsigned short ushort;

void parse_algorithm(char **s, bool algorithm[512]) {
    size_t idx = 0;
    while (**s != '\n') {
        algorithm[idx] = (**s == '#');
        idx++;
        (*s)++;
    }
}

void parse_image(char **s, bool image[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE]) {
    while (**s == '\n') {(*s)++;}
    for (size_t row = 0; row < INITIAL_IMAGE_SIZE; row++) {
        for (size_t col = 0; col < INITIAL_IMAGE_SIZE; col++) {
            image[row+N_STEPS+1][col+N_STEPS+1] = (**s == '#');
            (*s)++;
        }   
        (*s)++; // return line
    }
}

void enhance(bool src[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE], bool dst[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE], bool algorithm[512]) {
    ushort algo_idx = 0;
    // init border
    algo_idx = (src[0][0] == false) ? 0 : 511;
    for (size_t col = 0; col < MAX_IMAGE_SIZE; col++) {
        dst[0][col] = algorithm[algo_idx];
        dst[MAX_IMAGE_SIZE-1][col] = algorithm[algo_idx];
    }
    for (size_t row = 0; row < MAX_IMAGE_SIZE; row++) {
        dst[row][0] = algorithm[algo_idx];
        dst[row][MAX_IMAGE_SIZE-1] = algorithm[algo_idx];
    }
    // main
    for (size_t row = 1; row < MAX_IMAGE_SIZE-1; row++) {
        for (size_t col = 1; col < MAX_IMAGE_SIZE-1; col++) {
            algo_idx = (
                (src[row-1][col-1] << 8) | 
                (src[row-1][col] << 7) | 
                (src[row-1][col+1] << 6) |
                (src[row][col-1] << 5) | 
                (src[row][col] << 4) | 
                (src[row][col+1] << 3) | 
                (src[row+1][col-1] << 2) | 
                (src[row+1][col] << 1) | 
                (src[row+1][col+1] << 0)
            );
            dst[row][col] = algorithm[algo_idx];
        }
    }
}

ulong count_pixels(bool image[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE]) {
    ulong counter = 0;
    for (size_t row = 0; row < MAX_IMAGE_SIZE; row++) {
        for (size_t col = 0; col < MAX_IMAGE_SIZE; col++) {
            counter+=image[row][col];
        }
    }
    return counter;
}

ulong run(char* s) {
    bool algorithm[512] = {0};
    bool image1[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE] = {0};
    bool image2[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE] = {0};
    parse_algorithm(&s, algorithm);
    parse_image(&s, image1);
    enhance(image1, image2, algorithm);
    enhance(image2, image1, algorithm);
    return count_pixels(image1);
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
