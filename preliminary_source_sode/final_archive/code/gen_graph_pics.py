

from math import *
import random

radius = 2
NR_NODES = 15
for i in range(NR_NODES):
  angle = 2 * i * pi / NR_NODES

  (xPos,yPos) = (sin(angle), cos(angle))

  xPos *= radius
  yPos *= radius

  print "\t{(%.3f, %.3f)//%da}," % (xPos, yPos, i)


for p in [0, 0.1, 0.2]:
  print "\np = %f\n\n" % p

  for i in range(NR_NODES):
    for j in range(i):
      if (random.random() < p):
        print "    \path[hi, line width=1.0]  (%da)  -- (%da);" % (i,j)
