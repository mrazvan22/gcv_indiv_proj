

import sys
import numpy as np


if(len(sys.argv) != 3):
  print "Usage python calc_gdd.py <input.ndump2> <output>"


INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

gdvs = []
with open(INPUT_FILE) as f:
  for line in f:
    words = line.split(" ")

    # strip the \n
    words[-1] = words[-1][:-1]

    gdvs += [[int(x) for x in words[1:]]]




gdvs = np.array(gdvs)

NR_ORBITS = len(gdvs[0])

assert(NR_ORBITS == 73)

for orb in NR_ORBITS:
  degrees = gdvs[:,orb]
  values = sorted(set(degrees))
  deg_dist = [degrees.count(x) for x in values]
  print deg_dist

  TARGET_LEN = 30

  if(len(deg_dist) > TARGET_LEN):
    deg_dist = deg_dist[:TARGET_LEN]
  else:
    deg_dist = deg_dist + ([0] * (TARGET_LEN - len(deg_dist)))

  assert(len(deg_dist) == TARGET_LEN)


