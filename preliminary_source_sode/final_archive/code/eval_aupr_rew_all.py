
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

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

def drange(start, stop, step):
  r = start
  indices = []
  while r < stop:
    indices += [r]
    r += step

  return indices


def genPlot(OUTPUT_BASE, data_file):
  text = r'''

########## PNG PLOTS ###############

set output "''' + OUTPUT_BASE + r'''.png"
set terminal png size 1200,700

set ylabel "AUPR" font "Times-Roman, 20"


set key font "Times-Roman, 20"
set key spacing 1.5
set key outside
set key top

#set key at 100,100

#set x2tics ""
set xtics nomirror

set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

set lmargin 9
set rmargin 24
set bmargin 4

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#FFA500' lt 1 lw 3 pt 7 ps 1.5   # --- orange
set style line 7 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1.5   # --- black

plot '''

  for i in range(len(LABELS)):
    # dont'c include diameter
    if (i != 3):
      text += '''"''' + data_file +  r'''" using 1:''' + str(i+2) + r''' w lines ls ''' + str(i+1) + r''' title "''' + LABELS[i] + '''"'''
      if (i < len(LABELS) - 1):
        text += r''', \
     '''
  text += r'''

########## POSTSCRIPT PLOTS ###############

set output "''' + OUTPUT_BASE + r'''.eps"
set terminal postscript enhanced color
set size 1.0,0.7

plot '''

  for i in range(len(LABELS)):
    # dont'c include diameter
    if (i != 3):
      text += '''"''' + data_file +  r'''" using 1:''' + str(i+2) + r''' w lines ls ''' + str(i+1) + r''' title "''' + LABELS[i] + '''"'''
      if (i < len(LABELS) - 1):
        text += r''', \
     '''
  text += r'''

syscall=sprintf("epstopdf --outfile=''' + OUTPUT_BASE + '''2.pdf ''' + OUTPUT_BASE + '''.eps")
system syscall

'''

  return text


def print_matrix_core(matrix):
  indices = [30 * x for x in range(5)]

  for i in indices:
    for j in indices:
      print "%8.4f " % matrix[i][j],
      print "%8.4f .... " % matrix[i][j+1],
    print "\n"

    for j in indices:
      print "%8.4f " % matrix[i+1][j],
      print "%8.4f .... " % matrix[i+1][j+1],
    print "\n ..................................................................... \n"

def calc_aupr(dist_matrices):
  prec_rec_all = []
  aupr_all = []

  for k in range(len(dist_matrices)):
    dist_matrix = dist_matrices[k]

    minX = dist_matrix[0][1]
    maxX = dist_matrix[0][5]
    for i in range(len(dist_matrix)):
      for j in range(i):
        if minX > dist_matrix[i][j]:
          minX = dist_matrix[i][j]
        if maxX < dist_matrix[i][j]:
          maxX = dist_matrix[i][j]

    print "#", LABELS[k]
    print "#minX=%f,   maxX=%f" % (minX, maxX)


    indices=drange(minX, maxX, (maxX - minX)/200)

    #print indices
    #print "matrix core:"
    #print_matrix_core(dist_matrix)


    nr_rand_nets = len(dist_matrix)

    i = 0
    precision = []
    recall = []


    pr_dict = {}
    for eps in [float(x) for x in indices]:
      #print "eps:", eps

      TP = 0
      FP = 0
      FN = 0

      # only used for assertion
      TN = 0
      for x in range(nr_rand_nets):
        for y in range(x):
          if (dist_matrix[x][y] <= eps):
            if (CLASSES[x] == CLASSES[y]):
              TP += 1
            else:
              FP += 1
          else:
            if(CLASSES[x] == CLASSES[y]):
              FN += 1
            else:
              TN += 1


      assert (TP + FP + FN + TN == nr_rand_nets * (nr_rand_nets - 1)/2)


      prec = float(TP)/(TP+FP)
      rec = float(TP)/(TP+FN)

      pr_dict["%.3f" % rec] = prec

      #print "EPS=%.5f  TP=%d  FP=%d  FN=%d   PREC=%f   RECALL=%f" % (eps, TP, FP, FN, prec, rec)

      i += 1

      if (FN == 0):
        break


    #print pr_dict

    recalls = pr_dict.keys()
    recalls.sort()

    #print recalls

    prec_rec_vector = [(float(x), pr_dict[x]) for x in recalls] # containes tuples (recall, precision)
    #print np.array(prec_rec_vector)

    #print np.array(prec_rec_vector)
    prec_rec_all += [prec_rec_vector]


    aupr = 0
    for k in range(1,len(prec_rec_vector)):
      aupr += 0.5 * float((prec_rec_vector[k][0]-prec_rec_vector[k-1][0])*(prec_rec_vector[k][1]+prec_rec_vector[k-1][1]))

    aupr_all += [aupr]
    print "#aupr=", aupr


  #print prec_rec_all
  print "#aupr:",zip(IN_FILES, aupr_all)

  return aupr_all


