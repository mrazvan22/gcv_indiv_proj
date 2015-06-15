
import sys

import numpy as np
import random
import matplotlib.pyplot as plt
import math
from pylab import *

def get_dist(p,q):
  return math.pow(math.pow((p[0] - q[0]), 2) + math.pow((p[1] - q[1]),2), 0.5)

DIST = float(sys.argv[1])

NR_NODES = 200
OUTPUT = sys.argv[2]

fig = plt.figure(figsize=(5, 4))
# Create an Axes object.
ax1 = fig.add_subplot(1,1,1) # one row, one column, first plot

np.random.seed(seed=1)

x = np.random.uniform(0, 1, NR_NODES)
y = np.random.uniform(0, 1, NR_NODES)

# Plot non-ordered points
ax1.scatter(x, y, marker="o")


for i in range(NR_NODES):
  for j in range(NR_NODES):
    if (get_dist((x[i], y[i]), (x[j],y[j])) < DIST):
      ax1.plot([x[i], x[j]], [y[i], y[j]], color='b')

ax1.set_xlim([0, 1])
ax1.set_ylim([0, 1])

#plt.show()
savefig(OUTPUT, bbox_inches='tight')
