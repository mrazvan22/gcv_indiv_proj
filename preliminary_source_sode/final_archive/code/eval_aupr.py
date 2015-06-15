
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


def genPlot(OUTPUT_BASE):
  text = r'''

########## PNG PLOTS ###############

set output "''' + OUTPUT_BASE + r'''.png"
set terminal png size 1200,500

set xlabel "Recall" font "Times-Roman, 20"
set ylabel "Precision" font "Times-Roman, 20"


set key font "Times-Roman, 20"
set key spacing 1.5

#set key at 100,100

#set x2tics ""
set xtics nomirror

set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

set lmargin 9
set rmargin 9

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black
set style line 7 lc rgb '#000000' lt 1 lw 3 pt 7 ps 2.0     # --- black

plot "''' + OUTPUT_FILE +  r'''" using 1:2 w lines ls 1 title "GCV"


########## POSTSCRIPT PLOTS ###############

set output "''' + OUTPUT_BASE + r'''.eps"
set terminal postscript enhanced color
set size 1.0,0.7

plot "''' + OUTPUT_FILE +  r'''" using 1:2 w lines ls 1 title "GCV"

syscall=sprintf("epstopdf --outfile=''' + OUTPUT_BASE + '''2.pdf ''' + OUTPUT_BASE + '''.eps")
system syscall


'''
  return text



if (len(sys.argv) != 3):
  print 'Erorr parsing parameters. Usage: python eval_aupr.py <dist_matrix> <precision_rec_out_file>'
  exit()
## mode is either load or full


INPUT_MATRIX = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

dist_matrix = load_matrix(INPUT_MATRIX)

CLASSES = [0] * 30 + [1] * 30 + [2] * 30 + [3] * 30 + [4] * 30

minX = dist_matrix[0][1]
maxX = dist_matrix[0][5]
for i in range(len(dist_matrix)):
  for j in range(i):
    if minX > dist_matrix[i][j]:
      minX = dist_matrix[i][j]
    if maxX < dist_matrix[i][j]:
      maxX = dist_matrix[i][j]

print "#minX=%f,   maxX=%f" % (minX, maxX)


indices=drange(minX, maxX, (maxX - minX)/200)

#print indices

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

  print "EPS=%.5f  TP=%d  FP=%d FN=%d  TN=%d PREC=%f RECALL=%f" % (eps, TP, FP, FN, TN, prec, rec)

  i += 1

  if (FN == 0):
    break


#print pr_dict

recalls = pr_dict.keys()
recalls.sort()

#print recalls

gcv_prec_rec = [(float(x), pr_dict[x]) for x in recalls] # containes tuples (recall, precision)
#print gcv_prec_rec

#print np.array(gcv_prec_rec)

np.savetxt(OUTPUT_FILE, gcv_prec_rec, "%.3f")

IMAGE_OUT = OUTPUT_FILE.split(".")[0]
print genPlot(IMAGE_OUT)

aupr = 0
for k in range(1,len(gcv_prec_rec)):
  aupr += 0.5 * float((gcv_prec_rec[k][0]-gcv_prec_rec[k-1][0])*(gcv_prec_rec[k][1]+gcv_prec_rec[k-1][1]))

print "# AUPR GCV %f" % aupr
