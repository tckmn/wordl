#!/usr/bin/env python3

debug = 0

import json
import re
import sys
from collections import Counter, defaultdict
from functools import reduce

def color(w, t):
    ret = [1 if x==y else 0 for x,y in zip(w,t)]
    bank = [y for x,y in zip(w,t) if x!=y]
    for i,ch in enumerate(w):
        if not ret[i] and ch in bank:
            ret[i] = 2
            bank.remove(ch)
    return tuple(ret)
    return (((ret[0]*3+ret[1])*3+ret[2])*3+ret[3])*3+ret[4]

def legal(x, guess, col):
    colored = [guess[i] for i in range(5) if col[i] != 0]
    for i,c in enumerate(col):
        # if c == 0 and any(col[j] == 0 and x[j] == guess[i] for j in range(5)): return False
        # if c == 1 and guess[i] != x[i]: return False
        # if c == 2 and not any(col[j] != 1 and x[j] == guess[i] for j in range(5)): return False
        if c == 0 and (guess[i] == x[i] or x.count(guess[i]) > colored.count(guess[i])): return False
        if c == 1 and guess[i] != x[i]: return False
        if c == 2 and (guess[i] == x[i] or x.count(guess[i]) < colored.count(guess[i])): return False
    return True

def evaluate(targ):
    # print(f'evaluate {targ}')
    trying = guesslist[:]
    for attempt in range(1,99999):
        guess, *trying = trying
        if debug: print(guess, color(guess, targ), guesslist.index(guess))
        if targ == guess: return attempt
        trying = [x for x in trying if legal(x, guess, color(guess, targ))]

lf = lambda x: [y for y in x if len(y) == 5 and '*' not in y]
words = lf(json.load(open('hello-wordl/src/dictionary.json')))
targs = lf(json.load(open('hello-wordl/src/targets.json')))
targs = targs[:targs.index('murky')+1]

# print(Counter(tuple(color('learn', x)) for x in targs).values())

# def strategize(subset, guess):
#     return 1+max([0 if len(v) == 1 else min(strategize(v, nextguess) for nextguess in v) for v in reduce(lambda grp, x: grp[color(guess, x)].append(x) or grp, subset, defaultdict(list)).values()])

# print(strategize(targs, 'learn'))

def strategize(subset, guess):
    worst = 0
    guesses = [guess]
    for v in reduce(lambda grp, x: grp[color(guess, x)].append(x) or grp, subset, defaultdict(list)).values():
        if len(v) == 1:
            if v[0] != guess: guesses.append(v[0])
        else:
            worst2, guesses2 = min((strategize(v, nextguess) for nextguess in v), key=lambda x: x[0])
            if worst2 > worst: worst = worst2
            guesses.extend(guesses2)
    return (1+worst, guesses)

ipt = input()
print(Counter(tuple(color(ipt, x)) for x in targs).values(), file=sys.stderr)

worst, guesses = strategize(targs, ipt)
print('\n'.join(guesses))
print(worst)
