#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

// change these
#ifndef LENGTH
#define LENGTH 5
#endif

// don't care about these
#define BUF 200
#define WBUF 2500
#define GYSHIFT 32768
#if LENGTH <= 5
#define COLOR unsigned char
#else
#define COLOR int
#endif

#if defined DEBUG2 || defined TREE
#define DEBUG
#endif

#define fakequote(x) #x
#define quote(x) fakequote(x)

typedef struct {
    char word[LENGTH];
    COLOR x;
#ifdef TREE
    int d;
#endif
} xword;

int used[LENGTH];

#ifdef DEBUG
xword *origwords;
int depth;
#endif

// ternary
// 0 = green
// 1 = yellow
// 2 = gray
COLOR color(char *word, char *guess) {
    COLOR ret = 0;
    for (int i = 0; i < LENGTH; ++i) used[i] = 0;
    for (int i = 0; i < LENGTH; ++i) {
        ret *= 3;
        if (guess[i] != word[i]) {
            for (int j = 0; j < LENGTH; ++j) {
                if (guess[i] == word[j] && guess[j] != word[j] && !used[j]) {
                    used[j] = 1;
                    ret += 1;
                    goto done;
                }
            }
            ret += 2;
        }
        done: 0;
    }
    return ret;
}

char ccbuf1[LENGTH+1], ccbuf2[LENGTH+1];
char *convcol(COLOR col) {
    for (int i = 0; i < LENGTH; ++i) {
        ccbuf1[LENGTH-1-i] = "Gy."[col % 3];
        col /= 3;
    }
    return ccbuf1;
}
char *convcolb(char *buf, COLOR col) {
    for (int i = 0; i < LENGTH; ++i) {
        buf[LENGTH-1-i] = "Gy."[col % 3];
        col /= 3;
    }
    return buf;
}

int cmp(const void *a, const void *b) {
    return (*(xword*)a).x - (*(xword*)b).x;
}

#define FSTART do { \
    for (int i = 0; i < nw; ++i) { \
        words[i].x = color(words[i].word, guess); \
    } \
    qsort(words, nw, sizeof *words, cmp); \
    COLOR curgroup = 0; \
    int ngroup = 0; \
    for (int i = 1; i <= nw; ++i) { \
        if (i != nw && words[i].x == curgroup) { \
            ++ngroup; \
        } else {

#define FEND \
            curgroup = words[i].x; \
            ngroup = 1; \
        } \
    } \
} while (0)

int basedata(xword *words, int nw, char *guess) {
    int twos = 0, maxgroup = 0;
    FSTART {
        if (ngroup > 1) {
            if (ngroup > maxgroup) maxgroup = ngroup;
        } else {
            ++twos;
        }
    } FEND;
    return maxgroup * 1000 + twos;
}

unsigned long long total(xword *words, int nw, char *guess) {
    unsigned long long suptotal = 1;
    FSTART {
        if (ngroup > 1) {
            xword *base = words + i - ngroup;
            size_t chunk = ngroup * sizeof *base;

            xword *xbest = malloc(chunk);
            memcpy(xbest, base, chunk);
            unsigned long long subtotal = 0;

            for (int j = 0; j < ngroup; ++j) {
                subtotal += total(base, ngroup, xbest[j].word);
            }

            if (!subtotal) printf("%d %llu\n", nw, subtotal);
            suptotal *= subtotal;
            free(xbest);
        }
    } FEND;
    return suptotal;
}

int evaluate(xword *words, int nw, char *guess) {
#ifdef DEBUG
    ++depth;
#endif

    int worst = 0;

    FSTART {
        if (ngroup > 1) {
            xword *base = words + i - ngroup;
            int best = 999;
            size_t chunk = ngroup * sizeof *base;

            // this thing stores both the best ordering so far (in the
            // first half) as well as the original ordering (in the next
            // half) for iteration
            xword *xbest = malloc(2*chunk);
            memcpy(xbest + ngroup, base, chunk);

            for (int j = 0; j < ngroup; ++j) {
                int ret = evaluate(base, ngroup, xbest[ngroup+j].word);
                if (ret < best) {
                    best = ret;
                    memcpy(xbest, base, chunk);
                }
            }

            if (best > worst) worst = best;
            memcpy(base, xbest, chunk);
            free(xbest);
        }

#ifdef TREE
        words[i - ngroup].d = depth;
        if (curgroup) words[i - ngroup].x = curgroup;
#endif
    } FEND;

#ifdef DEBUG
    --depth;
#endif

    return worst+1;
}

int counts(xword *words, int nw, char *guess) {
    int greens = 0, yellows = 0;
    for (int i = 0; i < nw; ++i) {
        char *col = convcol(color(words[i].word, guess));
        for (int j = 0; j < LENGTH; ++j) {
            if (col[j] == 'G') ++greens;
            else if (col[j] == 'y') ++yellows;
        }
    }
    return greens * GYSHIFT + yellows;
}

