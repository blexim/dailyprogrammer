#!/usr/bin/pypy

import random
import copy

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
  to_shuffle = random.sample(range(0, len(cipher)), temp+1)
  shuffled = copy.copy(to_shuffle)

  while shuffled == to_shuffle:
    random.shuffle(shuffled)

  idxes = range(0, len(cipher))

  for i in xrange(len(shuffled)):
    j = shuffled[i]
    k = to_shuffle[i]
    cs[k] = cipher[j]

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

      if temp == 0:
        break

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
