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

# generated the change in time plot (containing the line)
def genPlot(basename):
  text = r'''

########## PNG PLOTS ###############

set output "''' + basename + '''.png"
set terminal png size 1200,500

set xlabel "Years" font "TImes-Roman, 20"
set ylabel "Change in correlation matrix" font "TImes-Roman, 20"

set lmargin 9

set key font "Times-Roman, 20"
set key spacing 1.5

set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

#set xtics center offset 0,-1
'''

  for axis in ['x']:
    text += 'set ' + axis + 'tics ('
    for i in [3*x for x in range(20)]:
      if i!=0:
        text += ','
      text += '"' + str(1961 + i+1) + "/" + str(1962 + i+1) + '" ' + str(1962 + i)

    text += ') rotate by 315\n'

  text += '''


set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black

set y2tics

plot "''' + basename + r'''.data" using 1:(100*$2) w lines ls 6 title "change in GCV correlation over time: 1962-2010", \
     "''' + basename + '''.data" using 1:3 w lines ls 5 title "change in oil price over time: 1962-2010" axes x1y2


########## POSTSCRIPT PLOTS ###############

set output "''' + basename + '''.ps"
set terminal postscript

plot "''' + basename + r'''.data" using 1:(100*$2) w lines ls 6 title "change in GCV correlation over time: 1962-2010", \
     "''' + basename + '''.data" using 1:3 w lines ls 5 title "change in oil price over time: 1962-2010" axes x1y2

'''

  return text

###############################
####### End of functions ######
###############################


if (len(sys.argv) != 4):
  print 'Erorr parsing parameters. Usage: python saudi_oil_vs_gcv.py <gcv_file> <oil_file> <out_file.data>'
  exit()

GCV_FILE=sys.argv[1]
OIL_FILE=sys.argv[2]
OUTPUT_FILE=sys.argv[3]
#OIL_FILE='final_results/crudeoilprices_noslide.csv'

NR_GRAPHLETS=29


year_gcv = []
gcv_change = []
with open(GCV_FILE) as f:
  for line in f:
    words = line.split(" ")
    year = words[0].split(".")[0]

    #strip the \n
    words[-1]=words[-1][:-1]

    gcv = [float(x) for x in words[1:]]

    year_gcv += [(year, gcv)]


change_gcv = []
#1993 is computed as (Price_{1993} - Price_{1992})

for i in range(len(year_gcv)-1):
  #print "gcv i+1:",np.array(year_gcv[i+1][1])
  #print "gcv i:", np.array(year_gcv[i][1])

  change = np.linalg.norm([x-y for (x,y) in zip(year_gcv[i+1][1], year_gcv[i][1])])
  change_gcv += [(int(year_gcv[i+1][0]), change )]


year_price = []
with open(OIL_FILE) as f:
  for line in f:
    words = line.split(",")
    year = int(words[0])
    price = float(words[1][:-1])
    year_price += [(year,price)]

change_oil = []

for i in range(len(year_price)-1):
  change_oil += [(year_price[i+1][0], abs(year_price[i+1][1] - year_price[i][1]))]


#print change_gcv
#print change_oil


change_gcv_slided = [(y,c) for (y,c) in change_gcv if y in [oil_year for (oil_year,x) in change_oil]]
change_oil_slided = [(y,c) for (y,c) in change_oil if y in [gcv_year for (gcv_year,x) in change_gcv]]

#print "------------------"
#print change_gcv_slided
#print change_oil_slided

N = len(change_gcv_slided)

for offset in [-2,-1,0,1,2]:
  change_gcv_offset = [(year + offset, c) for (year,c) in change_gcv_slided]
  change_gcv_offset_align = [(y,c) for (y,c) in change_gcv_offset if y in [oil_year for (oil_year,x) in change_oil_slided]]
  change_oil_slided_align = [(y,c) for (y,c) in change_oil_slided if y in [gcv_year for (gcv_year,x) in change_gcv_offset_align]]

  corr, p_value = scipy.stats.spearmanr([y for (x,y) in change_gcv_offset_align], [y for (x,y) in change_oil_offset_align])
  print "#offset:", offset, "  Spearman's rank coefficient: corr:",corr,"   p_value:", p_value

with open(OUTPUT_FILE, "w") as f:
  for i in range(len(change_gcv_slided)):
    f.write(str(change_gcv_slided[i][0]) + " " + str(change_gcv_slided[i][1]) + " " + str(change_oil_slided[i][1]) + "\n")

basename = OUTPUT_FILE.split(".")[0]
print genPlot(basename)
