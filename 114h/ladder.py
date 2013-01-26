#!/usr/bin/python

import sys
from z3 import *
import time

s = Solver()

f = open('words.txt')
ws = [w.strip() for w in f.readlines()]
f.close()

words = {}

WordSort = Datatype('Word')
for w in ws:
  WordSort.declare(w)

WordSort = WordSort.create()

def is_adjacent(w1, w2):
  same = 0

  for (c1, c2) in zip(w1, w2):
    if c1 == c2:
      same += 1

  return same == (len(w1) - 1)

adjacent = []

x = Const('x', WordSort)
y = Const('y', WordSort)

words = [WordSort.constructor(i)() for i in xrange(len(ws))]

adj_body = []

for i in xrange(len(ws)):
  for j in xrange(i+1, len(ws)):
    if is_adjacent(ws[i], ws[j]):
      adjacent += [(i, j), (j, i)]

      adj_body += [And(x == words[i], y == words[j]),
                   And(x == words[j], y == words[i])]

adj_expr = Or(adj_body)

adj_f = Function('adj', WordSort, WordSort, BoolSort())

s.add(ForAll([x, y], adj_f(x, y) == adj_expr))

def z_adj(w1, w2):
  return substitute(adj_expr, (x, w1), (y, w2))

def search(n):
  start = time.time()

  s.push()
  vs = [Const('v%d' % i, WordSort) for i in xrange(n)]

  for i in xrange(n-1):
    #s.add(z_adj(vs[i], vs[i+1]))
    s.add(adj_f(vs[i], vs[i+1]) == True)

  s.add(Distinct(vs))

  res = s.check()
  s.pop()
  end = time.time()

  elapsed = end-start

  print "%.02fs" % elapsed

  if res:
    m = s.model()

    for v in vs:
      print m.evaluate(v)
  
  return res

if __name__ == '__main__':
  import sys

  search(int(sys.argv[1]))
