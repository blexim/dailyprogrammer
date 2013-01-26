#!/usr/bin/python

from z3 import *

f = open('words.txt')
ws = f.readlines()
ws = [w.strip() for w in ws]
f.close()

s = Solver()

bestscore = 0
cipher = 'abcdefghijklmnopqrstuvwxyz'

score = Int('score')
chars = Ints(' '.join(cipher))

print "Adding cipher constraints..."

for c in chars:
  s.add(c >= 0)
  s.add(c < 26)

s.add(Distinct(chars))

score_expr = 0

print "Adding word constraints..."

for w in ws:
  idxes = [chars[ord(c) - ord('a')] for c in w]
  conds = []

  for i in xrange(len(w) - 1):
    for j in xrange(i, len(w)):
      conds.append(idxes[i] <= idxes[j])

  cond = And(conds)
  w_score = If(cond, 1, 0)
  score_expr = w_score + score_expr

s.add(score == score_expr)

def solve(lim):
  s.push()

  print "Adding score constraint..."
  s.add(score > lim)

  print "Solving..."
  res = s.check()

  s.pop()

  if res:
    m = s.model()
    cipher = ''

    for c in chars:
      idx = ord('a') + m[c].as_long()
      cipher += chr(idx)

    score_val = m[score].as_long()

    return (score_val, cipher)

  return None

def search():
  lo = 0
  hi = len(ws)

  while lo < hi:
    mid = (lo + hi)/2

    res = solve(mid)

    if res is None:
      hi = mid
    else:
      (score, cipher) = res
      lo = score

      print "Score: %d, %s" % (score, cipher)

def search2():
  res = (0, '')

  while res is not None:
    (score, cipher) = res
    print "Score: %d, %s" % (score, cipher)
    res = solve(score)

if __name__ == '__main__':
  import sys

  if len(sys.argv) > 1:
    lim = int(sys.argv[1])
    print solve(lim)
  else:
    search2()
