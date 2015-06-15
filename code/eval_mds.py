
import numpy as np

#import matplotlib
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.font_manager import FontProperties


from sklearn import manifold
from sklearn.metrics import euclidean_distances
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D

import sys

def load_matrix(filepath):
  matrix = []
  for line in open(filepath, 'r'):
    new_array = [float(i) for i in line.split(' ') if i != '\n']
    matrix.append(new_array)

  return matrix


if (len(sys.argv) != 4):
  print 'Erorr parsing parameters. Usage: python eval_mds.py <mode> <input_matrix> <eval_mds_pos_output_file>'
  exit()
## mode is either load or full


MODE = sys.argv[1]
INPUT_MATRIX = sys.argv[2]
OUT_FILE = sys.argv[3]

if(MODE == "full"):
  dist_matrix = np.array(load_matrix(INPUT_MATRIX))

  mds = manifold.MDS(n_components=3, max_iter=3000, eps=1e-9,
                   dissimilarity="precomputed", n_jobs=1)
  pos = mds.fit(dist_matrix).embedding_
  np.savetxt(OUT_FILE, pos, fmt='%.9f')

else:
  pos = np.array(load_matrix(OUT_FILE))

print "pos:",pos

fig = plt.figure(1, figsize=(7, 8))
ax = fig.add_subplot(111, projection='3d')

# b: blue
# g: green
# r: red
# c: cyan
# m: magenta


fontP = FontProperties()
fontP.set_size('large')

colours = ['b', 'g', 'r', 'c','m']
labels = ['ER', 'ER-DD', 'GEO', 'SF-BA', 'STICKY']

for i in range(5):
  indices = range(30*i, 30*(i+1))
  print indices
  #ax.scatter(pos[indices, 0], pos[indices, 1], pos[indices,2], c=colours[i], marker='o')

  ax.plot( pos[indices, 0], pos[indices, 1], pos[indices,2],'o', color=colours[i], label=labels[i], markersize=10)

fig.subplots_adjust(left=0.00, bottom=0.15, top=1.0, right=1.0)

plt.legend(loc='upper left', numpoints=1, ncol=3, bbox_to_anchor=(0, 0), prop = {'size':20})
plt.show()


