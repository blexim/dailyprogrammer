#!/usr/bin/python

from __future__ import division

import sys
from sympy import *

l = Real(sys.argv[1])
r = Real(sys.argv[2])
s = 1.0 - l - r
n = int(sys.argv[3])

sys.setrecursionlimit(n+100)

memo_R = {}

# Probability that the rightmost position seen after k steps is x.
def R(x, k):
  if k == 0:
    if x == 0:
      return 1.0
    else:
      return 0.0

  if x < 0:
    return 0.0

  if (x, k) in memo_R:
    return memo_R[(x, k)]

  res = (R(x-1, k-1) * Pe(x-1, k-1) * r      +
         R(x,   k-1) * Pl(x,   k-1)          +
         R(x,   k-1) * Pe(x,   k-1) * (l+s))

  memo_R[(x, k)] = res

  if res > 1.0:
    print "x=%d, k=%d" % (x, k)
    print "R(x-1, k-1)=%f, Pe(x-1, k-1)=%f" % (R(x-1, k-1), Pe(x-1, k-1))
    print "R(x, k-1)=%f, Pl(x, k-1)=%f" % (R(x, k-1), (Pl(x, k-1)))
    print "R(x, k-1)=%f, Pe(x, k-1)=%f" % (R(x, k-1), Pe(x, k-1))
    print "res=%f" % res

  return res

memo_Pe = {}

# Probability that we are at position x after k steps.
def Pe(x, k):
  if k == 0:
    if x == 0:
      return 1.0
    else:
      return 0.0

  if x > k or x < -k:
    return 0.0

  if (x, k) in memo_Pe:
    return memo_Pe[(x, k)]

  res = (Pe(x-1, k-1) * r +
         Pe(x,   k-1) * s +
         Pe(x+1, k-1) * l)

  memo_Pe[(x, k)] = res

  #print "Pe(%d, %d)=%f" % (x, k, res)

  return res

memo_Pl = {}

# Probability that our position is less than x after k steps.
def Pl(x, k):
  if k == 0:
    if x > 0:
      return 1.0
    else:
      return 0.0

  if (x, k) in memo_Pl:
    return memo_Pl[(x, k)]

  res = (Pl(x-1, k-1) +
         Pe(x-1, k-1) * (l+s) +
         Pe(x,   k-1) * l)

  memo_Pl[(x, k)] = res

  #print "Pl(%d, %d)=%f" % (x, k, res)

  return res

avg = 0

for x in xrange(n+1):
  avg += x*R(x, n)

  print "%d, %f, %f" % (x, R(x, n), avg)

  x += 1

print avg
