#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from scipy.spatial.distance import *
#import scipy.cluster.hierarchy as sch
import numpy as np
#from scipy.cluster.hierarchy import linkage, dendrogram
import scipy.stats

import sys
#from plot_pearsons_heatmap_hclust import *


def load_matrix(filepath):
  matrix = []
  for line in open(filepath, 'r'):
    new_array = [float(i) for i in line.split(' ') if i != '\n']
    matrix.append(new_array)

  return matrix

def write_matrix_to_file(matrix, outpath):
  outfile = file(outpath, 'w')
  np.savetxt(outfile, matrix, fmt='%-3.6f')

# Calculates the pairwise Euclidean distance between each element
def compute_distance(matrix1, matrix2):
  vect_dist = []
  for i in range(len(matrix1)):
    vect_dist += [np.linalg.norm(np.array(matrix1[i]) - np.array(matrix2[i]))]

  return np.linalg.norm(np.array(vect_dist))



if (len(sys.argv) != 3):
  print 'Erorr parsing parameters. Usage: python eval_mds net_type dist_matrix_out'
  exit()


netType = int(sys.argv[1])
OUTPUT_FILE= sys.argv[2]

FOLDER = "model_nets_rand_generated";

NETWORKS = ["hsa_metabolic_network", "human_ppi", "trade_2010_thresholded"]

TYPES = ["er", "er_dd", "geo", "sf", "sticky"]

NR_RAND_NETS = 30
RAND_NET_TYPES = len(TYPES)
NR_THREADS = 2

CLASSES = [0] * 30 + [1] * 30 + [2] * 30 + [3] * 30 + [4] * 30
print CLASSES

DIST_MAT_LEN = NR_RAND_NETS * RAND_NET_TYPES;
dist_matrix = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);


i = 0
for randType1 in range(RAND_NET_TYPES):
  for randNetNr1 in range(1, NR_RAND_NETS+1):
    source1 = "%s/%s/models/%s/%s-%s-%d/pearsons_matrix.data" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1)
    matrix1 = load_matrix(source1)

    j = 0
    for randType2 in range(RAND_NET_TYPES):
      for randNetNr2 in range(1, NR_RAND_NETS+1):
        source2 = "%s/%s/models/%s/%s-%s-%d/pearsons_matrix.data" % ( FOLDER, NETWORKS[netType], TYPES[randType2], NETWORKS[netType], TYPES[randType2], randNetNr2)
        matrix2 = load_matrix(source2)

        #print "Reading files: %s \n %s" % (source1, source2)
        dist_matrix[i,j] = compute_distance(matrix1, matrix2)

        j += 1


    indices = [30 * x for x in range(5)]
    #print dist_matrix[0][indices]
    #print dist_matrix[i][:]

    print "progress %d out of 150" % i

    i += 1

assert(i == 150 and j == 150)

print indices
print dist_matrix[indices]



np.savetxt(OUTPUT_FILE, np.array(dist_matrix), fmt='%.4f')

