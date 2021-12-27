#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef unsigned short ushort;
typedef unsigned long ulong;
typedef unsigned long long ullong;

typedef struct {
    ushort pos1; // 1 -> 10 
    ushort pos2; // 1 -> 10
    ushort score1; // 1 -> 1000
    ushort score2; // 1 -> 1000
} Game;

typedef struct {
    Game key;
    ullong value;
    LinkedListNode *next;
} LinkedListNode;


#define PRIME 193

typedef struct {
    LinkedListNode mapping[PRIME];
    ulong a[4];
} Dict;

void dict_init(Dict *dict, ulong seed) {
    srand(seed);
    for (size_t i=0; i<4; i++) {dict->a[i] = rand() % PRIME;}
    memset(dict->mapping, 0, PRIME * sizeof(LinkedListNode));
}

void dict_add(Game *key, ullong value) {

}

void parse_input(char *s, Game *game) {
    s += 28;
    ushort acc = 0;
    while (*s != '\n') {
        acc = 10 * acc + (ushort)(*s - '0');
        s++;
    }
    game->pos1 = acc;
    acc = 0;
    s += 29;
    while (*s != '\0') {
        acc = 10 * acc + (ushort)(*s - '0');
        s++;
    }
    game->pos2 = acc;
}

ulong run(char *s) {
    Game game = {0, 0, 0, 0};
    parse_input(s, &game);
    Dict dict;
    dict_init(&dict, 0);
    while (true) {
        // player 1
        for (ushort i = 0; i < 3; i++) {
            game.pos1 += game.dice;
            game.dice %= 100;
            game.dice++;
        }
        game.pos1 %= 10;
        game.score1 += game.pos1 + (game.pos1 == 0) * 10;
        game.nrolls+=3;
        if (game.score1 >= 1000) {return (ulong)(game.score2) * game.nrolls;}

        // player 2
        for (ushort i = 0; i < 3; i++) {
            game.pos2 += game.dice;
            game.dice %= 100;
            game.dice++;
        }
        game.pos2--;
        game.pos2 %= 10;
        game.pos2++;
        game.score2 += game.pos2;
        game.nrolls+=3;
        if (game.score2 >= 1000) {return (ulong)(game.score1) * game.nrolls;}
    }
    return 0;
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
