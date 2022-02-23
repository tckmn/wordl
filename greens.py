#!/usr/bin/env python3

import json
import random

lf = lambda x: [y for y in x if len(y) == 5 and '*' not in y]
words = lf(json.load(open('hello-wordl/src/dictionary.json')))
targs = lf(json.load(open('hello-wordl/src/targets.json')))
targs = targs[:targs.index('murky')+1]

def greens(w, t):
    return sum(1 if x==y else 0 for x,y in zip(w,t))

def yellows(w, t):
    return color(w, t).count(2)

def color(w, t):
    ret = [1 if x==y else 0 for x,y in zip(w,t)]
    bank = [y for x,y in zip(w,t) if x!=y]
    for i,ch in enumerate(w):
        if not ret[i] and ch in bank:
            ret[i] = 2
            bank.remove(ch)
    return ret
    return (((ret[0]*3+ret[1])*3+ret[2])*3+ret[3])*3+ret[4]

for w in targs:
    print(f'{w} {sum(greens(w,t) for t in targs)} {sum(yellows(w,t) for t in targs)}')
