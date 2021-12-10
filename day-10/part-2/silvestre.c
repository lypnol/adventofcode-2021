#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

int compare( const void* a, const void* b)
{
     unsigned long ul_a = * ( (unsigned long*) a );
     unsigned long ul_b = * ( (unsigned long*) b );

     if ( ul_a == ul_b ) return 0;
     else if ( ul_a < ul_b ) return -1;
     else return 1;
}

void update_score( unsigned long* scores, size_t n_scores, char* stack, size_t idx) {
    while (idx > 0) {
        scores[n_scores] *= 5;
        switch (stack[idx-1])
        {
        case '(':
            scores[n_scores] += 1;
            break;
        case '[':
            scores[n_scores] += 2;
            break;
        case '{':
            scores[n_scores] += 3;
            break;
        case '<':
            scores[n_scores] += 4;
            break;
        default:
            break;
        }
        idx--;
    }
}

unsigned long run(char* s) {
    char stack[200];
    size_t idx = 0;
    bool corrupted = false;
    unsigned long scores[102] = {0};
    size_t n_scores = 0;
    while (*s) {
        if (corrupted) {while (*s != '\n' && *s != '\0') s++;}
        switch (*s)
        {
        case '\n':
            if (!corrupted) {
                update_score(scores, n_scores, stack, idx);
                n_scores++;
            }
            corrupted = false;
            idx = 0;
            break;
        case ')':
            if (idx == 0 || stack[idx-1] != '(') {
                corrupted = true;
            } else {idx--;}
            break;
        case ']':
            if (idx == 0 || stack[idx-1] != '[') {
                corrupted = true;
            } else {idx--;}
            break;
        case '}':
            if (idx == 0 || stack[idx-1] != '{') {
                corrupted = true;
            } else {idx--;}
            break;
        case '>':
            if (idx == 0 || stack[idx-1] != '<') {
                corrupted = true;
            } else {idx--;}
            break;
        default:
            stack[idx] = *s;
            idx++;
            break;
        }
        s++;
    }
    if (!corrupted) {
        update_score(scores, n_scores, stack, idx);
        n_scores++;
    }
    qsort(scores, n_scores, sizeof(unsigned long), compare);
    return scores[n_scores/2];
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
