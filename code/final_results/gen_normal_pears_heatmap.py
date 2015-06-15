import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.spatial.distance import *
import scipy.cluster.hierarchy as sch
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram

import sys
from plot_pearsons_heatmap_hclust import *


def load_matrix(filepath):
  matrix = []
  for line in open(filepath, 'r'):
    new_array = [float(i) for i in line.split(' ') if i != '\n']
    matrix.append(new_array)

  return matrix

def get_permutation(matrix):
  dist_matrix = squareform(pdist(matrix, metric='euclidean'))
  R  = dendrogram(linkage(dist_matrix, method='complete'))
  #print R['leaves']

  #plt.xlabel('points')
  #plt.ylabel('Height')
  #plt.suptitle('Cluster Dendrogram', fontweight='bold', fontsize=14);
  #plt.show()
  return R['leaves']


def rearange_matrix(matrix, permutation):
  #switch columns
  flipped_matrix = [[row[i] for i in permutation] for row in matrix]
  #switch rows
  flipped_matrix = [flipped_matrix[i] for i in permutation]

  #print flipped_matrix[0]
  return flipped_matrix


def write_matrix_to_file(matrix, outpath):
  outfile = file(outpath, 'w')
  np.savetxt(outfile, matrix, fmt='%-3.6f')

def generate_heatmap(matrix):
  return 0


if (len(sys.argv) != 2):
  print 'Erorr parsing parameters. Usage: python gen_normal_pears_heatmap.py <orig_matrix_path>'
  exit()

orig_matrix_path = sys.argv[1]
orig_matrix = load_matrix(orig_matrix_path)
#print orig_matrix

#perm = get_permutation(orig_matrix)
perm = range(30)
#print perm

#new_matrix = rearange_matrix(orig_matrix, perm)
#print rearange_matrix([[1,2,3],[4,5,6],[7,8,9]], [2,0,1])

#new_matrix_path = sys.argv[2];
#write_matrix_to_file(new_matrix, new_matrix_path)

print genText(orig_matrix_path, perm)

