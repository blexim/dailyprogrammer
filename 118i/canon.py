#!/usr/bin/python

import re
import sys

r = re.compile(r'(\d\d?).(\d\d) (\d\d?).(\d\d) (\d\d?).(\d\d) (\d\d?).(\d\d)')
parameters = sys.stdin.readline()
m = r.match(parameters)

N = int(m.group(1))*100 + int(m.group(2))
A = int(m.group(3))*100 + int(m.group(4))
B = int(m.group(5))*100 + int(m.group(6))
C = int(m.group(7))*100 + int(m.group(8))

# Time to fire the first shot is however long it takes to get both shell
# and propellant to the canon, i.e. max(A, B)
first_shot = max(A, B) + C

# Time to fire each subsequent shot is however long it takes to get a
# shell and propellant to the canon and reload it.  However all these can
# be done in parallel, so this is just max(A, B, C)
cycle_time = max(A, B, C)

shots = 1 + (N-first_shot) / cycle_time

print shots

shots = 0
t = first_shot

while t <= N:
  print t
  shots += 1
  t += cycle_time

print shots
