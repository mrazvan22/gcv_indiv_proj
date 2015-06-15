#ifndef AVG_GDV_H
#define AVG_GDV_H

#include "utils.cpp"

int64* count_graphlets(struct graph graph_res);
struct graph parse_leda_file(FILE *f);

#define Connect(i,j) (adjmat[i][(j)/8] |= 1<<((j)%8))
#define Connected(i,j) (adjmat[i][(j)/8] & (1<<((j)%8)))

#endif

