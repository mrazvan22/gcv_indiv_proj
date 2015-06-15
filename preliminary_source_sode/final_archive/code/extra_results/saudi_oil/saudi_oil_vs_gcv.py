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

# generated the change in time plot (containing the line) . if first entry is change 1962/1963 then start year is 1963
def genPlot(basename, start_year, offset):
  text = r'''

########## PNG PLOTS ###############

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1.5     # --- black

set style line 7 lc rgb '#993300' lt 1 lw 3 pt 2 ps 1.5   # --- brown
set style line 8 lc rgb '#000000' lt 1 lw 3 pt 3 ps 1.5     # --- black



set output "''' + basename + '''.png"
set terminal png size 1200,500

set xlabel "Years (GCV)" font "TImes-Roman, 20"
set x2label "Years (Oil)" font "TImes-Roman, 20" textcolor ls 5
set ylabel "Network Topology change" font "Times-Roman, 20"
set y2label "Oil price change ($)" font "Times-Roman, 20" textcolor ls 5


set lmargin 9
set tmargin 7


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
      text += '"' + str(start_year - 1 + i - offset) + "/" + str(start_year + i - offset) + '" ' + str(start_year + i)

    text += ') rotate by 315\n'

  for axis in ['x2']:
    text += 'set ' + axis + 'tics ('
    for i in [3*x for x in range(20)]:
      if i!=0:
        text += ','
      text += '"' + str(start_year - 1 + i) + "/" + str(start_year + i) + '" ' + str(start_year + i)

    text += ') rotate by 45\n'




  text += '''


set y2tics

#set border 34 ls 5

set x2tics textcolor ls 5
set y2tics textcolor ls 5

plot "''' + basename + r'''.data" using 1:(100*$2) w lines ls 8 title "change in Saudi GCV (offset by ''' + str(offset) + '''): 1962-2009", \
     "''' + basename + '''.data" using 1:3 w lines ls 7 title "change in Crude Oil Price: 1962-2009" axes x1y2


########## POSTSCRIPT PLOTS ###############

set output "''' + basename + '''.eps"
set terminal postscript enhanced color
set size 1.0,0.7


plot "''' + basename + r'''.data" using 1:(100*$2) w lines ls 8 title "change in Saudi GCV (offset by ''' + str(offset) + '''): 1962-2009", \
     "''' + basename + '''.data" using 1:3 w lines ls 7 title "change in Crude Oil Price: 1962-2009" axes x1y2

syscall=sprintf("epstopdf --outfile=''' + basename + '''2.pdf ''' + basename + '''.eps"    )
system syscall

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
#change at 1993 is computed as (Price_{1993} - Price_{1992})

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


#only been aligned, not actually offset
change_gcv_slided = [(y,c) for (y,c) in change_gcv if y in [oil_year for (oil_year,x) in change_oil]]
change_oil_slided = [(y,c) for (y,c) in change_oil if y in [gcv_year for (gcv_year,x) in change_gcv]]

#print "------------------"
#print change_gcv_slided
#print change_oil_slided

N = len(change_gcv_slided)

best_offset = 0
min_pvalue = 1000

for offset in [-2,-1,0,1,2]:
  change_gcv_offset = [(year + offset, c) for (year,c) in change_gcv_slided]
  change_gcv_offset_align = [(y,c) for (y,c) in change_gcv_offset if y in [oil_year for (oil_year,x) in change_oil_slided]]
  change_oil_offset_align = [(y,c) for (y,c) in change_oil_slided if y in [gcv_year for (gcv_year,x) in change_gcv_offset_align]]

  corr, p_value = scipy.stats.spearmanr([y for (x,y) in change_gcv_offset_align], [y for (x,y) in change_oil_offset_align])
  print "#gcv offset:", offset, "  Spearman's rank coefficient: corr:",corr,"   p_value:", p_value

  if(min_pvalue > p_value):
    min_pvalue = p_value
    best_offset = offset

print "#best_offset = ", best_offset

change_gcv_offset = [(year + best_offset, c) for (year,c) in change_gcv_slided]
change_gcv_offset_align = [(y,c) for (y,c) in change_gcv_offset if y in [oil_year for (oil_year,x) in change_oil_slided]]
change_oil_offset_align = [(y,c) for (y,c) in change_oil_slided if y in [gcv_year for (gcv_year,x) in change_gcv_offset_align]]

#print change_gcv_offset_align
#print change_oil_offset_align

with open(OUTPUT_FILE, "w") as f:
  for i in range(len(change_gcv_offset_align)):
    f.write(str(change_oil_offset_align[i][0]) + " " + str(change_gcv_offset_align[i][1]) + " " + str(change_oil_offset_align[i][1]) + "\n")

basename = OUTPUT_FILE.split(".")[0]
print genPlot(basename, change_oil_offset_align[0][0], best_offset)
