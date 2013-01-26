#!/usr/bin/pypy

import random

f = open('words.txt')
ws = f.readlines()
ws = [w.strip() for w in ws]
f.close()

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

def mutate(cipher, temp):
  cs = list(cipher)

  for i in xrange(temp):
    if random.randint(0, 3) == 0:
      a = random.randint(0, 25)
      b = random.randint(0, 25)
      c = random.randint(0, 25)

      while a == b or a == c or b == c:
        a = random.randint(0, 25)
        b = random.randint(0, 25)
        c = random.randint(0, 25)

      c1 = cs[a]
      c2 = cs[b]
      c3 = cs[c]

      cs[a] = c2
      cs[b] = c3
      cs[c] = c1
    else:
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
    if i  == (10000/temp):
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

if __name__ == '__main__':
  import sys

  if len(sys.argv) > 1:
    search(sys.argv[1])
  else:
    search()
