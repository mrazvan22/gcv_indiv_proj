#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from scipy.spatial.distance import *
#import scipy.cluster.hierarchy as sch
import numpy as np
#from scipy.cluster.hierarchy import linkage, dendrogram
import scipy.stats
from math import log

import sys
#from plot_pearsons_heatmap_hclust import *

TARGET_DIST_LEN = 60

def parse_pears_gdv_matrix(filepath):
  matrix = []
  for line in open(filepath, 'r'):
    new_array = [float(i) for i in line.split(' ') if i != '\n']
    matrix.append(new_array)

  return matrix

def write_matrix_to_file(matrix, outpath):
  outfile = file(outpath, 'w')
  np.savetxt(outfile, matrix, fmt='%-3.6f')

# Calculates the pairwise Euclidean distance between each element
def cmp_dist_matrices(matrix1, matrix2):
  vect_dist = []
  for i in range(len(matrix1)):
    vect_dist += [np.linalg.norm(np.array(matrix1[i]) - np.array(matrix2[i]))]

  return np.linalg.norm(np.array(vect_dist))


def cmp_dist_deg(deg_distrib1, deg_distrib2):
  distrib1 = np.array(deg_distrib1)
  distrib2 = np.array(deg_distrib2)
  #print "distrib1.shape:", distrib1.shape
  #(dimx,dimy) = distrib1.shape
  assert(len(distrib1.shape) == 1)
  return np.linalg.norm( distrib1 - distrib2)

def cmp_dist_spectral(spectral_distrib1, spectral_distrib2):
  return np.linalg.norm(np.array(spectral_distrib1) - np.array(spectral_distrib2))

def cmp_dist_egfd(gr_freq1, gr_freq2):
  return np.linalg.norm(np.array(gr_freq1) - np.array(gr_freq2), 1)


def parse_sigs(sigs_source):
  with open(sigs_source) as f:
    lines = f.readlines()

    #print "sigs source:", sigs_source
    deg_distrib = lines[1].split(" ")
    deg_distrib2 = [float(x) for x in deg_distrib[:-1]]
    #print "degree_dist:", deg_distrib2

    clust_coeff = float(lines[3].split(" ")[0])
    #print "clust_coeff", clust_coeff


    diam = float(lines[5].split(" ")[0])
    #print "diam", diam

    spectral_distrib = lines[7].split(" ")
    spectral_distrib2 = [float(x) for x in spectral_distrib[:-1]]
    #print "spectral distrib:", spectral_distrib2

    assert(len(deg_distrib2) == TARGET_DIST_LEN )
    assert(len(spectral_distrib2) == TARGET_DIST_LEN )

  return (deg_distrib2, clust_coeff, diam, spectral_distrib2)


def parse_gr_freq(gr_freq_source):
  gr_freq = []
  with open(gr_freq_source) as f:
    for line in f:
      words = line.split("\t")
      #print "gr_freq words:", words

      freq = float(words[-1][:-1])
      gr_freq += [freq]


  assert(len(gr_freq) == 29)

  #print "gr_freq:", gr_freq
  sumgr = sum(gr_freq)

  if(sumgr == 0):
    sumgr = 1

  for i in range(len(gr_freq)):
    if (gr_freq[i] == 0):
      gr_freq[i] = 1

  gr_freq = [ -log(x/sumgr) for x in gr_freq]
  #print "normalised gr_freq:", gr_freq

  return gr_freq

