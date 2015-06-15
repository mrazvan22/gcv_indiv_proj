import os
import sys
import numpy as np

if(len(sys.argv) != 3):
  print "Usage: python gcv_dist.py <input_matrix_spreads.data> <output_file.dist>"
  exit()

INPUT=sys.argv[1]
OUTPUT=sys.argv[2]

rnd_nets = ['ER', 'ER_DD', 'GEO', 'SF', 'STICKY', 'REAL']

gcvs = []
with open(INPUT) as f:
  lines = f.readlines()[3:]
  for line in lines:
    words = line.split(" ")

    #strip the last '\n' character
    words[-1]=words[-1][:-1]
    #print words
    nrs = [float(x) for x in words]

    # keep only the averages
    gcvs += [[nrs[1], nrs[3], nrs[5], nrs[7], nrs[9], nrs[11]]]



gcvs = np.array(gcvs)

n = len(rnd_nets)
assert(n == len(gcvs[0]))

dist = np.zeros((n,n),float)

for i in range(n):
  for j in range(n):
    diff = gcvs[:,i] - gcvs[:,j]
    assert(len(diff) == 29)
    dist[i,j] = np.linalg.norm(diff, 1)


print dist

with open(OUTPUT, "w") as f:
  f.write("# Average GCV Distance matrix\n")
  f.write("#")
  for i in range(n):
    f.write("  " + rnd_nets[i])

  f.write("\n\n")

  for i in range(n):
    for j in range(n):
      f.write("%.3f " % dist[i,j])
    f.write("\n")
