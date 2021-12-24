#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef unsigned short ushort;
typedef unsigned long ulong;

typedef struct {
    int xmin;
    int xmax;
    int ymin;
    int ymax;
    int zmin;
    int zmax;
} cube;
void cube_from_array(cube *c, int arr[6]) {
    c->xmin = arr[0];
    c->xmax = arr[1];
    c->ymin = arr[2];
    c->ymax = arr[3];
    c->zmin = arr[4];
    c->zmax = arr[5];
}
ulong cube_volume(cube *c) {
    return (ulong)(c->xmax - c->xmin + 1) * (ulong)(c->ymax - c->ymin +1) * (ulong)(c->zmax - c->zmin +1);
}
void cube_copy(cube *original, cube *new) {
    new->xmin = original->xmin;
    new->xmax = original->xmax;
    new->ymin = original->ymin;
    new->ymax = original->ymax;
    new->zmin = original->zmin;
    new->zmax = original->zmax;
}
bool cube_are_disjoint(cube *c0, cube *c1) {
    return ( 
        c1->xmin > c0->xmax || c1->xmax < c0->xmin
        || c1->ymin > c0->ymax || c1->ymax < c0->ymin
        || c1->zmin > c0->zmax || c1->zmax < c0->zmin
    );
}

typedef struct {
    cube (*current)[4096];
    cube (*next)[4096];
    size_t current_len;
    size_t next_len;
} reactor;
void reactor_init(reactor *r) {
    r->current = calloc(4096, sizeof(cube));
    r->next = calloc(4096, sizeof(cube));
    r->current_len = 0;
    r->next_len = 0;
}
void reactor_swap(reactor *r) {
    cube (*tmp)[4096];
    tmp = r->current;
    r->current = r->next;
    r->next = tmp;

    r->current_len = r->next_len;
    r->next_len = 0;
}
void reactor_append_next(reactor *r, cube *c) {
    (*r->next)[r->next_len] = *c;
    r->next_len++;
}
ulong reactor_volume(reactor *r) {
    ulong acc = 0;
    for (size_t idx=0; idx<r->current_len; idx++){
        acc += cube_volume(&((*r->current)[idx]));
    }
    return acc;
}



void parse_line(char *s, int arr[6], bool *on) {
    s++;
    *on = (*s == 'n') ? true: (s++, false);
    s += 4;
    size_t idx = 0;
    short sign = 1;
    int acc = 0;
    while (*s != '\n' && *s) {
        switch (*s) {
        case ',':
            arr[idx] = sign * acc;
            sign = 1;
            acc = 0;
            idx++;
            s += 3;
            break;
        case '.':
            arr[idx] = sign * acc;
            sign = 1;
            acc = 0;
            idx++;
            s += 2;
            break;
        case '-':
            sign = -1;
            s++;
            break;
        default:
            acc = 10 * acc + (short)(*s - '0');
            s++;
            break;
        }
    }
    arr[idx] = sign * acc;
}



void reactor_split_current_cubes(reactor *r, cube *c1) {
    int xmin, ymin, zmin;
    cube new, *c0; 
    for (size_t current_idx = 0; current_idx < r->current_len; current_idx++) {
        c0 = &((*r->current)[current_idx]);        
        if (cube_are_disjoint(c1, c0)) {
            reactor_append_next(r, c0);
        } else {
            // intersection ! 
            cube_copy(c0, &new);
            xmin = new.xmin;
            ymin = new.ymin;
            zmin = new.zmin;
            if (/*left*/ c0->xmin < c1->xmin) {
                new.xmax = c1->xmin - 1;
                reactor_append_next(r, &new);
                new.xmax = c0->xmax;
                xmin = c1->xmin;
            }
            if (/*right*/ c0->xmax > c1->xmax) {
                new.xmin = c1->xmax + 1;
                reactor_append_next(r, &new);
                new.xmin = c0->xmin;
                new.xmax = c1->xmax;
            }
            new.xmin = xmin;
            if (/*bottom*/ c0->ymin < c1->ymin) {
                new.ymax = c1->ymin - 1;
                reactor_append_next(r, &new);
                new.ymax = c0->ymax;
                ymin = c1->ymin;
            } 
            if (/*top*/ c0->ymax > c1->ymax) {
                new.ymin = c1->ymax + 1;
                reactor_append_next(r, &new);
                new.ymin = c0->ymin;
                new.ymax = c1->ymax;
            } 
            new.ymin = ymin;
            if (/*behind*/ c0->zmin < c1->zmin) {
                new.zmax = c1->zmin - 1;
                reactor_append_next(r, &new);
                new.zmax = c0->zmax;
                zmin = c1->zmin;
            } 
            if (/*in-front*/ c0->zmax > c1->zmax) {
                new.zmin = c1->zmax + 1;
                reactor_append_next(r, &new);
                new.zmin = c0->zmin;
                new.zmax = c1->zmax;
            } 
            new.zmin = zmin; 
        }
    }
}


ulong run(char* s) {
    bool on;
    cube c;
    int arr[6];
    reactor r;
    reactor_init(&r);

    char *newline;
    while(s) {
        newline = strchr(s, '\n');
        parse_line(s, arr, &on);
        cube_from_array(&c, arr);
        reactor_split_current_cubes(&r, &c);
        if (on) {reactor_append_next(&r, &c);}
        reactor_swap(&r);
        s = newline ? newline + 1: NULL;
    }
    return reactor_volume(&r);
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