int counts2(xword *words, int nw, char *g1, char *g2) {
    int greens = 0, yellows = 0;
    for (int i = 0; i < nw; ++i) {
        char *c1 = convcolb(ccbuf1, color(words[i].word, g1)),
             *c2 = convcolb(ccbuf2, color(words[i].word, g2));
        for (int j = 0; j < LENGTH; ++j) {
            if (c1[j] == 'G' || c2[j] == 'G') ++greens;
            else if (c1[j] == 'y' || c2[j] == 'y') ++yellows;
        }
    }
    return greens * GYSHIFT + yellows;
}

int counts3(xword *words, int nw, char *g1, char *g2, char *g3) {
    int greens = 0, yellows = 0;
    for (int i = 0; i < nw; ++i) {
        char *c1 = convcol(color(words[i].word, g1)),
             *c2 = convcol(color(words[i].word, g2)),
             *c3 = convcol(color(words[i].word, g3));
        for (int j = 0; j < LENGTH; ++j) {
            if (c1[j] == 'G' || c2[j] == 'G' || c3[j] == 'G') ++greens;
            else if (c1[j] == 'y' || c2[j] == 'y' || c3[j] == 'y') ++yellows;
        }
    }
    return greens * GYSHIFT + yellows;
}

int filter(char *word) {
#ifdef FILTER
    return strstr(convcol(color(word, "slate")), quote(FILTER)) != 0
        && strstr(convcol(color(word, "finer")), "...yy") != 0;
        ;
#else
    return 1;
#endif
}

int main() {
    FILE *fp = fopen("hello-wordl/src/targets.json", "r");
    char line[BUF];
    xword words[WBUF];
    char wlist[WBUF*LENGTH];
    int nw = 0;
    while (fgets(line, BUF, fp)) {
        if (strlen(line) == LENGTH+6 && line[3] != '*' && filter(line+3)) {
            strncpy(wlist + nw*LENGTH, line+3, LENGTH);
            strncpy(words[nw++].word, line+3, LENGTH);
        }
        if (strstr(line, "\"murky\"")) break;
    }
    fclose(fp);

#ifdef DEBUG
    origwords = words;
    depth = 0;
#endif

#ifdef TREE
    evaluate(words, nw, quote(TREE));
    for (int i = 0; i < nw; ++i) {
        for (int j = 0; j < words[i].d; ++j) printf("    ");
        printf("%.*s %s\n", LENGTH, words[i].word, convcol(words[i].x));
    }
    return 0;
#endif

#ifdef TRIPLES
    for (int i = 0; i < nw; ++i) {
        for (int j = i+1; j < nw; ++j) {
            int cols = counts2(words, nw, wlist + i*LENGTH, wlist + j*LENGTH);
            int g = cols/GYSHIFT;
            int y = cols%GYSHIFT;
            if (g > 2800) printf("%.*s\t%.*s\t%d\t%d\t%d\n",
                    LENGTH,
                    wlist + i*LENGTH,
                    LENGTH,
                    wlist + j*LENGTH,
                    g, y, g+y
                    );
            /* for (int k = j+1; k < nw; ++k) { */
            /*     int cols = counts3(words, nw, wlist + i*LENGTH, wlist + j*LENGTH, wlist + k*LENGTH); */
            /*     if (cols / GYSHIFT > 1800) printf("%.*s\t%.*s\t%.*s\t%d\t%d\t%d\n", */
            /*             LENGTH, */
            /*             wlist + i*LENGTH, */
            /*             LENGTH, */
            /*             wlist + j*LENGTH, */
            /*             LENGTH, */
            /*             wlist + k*LENGTH, */
            /*             cols / GYSHIFT, */
            /*             cols % GYSHIFT, */
            /*             (cols / GYSHIFT) + (cols % GYSHIFT) */
            /*             ); */
            /* } */
        }
    }
    return 0;
#endif

    struct timeval start, stop;
    for (int i = 0; i < nw; ++i) {

        // do the main thing
        gettimeofday(&start, NULL);
        /* int ret = evaluate(words, nw, wlist + i*LENGTH); */
        int ret = 0;
        gettimeofday(&stop, NULL);

        // do the coloring things
        int cols = counts(words, nw, wlist + i*LENGTH);

        // do the level 1 things
        int twos = basedata(words, nw, wlist + i*LENGTH);

        // out
        printf("%.*s\t%d\t%d\t%lu\t%d\t%d\t%d\t%d\t%d\n",
                LENGTH,
                wlist + i*LENGTH,
                i+1, // freq
                ret, // max depth
                (stop.tv_sec-start.tv_sec)*1000000+stop.tv_usec-start.tv_usec, // comp time
                cols / GYSHIFT, // greens
                cols % GYSHIFT, // yellows
                (cols / GYSHIFT) + (cols % GYSHIFT), // green+yellow
                twos / 1000, // max width
                twos % 1000 // size-1 groups
              );
    }
}
