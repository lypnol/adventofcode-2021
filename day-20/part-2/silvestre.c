#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define INITIAL_IMAGE_SIZE 100
#define N_STEPS 50
#define MAX_IMAGE_SIZE (INITIAL_IMAGE_SIZE+(N_STEPS+1)*2)

typedef unsigned long ulong;
typedef unsigned short ushort;

typedef struct {
    bool pixels[MAX_IMAGE_SIZE][MAX_IMAGE_SIZE];
    size_t xmin;
    size_t xmax;
    size_t ymin;
    size_t ymax;
} Image;

void parse_algorithm(char **s, bool algorithm[512]) {
    size_t idx = 0;
    while (**s != '\n') {
        algorithm[idx] = (**s == '#');
        idx++;
        (*s)++;
    }
}

void parse_image(char **s, Image *image) {
    while (**s == '\n') {(*s)++;}
    for (size_t row = 0; row < INITIAL_IMAGE_SIZE; row++) {
        for (size_t col = 0; col < INITIAL_IMAGE_SIZE; col++) {
            image->pixels[row+N_STEPS+1][col+N_STEPS+1] = (**s == '#');
            (*s)++;
        }   
        (*s)++; // return line
    }
    image->xmin=N_STEPS+1;
    image->xmax=INITIAL_IMAGE_SIZE+N_STEPS+1;
    image->ymin=N_STEPS+1;
    image->ymax=INITIAL_IMAGE_SIZE+N_STEPS+1;
}

void enhance(Image *src, Image *dst, bool algorithm[512]) {
    ushort algo_idx;
    // init border
    algo_idx = (src->pixels[src->xmin -1][src->ymin -1] == false) ? 0 : 511;
    for (size_t col = src->ymin-3; col < src->ymax+3; col++) {
        dst->pixels[src->xmin-3][col] = algorithm[algo_idx];
        dst->pixels[src->xmin-2][col] = algorithm[algo_idx];
        dst->pixels[src->xmax+1][col] = algorithm[algo_idx];
        dst->pixels[src->xmax+2][col] = algorithm[algo_idx];
    }
    for (size_t row = src->xmin-3; row < src->xmax+3; row++) {
        dst->pixels[row][src->ymin-3] = algorithm[algo_idx];
        dst->pixels[row][src->ymin-2] = algorithm[algo_idx];
        dst->pixels[row][src->ymax+1] = algorithm[algo_idx];
        dst->pixels[row][src->ymax+2] = algorithm[algo_idx];
    }
    // main
    for (size_t row = src->xmin-1; row < src->xmax+1; row++) {
        for (size_t col = src->ymin-1; col < src->ymax+1; col++) {
            algo_idx = (
                (src->pixels[row-1][col-1] << 8) | 
                (src->pixels[row-1][col] << 7) | 
                (src->pixels[row-1][col+1] << 6) |
                (src->pixels[row][col-1] << 5) | 
                (src->pixels[row][col] << 4) | 
                (src->pixels[row][col+1] << 3) | 
                (src->pixels[row+1][col-1] << 2) | 
                (src->pixels[row+1][col] << 1) | 
                (src->pixels[row+1][col+1] << 0)
            );
            dst->pixels[row][col] = algorithm[algo_idx];
        }
    }
    dst->xmin = src->xmin-1;
    dst->xmax = src->xmax+1;
    dst->ymin = src->ymin-1;
    dst->ymax = src->ymax+1;
}

ulong count_pixels(Image *image) {
    ulong counter = 0;
    for (size_t row = image->xmin; row < image->xmax; row++) {
        for (size_t col = image->ymin; col < image->ymax; col++) {
            counter+=image->pixels[row][col];
        }
    }
    return counter;
}

ulong run(char* s) {
    bool algorithm[512] = {0};
    Image image1; 
    memset(image1.pixels, 0, sizeof(bool) * MAX_IMAGE_SIZE * MAX_IMAGE_SIZE);
    Image image2;
    memset(image2.pixels, 0, sizeof(bool) * MAX_IMAGE_SIZE * MAX_IMAGE_SIZE);
    parse_algorithm(&s, algorithm);
    parse_image(&s, &image1);
    for (size_t step = 0; step < N_STEPS/2; step++) {
        enhance(&image1, &image2, algorithm);
        enhance(&image2, &image1, algorithm);
    }
    return count_pixels(&image1);
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
