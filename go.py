#!/usr/bin/env python3

import json
import random

lf = lambda x: [y for y in x if len(y) == 5 and '*' not in y]
words = lf(json.load(open('hello-wordl/src/dictionary.json')))
targs = lf(json.load(open('hello-wordl/src/targets.json')))
targs = targs[:targs.index('murky')+1]
print(len(targs))
print([x for x in targs if x[1:] == 'ound'])

goods = [x for x in words if len(set(x)) == 5 and not any(c in x for c in 'qjzxv')]

goode = [x for x in goods if 'e' in x]
goodf = [x for x in goods if 'e' not in x]

print(len(goods))
print(len(goode) * len(goodf)**2)

print(len([x for x in goods if 'e' in x and 'a' in x]) * len([x for x in goods if 'e' not in x and 'a' not in x])**2)
print(len([x for x in goods if 'e' in x and 'a' not in x]) * len([x for x in goods if 'e' not in x and 'a' in x]) * len([x for x in goods if 'e' not in x and 'a' not in x]))


from collections import Counter
print(''.join(x[0] for x in Counter(''.join(targs)).most_common(15)))
print(''.join(x[0] for x in Counter(''.join(targs)).most_common(20)))
print(''.join(x[0] for x in Counter(''.join(targs)).most_common(26)))
tt = targs[:]
chrs = ''
while len(chrs) < 15:
    chrs += Counter(c for c in ''.join(tt) if c not in chrs).most_common(1)[0][0]
    tt = [t for t in tt if len([c for c in t if c in chrs]) < 3]
print(chrs)

print([x for x in words if sum(1 for c in 'pgbfk' if c in x) >= 3])
print([x for x in words if sum(1 for c in 'pgbfkwv' if c in x) >= 3])
print([x for x in words if sum(1 for c in 'pgbfkwvxzjq' if c in x) >= 3])

# __import__('sys').exit()

# goods = [x for x in words if len(set(x)) == 5 and set(x) < set('earotlsincuydhm')]
goods = [x for x in words if len(set(x)) == 5 and set(x) < set('eartolsinchudpymgbfv')]


#me:   hm
#ihnn: pg

gr = lambda a,b: sum(x==y for x,y in zip(a,b))

# goods = sorted(goods, key=lambda x: -sum(gr(x,t) for t in targs))
# print('hi')

# for w1 in [x for x in goods if 'y' in x]:
#     for w2 in [x for x in goods if not any(c in x for c in w1)]:
#         for w3 in [x for x in goods if not any(c in x for c in w1+w2)]:
#             greens = sum(gr(w1,t)+gr(w2,t)+gr(w3,t) for t in targs)
#             if maxgr < greens:
#                 maxgr = greens
#                 print(greens, w1, w2, w3)

def color(w, t):
    ret = [1 if x==y else 0 for x,y in zip(w,t)]
    bank = [y for x,y in zip(w,t) if x!=y]
    for i,ch in enumerate(w):
        if not ret[i] and ch in bank:
            ret[i] = 2
            bank.remove(ch)
    return (((ret[0]*3+ret[1])*3+ret[2])*3+ret[3])*3+ret[4]

def width(w1, w2, w3, ts):
    colors = Counter([color(w1,t) + color(w2,t)*3**5 + color(w3,t)*3**10 for t in ts])
    return -sum(x*x for x in colors.values())
    return (-sum(x*x for x in colors.values()), -max(colors.values()))
    return -max(colors.values())

def width2(w1, w2, w3, ts):
    colors = Counter([color(w1,t) + color(w2,t)*3**5 + color(w3,t)*3**10 for t in ts])
    return -max(colors.values())

def width4(w1, w2, w3, w4, ts):
    colors = Counter([color(w1,t) + color(w2,t)*3**5 + color(w3,t)*3**10 + color(w4,t)*3**15 for t in ts])
    return -sum(x*x for x in colors.values())

def width42(w1, w2, w3, w4, ts):
    colors = Counter([color(w1,t) + color(w2,t)*3**5 + color(w3,t)*3**10 + color(w4,t)*3**15 for t in ts])
    return -max(colors.values())

def bads(w1, w2, w3, ts):
    print(w1,w2,w3)
    colors = {t: color(w1,t) + color(w2,t)*3**5 + color(w3,t)*3**10 for t in ts}
    counts = Counter(colors.values())
    print(Counter(counts.values()))
    print()
    pats = sorted([(v,k) for k,v in counts.items() if v > 3])
    for _,pat in pats:
        pat3=pat
        pat2 = ''
        for i in range(15):
            pat2 += str(pat%3)
            pat = pat//3
            if i % 5 == 4: pat2 += ' '
        print(' '.join(reversed(''.join(reversed(pat2)).split())).replace('0','.').replace('1','G').replace('2','y'))
        print([k for k,v in colors.items() if v == pat3])
        print()
    print()

