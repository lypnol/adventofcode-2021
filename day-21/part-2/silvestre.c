#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef unsigned short ushort;
typedef unsigned long ulong;
typedef unsigned long long ullong;

typedef struct {
    size_t pos1; // 1 -> 10 
    size_t pos2; // 1 -> 10
    size_t score1; // 1 -> 21
    size_t score2; // 1 -> 21
    size_t to_move; // 1 -> 2
} Game;

#define MAP_SIZE (21*21*10*10*2)
typedef struct {
    ullong player1;
    ullong player2;
} WinCount;

void add(WinCount *left, WinCount *right) {
    left->player1 += right->player1;
    left->player2 += right->player2;
}

void int_multiply(WinCount *left, ullong right) {
    left->player1 *= right;
    left->player2 *= right;
}

size_t hash(Game *game) {
    return (game->pos1-1) + ( (game->pos2-1) * 10 ) + ( (game->score1-1) * 100 ) + ( (game->score2-1) * 2100 ) + ( (game->to_move-1) * 21 * 2100);
}

WinCount get(WinCount dict[MAP_SIZE], Game *game) {return dict[hash(game)];}

void set(WinCount dict[MAP_SIZE], Game *game, WinCount value) {dict[hash(game)] = value;}

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

ullong dice_multiplier[7] = {1,3,6,7,6,3,1};

WinCount count_wins(Game *game, WinCount dict[MAP_SIZE]) {
    WinCount counter = get(dict, game);
    if (counter.player1 > 0 || counter.player2 > 0) {
        return counter;
    } else /* {0, 0} */ {
        // check victory 
        if (game->score1 >= 21) {
            counter.player1 = 1;
        } else if (game->score2 >= 21) {
            counter.player2 = 1;
        } else {
            // update counter;
            Game new;
            WinCount tmp;
            for (size_t dice = 3; dice <= 9; dice++) {
                memcpy(&new, game, sizeof(Game));
                if (new.to_move == 1) {
                    // move player 1
                    new.pos1 += dice;
                    new.pos1 %= 10;
                    new.score1 += new.pos1 + (new.pos1 == 0) * 10;
                } else {
                    // move player 2
                    new.pos2 += dice;
                    new.pos2 %= 10;
                    new.score2 += new.pos2 + (new.pos2 == 0) * 10;
                }
                new.to_move = new.to_move == 1 ? 2 : 1;
                tmp = count_wins(&new, dict);
                int_multiply(&tmp, dice_multiplier[dice-3]);
                add(&counter, &tmp);
            }
        }
        // clean key
        set(dict, game, counter);
        return counter;
    }
}

ullong run(char *s) {
    Game game = {0, 0, 0, 0, 1};
    parse_input(s, &game);
    WinCount dict[MAP_SIZE] = {0};
    WinCount res = count_wins(&game, dict);
    return res.player1 > res.player2 ? res.player1 : res.player2;
} 


int main(int argc, char** argv)
{
    if (argc < 2) {
        printf("Missing one argument\n");
        exit(1);
    }

    clock_t start = clock();
    ullong answer = run(argv[1]);
    
    printf("_duration:%f\n%llu\n", (float)( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC, answer);
    return 0;
}
