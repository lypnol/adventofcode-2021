#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>

unsigned long run(char* s) {
    char stack[200];
    size_t idx = 0;
    bool corrupted = false;
    unsigned int counter = 0;
    while (*s) {
        if (corrupted) {while (*s != '\n' && *s != '\0') s++;}
        switch (*s)
        {
        case '\n':
            corrupted = false;
            idx = 0;
            break;
        case ')':
            if (idx == 0 || stack[idx-1] != '(') {
                corrupted = true;
                counter += 3;
            } else {idx--;}
            break;
        case ']':
            if (idx == 0 || stack[idx-1] != '[') {
                corrupted = true;
                counter += 57;
            } else {idx--;}
            break;
        case '}':
            if (idx == 0 || stack[idx-1] != '{') {
                corrupted = true;
                counter += 1197;
            } else {idx--;}
            break;
        case '>':
            if (idx == 0 || stack[idx-1] != '<') {
                corrupted = true;
                counter += 25137;
            } else {idx--;}
            break;
        default:
            stack[idx] = *s;
            idx++;
            break;
        }
        s++;
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
    unsigned long answer = run(argv[1]);
    
    printf("_duration:%f\n%lu\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
