#!/usr/bin/python

import random

f = open('words.txt')
ws = f.readlines()
ws = [w.strip() for w in ws]
f.close()

def matches_and_swaps(w, cipher):
  for i in xrange(len(w) - 1):
    i1 = ord(w[i]) - ord('a')
    i2 = ord(w[i+1]) - ord('a')

    c1 = cipher[i1]
    c2 = cipher[i2]

    if c1 > c2:
      ret = []

      for i in xrange(len(w) - 1):
        for j in xrange(len(w)):
          i1 = ord(w[i]) - ord('a')
          i2 = ord(w[j]) - ord('a')
          c1 = cipher[i1]
          c2 = cipher[i2]

          if c1 > c2:
            ret.append((i1, i2))

      return ret

  return None

def matches(w, cipher):
  for i in xrange(len(w) - 1):
    i1 = ord(w[i]) - ord('a')
    i2 = ord(w[i+1]) - ord('a')

    if cipher[i1] > cipher[i2]:
      return False

  return True

def score(cipher):
  total = 0

  for w in ws:
    if matches(w, cipher):
      total += 1

  return total

def score_and_swaps(cipher, n):
  swaps = {}
  total = 0

  for w in ws:
    res = matches_and_swaps(w, cipher)

    if res is None:
      total += 1
    else:
      for s in res:
        if s in swaps:
          swaps[s] += 1
        else:
          swaps[s] = 1

  ret = []
  min_swaps = 0

  for (swap, k) in swaps.iteritems():
    if len(ret) < n:
      ret.append((k, swap))
      ret = sorted(ret)
      min_swaps = ret[0][0]
    else:
      if k > min_swaps:
        ret = ret[1:]
        ret.append((k, swap))
        ret = sorted(ret)
        min_swaps = ret[0][0]

  ret = [s for (k, s) in ret]
  return (total, ret)

def mutate(cipher, temp):
  cs = list(cipher)

  for i in xrange(temp):
    a = random.randint(0, 25)
    b = random.randint(0, 25)

    c = cs[a]
    cs[a] = cs[b]
    cs[b] = c

  return ''.join(cs)

def search(cipher='abcdefghijklmnopqrstuvwxyz'):
  temp = 25
  best = score(cipher)
  i = 0

  print "Score: %d, %s" % (best, cipher)

  while temp > 0:
    if i  == (1000/temp):
      temp -= 1
      i = 0
      print "Temp = %d" % temp

    i += 1

    guess = mutate(cipher, temp)
    s = score(guess)

    if s > best:
      i = 0
      cipher = guess
      best = s

      print "Score: %d, %s" % (best, cipher)

def do_swaps(cipher, swaps):
  cs = list(cipher)

  for (i1, i2) in swaps:
    c1 = cs[i1]
    c2 = cs[i2]

    if c1 > c2:
      cs[i1] = c2
      cs[i2] = c1

  return ''.join(cs)

def search2(cipher='abcdefghijklmnopqrstuvwxyz'):
  temp = 5
  (best, swaps) = score_and_swaps(cipher, temp)
  i = 0

  print "Score: %d, %s" % (best, cipher)

  while temp > 0:
    if i == 10000/(temp**2):
      temp -= 1
      i = 0
      print "Temp: %d" % temp

    i += 1

    guess = do_swaps(cipher, swaps)
    (val, swaps) = score_and_swaps(guess, temp)

    if val > best:
      print "Score: %d, %s" % (val, cipher)
      best = val
      cipher = guess
    else:
      guess = mutate(cipher, temp)
      (val, swaps2) = score_and_swaps(guess, temp)

      if val > best:
        print "Score: %d, %s" % (val, guess)
        best = val
        cipher = guess
        swaps = swaps2

if __name__ == '__main__':
  import sys

  if len(sys.argv) > 1:
    search(sys.argv[1])
  else:
    search()