def write_to_out_file(out_file, auprs, indices):
  assert(len(auprs) == len(indices))

  OUT_LABELS = ["".join(label.split(" ")) for label in LABELS]

  with open(out_file, "w") as f:
    f.write("#" + " ".join(OUT_LABELS) + "\n")
    for i in range(len(indices)):
      f.write("%d" % indices[i])
      for aupr in auprs[i]:
        f.write(" %.5f" % aupr)
      f.write("\n")

def calc_plotdata():
  mode = "rew"
  aupr_all_sigs = []
  for net_nr in range(10):
    dist_matrices = [load_matrix("%s/%s/%d_%s" % (SOURCE_FOLDER, mode, net_nr, f)) for f in IN_FILES]
    aupr_all_sigs += [calc_aupr(dist_matrices)]


  print "%s aupr_all_sigs:" % mode, aupr_all_sigs
  write_to_out_file(OUT_FILES[0], aupr_all_sigs, [10*x for x in range(10)])

  for i in range(1,3):
    aupr_all_sigs = []
    mode = modes[i]

    for net_nr in range(1,11):
      dist_matrices = [load_matrix("%s/%s/%d_%s" % (SOURCE_FOLDER, mode, net_nr, f)) for f in IN_FILES]
      aupr_all_sigs += [calc_aupr(dist_matrices)]

    print "%s aupr_all_sigs:" % mode, aupr_all_sigs

    write_to_out_file(OUT_FILES[i], aupr_all_sigs, [10*x for x in range(1,11)]) # [::-1] reverses the list .. see extended slice syntax


if (len(sys.argv) != 1):
  print 'Erorr parsing parameters. Usage: python eval_aupr_rew_all.py'
  exit()

GCV_IN = "gcv_dist.matrix"
DEG_IN = "deg_distrib_dist.matrix"
CLUST_IN = "clust_coeff_dist.matrix"
DIAM_IN = "diameter_dist.matrix"
SPECT_IN = "spectral_distrib_dist.matrix"
RGFD_IN = "rgfd_dist.matrix"
GCD73_IN = "gcd73_dist.matrix"

SOURCE_FOLDER = "final_results/trade_2010_thresholded/eval_results"

IN_FILES = [GCV_IN, DEG_IN, CLUST_IN, DIAM_IN, SPECT_IN, RGFD_IN, GCD73_IN]
LABELS = ["GCV", "Degree Dist.", "Clust. coeff.", "Diameter", "Spectral dist.", "RGFD", "GCD73"]

modes = ['rew', 'sampl', 'compl']
OUT_FILES = [("%s/%s_aupr_all_sigs.plotdata" % (SOURCE_FOLDER, mode)) for mode in modes]

IMAGES_OUT = ["%s/%s_aupr_all_sigs" % (SOURCE_FOLDER, mode)  for mode in modes]


CLASSES = [0] * 30 + [1] * 30 + [2] * 30 + [3] * 30 + [4] * 30

#calc_plotdata()

print r'''set xlabel "Rewiring Rate (%)" font "Times-Roman, 20"'''
print genPlot(IMAGES_OUT[0], OUT_FILES[0])

print "set xrange [100:10] reverse"
print r'''set xlabel "Nodes Sampled (%)" font "Times-Roman, 20"'''
print genPlot(IMAGES_OUT[1], OUT_FILES[1])

print r'''set xlabel "Edge Completeness (%)" font "Times-Roman, 20"'''
print genPlot(IMAGES_OUT[2], OUT_FILES[2])