# mode = rew, sampl, compl
def compute_dist_matrices(mode, net_nr):
  deg_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);
  clust_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);
  diam_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);
  spectral_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);

  rgfd_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);
  gcd73_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);

  gcv_dist = np.zeros((DIST_MAT_LEN, DIST_MAT_LEN), float);


  i = 0

  NET_NAME = "graph_%s_%d" % (mode, net_nr)
  for randType1 in range(RAND_NET_TYPES):
    for randNetNr1 in range(1, NR_RAND_NETS+1):
      SOURCE_FOLDER1 = "%s/%s/models/%s/%s-%s-%d" % ( FOLDER, NETWORKS[netType], TYPES[randType1], NETWORKS[netType], TYPES[randType1], randNetNr1)
      sigs_source1 = "%s/%s.sigs" % ( SOURCE_FOLDER1, NET_NAME)
      (deg_distrib1, clust_coeff1, diam1, spectral_distrib1) = parse_sigs(sigs_source1)

      gr_freq_source1 = "%s/%s_gdv.gr_freq" % ( SOURCE_FOLDER1, NET_NAME)
      gr_freq1 = parse_gr_freq(gr_freq_source1)

      pears_gdv_source1 = "%s/%s_gdv.pears" % ( SOURCE_FOLDER1, NET_NAME)
      pears_matrix1 = parse_pears_gdv_matrix(pears_gdv_source1)

      pears_gcv_source1 = "%s/%s_gcv.pears" % ( SOURCE_FOLDER1, NET_NAME)
      gcv_matrix1 = parse_pears_gdv_matrix(pears_gcv_source1)

      j = 0
      for randType2 in range(RAND_NET_TYPES):
        for randNetNr2 in range(1, NR_RAND_NETS+1):
          SOURCE_FOLDER2 = "%s/%s/models/%s/%s-%s-%d" % ( FOLDER, NETWORKS[netType], TYPES[randType2], NETWORKS[netType], TYPES[randType2], randNetNr2)
          sigs_source2 = "%s/%s.sigs" % ( SOURCE_FOLDER2, NET_NAME)
          (deg_distrib2, clust_coeff2, diam2, spectral_distrib2) = parse_sigs(sigs_source2)

          gr_freq_source2 = "%s/%s_gdv.gr_freq" % ( SOURCE_FOLDER2, NET_NAME)
          gr_freq2 = parse_gr_freq(gr_freq_source2)

          pears_gdv_source2 = "%s/%s_gdv.pears" % ( SOURCE_FOLDER2, NET_NAME)
          pears_matrix2 = parse_pears_gdv_matrix(pears_gdv_source2)

          pears_gcv_source2 = "%s/%s_gcv.pears" % ( SOURCE_FOLDER2, NET_NAME)
          gcv_matrix2 = parse_pears_gdv_matrix(pears_gcv_source2)

          #print "Reading files: %s \n %s" % (source1, source2)

          deg_dist[i,j] = cmp_dist_deg(deg_distrib1, deg_distrib2)
          clust_dist[i,j] = abs(clust_coeff1 - clust_coeff2)
          diam_dist[i,j] = abs(diam1 - diam2)
          spectral_dist[i,j] = cmp_dist_spectral(spectral_distrib1, spectral_distrib2)
          rgfd_dist[i,j] = cmp_dist_egfd(gr_freq1, gr_freq2)
          gcd73_dist[i,j] = cmp_dist_matrices(pears_matrix1, pears_matrix2)
          gcv_dist[i,j] = cmp_dist_matrices(gcv_matrix1, gcv_matrix2)

          j += 1


      indices = [30 * x for x in range(5)]
      print "deg_dist     [0,30,60,90,120]", deg_dist[i][indices]
      print "clust_dist   [0,30,60,90,120]", clust_dist[i][indices]
      print "diam_dist    [0,30,60,90,120]", diam_dist[i][indices]
      print "spectral_dist[0,30,60,90,120]", spectral_dist[i][indices]
      print "rgfd_dist    [0,30,60,90,120]", rgfd_dist[i][indices]
      print "gcd73_dist   [0,30,60,90,120]", gcd73_dist[i][indices]
      print "gcv_dist     [0,30,60,90,120]", gcv_dist[i][indices]

      print "progress %d out of 150" % i

      i += 1

  assert(i == 150 and j == 150)

  prefix = "%s/%s/%d_" % (OUT_FOLDER, mode, net_nr)

  np.savetxt(prefix + DEG_OUT, np.array(deg_dist), fmt='%.4f')
  np.savetxt(prefix + CLUST_OUT, np.array(clust_dist), fmt='%.4f')
  np.savetxt(prefix + DIAM_OUT, np.array(diam_dist), fmt='%.4f')
  np.savetxt(prefix + SPECT_OUT, np.array(spectral_dist), fmt='%.4f')
  np.savetxt(prefix + RGFD_OUT, np.array(rgfd_dist), fmt='%.4f')
  np.savetxt(prefix + GCD73_OUT, np.array(gcd73_dist), fmt='%.4f')
  np.savetxt(prefix + GCV_OUT, np.array(gcv_dist), fmt='%.4f')




if (len(sys.argv) != 2):
  print 'Erorr parsing parameters. Usage: python eval_rew_cmp_dist.py net_type'
  exit()


netType = int(sys.argv[1])

assert(netType == 2)

FOLDER = "model_nets_rand_generated";


NETWORKS = ["hsa_metabolic_network", "human_ppi", "trade_2010_thresholded"]

TYPES = ["er", "er_dd", "geo", "sf", "sticky"]

NR_RAND_NETS = 30
RAND_NET_TYPES = len(TYPES)
NR_THREADS = 2

DIST_MAT_LEN = NR_RAND_NETS * RAND_NET_TYPES;

OUT_FOLDER = "final_results/trade_2010_thresholded/eval_results"

DEG_OUT = "deg_distrib_dist.matrix"
CLUST_OUT = "clust_coeff_dist.matrix"
DIAM_OUT = "diameter_dist.matrix"
SPECT_OUT = "spectral_distrib_dist.matrix"
RGFD_OUT = "rgfd_dist.matrix"
GCD73_OUT = "gcd73_dist.matrix"
GCV_OUT = "gcv_dist.matrix"


#for net_nr in range(10):
#  print "rew %d" % net_nr
#  compute_dist_matrices('rew', net_nr)

#for net_nr in range(1,11):
#  print "compl %d" % net_nr
#  compute_dist_matrices('compl', net_nr)

for net_nr in range(1,11):
  print "sampl %d" % net_nr
  compute_dist_matrices('sampl', net_nr)
