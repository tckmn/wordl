#!/usr/bin/env python3

debug = 0

import json
import re

def color(w, t):
    ret = [1 if x==y else 0 for x,y in zip(w,t)]
    bank = [y for x,y in zip(w,t) if x!=y]
    for i,ch in enumerate(w):
        if not ret[i] and ch in bank:
            ret[i] = 2
            bank.remove(ch)
    return ret
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

# bumped = [x for x in targs if sum(x.count(c) for c in 'eartolsinchudpymgbfvkwxzqj') > 1]
# bumped = [x for x in targs if sum(x.count(c) for c in 'chudpymgbf') > 2]
# print(len(bumped))
# guesslist = bumped + [x for x in targs if x not in bumped]
# bumped = ['learn']
# guesslist = bumped + [x for x in targs if x not in bumped]
# guesslist = bumped + sorted([x for x in targs if x not in bumped], key=lambda x:len(set(x)))
# guesslist = ['learn'] + sorted([x for x in targs if x != 'learn'], key=lambda x:len(set(x)))

# guesslist = sorted(targs, key=lambda x: -len(set(x)))
# bumped = ['aeons']

guesslist = targs[:]
bumped = [
    'learn',
    'nymph', 'swing',
    'prove',
    'evade',
    'wharf'
]
guesslist = bumped + [x for x in guesslist if x not in bumped]
debumped = [x for x in guesslist if re.fullmatch(r'.oun.|.atch|about|above', x)]
guesslist = [x for x in guesslist if x not in debumped] + debumped
# debumped = [x for x in guesslist if re.fullmatch(r'.i.er|.aste|.ound|.atch|cause|their|faith|point|young|state|board|start', x)]

guesslist = sorted(targs, key=lambda x: (-len(set(x)), sum('eartolsinchudpymgbfvkwxzqj'.index(c) for c in x)))

guesslist = [x[:-1] for x in open(f'branch-{input()}').readlines() if len(x)>4]


if 0:
    for x in '''

6 brake
6 erase
6 graze
6 match


'''.split('\n'):
        if not x: continue
        evaluate(x.split()[1])
        print()

    # print([x for x in targs if sum(1 for c in 'fsbwmph' if c in x) > 2 and 'n' in x and all(c not in x for c in 'lear')])
    # print([x for x in targs if sum(1 for c in 'fsbw' if c in x) > 1 and 'n' in x and all(c not in x for c in 'learymph')]) # ['swing', 'bonus', 'snuff', 'bison']
    # print([x for x in targs if legal(x, 'learn', [0,2,0,2,0]) and sum(1 for c in 'vfbpmx' if c in x) > 1])
    print([x for x in targs if legal(x, 'learn', list(map(int, '00110'))) and sum(1 for c in 'hpwmcfy' if c in x) > 2])

else:

    for targ in targs:
        if 1 or re.fullmatch('.i.er', targ):
            print(evaluate(targ), targ)