# bads(*'shady crine moult'.split(), targs)
# bads(*'manly crude hoist'.split(), targs)
bads(*'doily crame shunt'.split(), targs)

# for trip in '''
# madly count shire
# randy hoise mulct
# soyle daunt chirm
# horsy clime daunt
# manly crude hoist
# dimly haunt corse
# shaly mount cried
# chary slide mount
# shily crate mound
# doily crame shunt
# shady moult crine
# aesir pouty cling
# alien short ducky
# siren octal dumpy
# train lucky moped
# aloes girth cundy
# aloes mirth cundy
# scale intro pudgy
# later coins pudgy
# '''.split('\n'):
#     if not trip:
#         print('###')
#         continue
#     w1,w2,w3 = trip.split()
#     a=width(w1,w2,w3,targs)
#     b=sum(gr(w1,t)+gr(w2,t)+gr(w3,t) for t in targs)
#     print(a+b,a,b,width2(w1,w2,w3,targs),trip)

for trip in '''
vughy escot brand flimp
nobly fraud vetch gimps
ledgy bumfs parvo nicht
trayf pling chubs moved
bandy roves fight clump
grypt bundh fomes clavi
mysid parve flung botch
yacht lengs bovid frump
gyves fonda richt plumb
pervy mound chaft glibs
fluyt dimps ganev broch
hynde scurf blimp gavot
bundy might focal pervs
ovary fight bends clump
gothy crave finds plumb
curvy flans pight demob
podgy bumfs navel crith
chevy undos blimp graft
fleys gramp bitch vodun
chevy trild fango bumps
nymph flubs cigar devot
vinyl fetch gramp budos
'''.split('\n'):
    if not trip:
        print('###')
        continue
    w1,w2,w3,w4 = trip.split()
    a=width4(w1,w2,w3,w4,targs)
    b=sum(gr(w1,t)+gr(w2,t)+gr(w3,t)+gr(w4,t) for t in targs)
    print(a+b,a,b,width42(w1,w2,w3,w4,targs),trip)

maxgr = ((-1000000,0),0)
maxgr = (-1000000, -1000000)
maxgr = -1000000

# maxgrs = set()
# w1,w2,w3 = 'shady','moult','crine'
# maxgrs.add((width(w1,w2,w3,targs), sum(gr(w1,t)+gr(w2,t)+gr(w3,t) for t in targs)))
# print(maxgrs)
# w1,w2,w3 = 'dimly','haunt','corse'
# maxgrs.add((width(w1,w2,w3,targs), sum(gr(w1,t)+gr(w2,t)+gr(w3,t) for t in targs)))
# print(maxgrs)

while 1:
    w1 = random.choice([x for x in goods if 'y' in x])
    # w1 = 'madly'
    w2 = random.choice([x for x in goods if not any(c in x for c in w1)])

    w3 = random.choice([x for x in goods if not any(c in x for c in w1+w2)] or [''])
    if not w3: continue

    w4 = random.choice([x for x in goods if not any(c in x for c in w1+w2+w3)] or [''])
    if not w4: continue

    # w1, w2, w3 = 'aesir', 'pouty', 'cling'
    # w1, w2, w3 = 'alien', 'short', 'ducky'
    # w1, w2, w3 = 'siren', 'octal', 'dumpy'
    # w1, w2, w3 = 'train', 'lucky', 'moped'
    # w1, w2, w3 = 'later', 'coins', 'pudgy' # gp instead of mh
    # w1, w2, w3 = 'aloes', 'girth', 'cundy' # c instead of m
    # w1, w2, w3 = 'madly', 'count', 'shire'

    print(w1,w2,w3,w4)
    # continue

    wwx = width4(w1,w2,w3,w4,targs)
    # greens = sum(gr(w1,t)+gr(w2,t)+gr(w3,t)+gr(w4,t) for t in targs)
    # ww = wwx+greens
    # ww = (wwx, greens)
    # ww = greens
    ww = wwx

    # if any(ww[0] > x[0] or ww[1] > x[1] for x in maxgrs):
    if maxgr < ww:
        # maxgrs.add(ww)
        # maxgrs = set(x for x in maxgrs if not any(y[0] > x[0] and y[1] > x[1] for y in maxgrs))
        # print(ww, w1, w2, w3)
        maxgr = ww
        # print(maxgr, wwx, greens, w1, w2, w3)
        print(maxgr, w1, w2, w3, w4)
    # greens = sum(gr(w1,t)+gr(w2,t)+gr(w3,t) for t in targs)
    # if maxgr < greens:
    #     maxgr = greens
    #     print(maxgr, w1, w2, w3)
