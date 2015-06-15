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


set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black

set y2tics

set x2tics textcolor ls 5
set y2tics textcolor ls 5


plot "''' + basename + r'''.data" using 1:(100*$2) w lines ls 6 title "change in Network Topology (offset by ''' + str(offset) + '''): 1962-2010", \
     "''' + basename + '''.data" using 1:3 w lines ls 5 title "change in Crude Oil Price: 1962-2010" axes x1y2


########## POSTSCRIPT PLOTS ###############

#set output "| ps2pdf -dEPSCrop - ''' + basename + '''2.pdf"
#set output "| epstopdf --outfile=''' + basename + '''2.pdf - "
set output "''' + basename + '''.eps"
set terminal postscript enhanced color
set size 1.0,0.8

plot [:][:]"''' + basename + r'''.data" using 1:(100*$2) w lines ls 6 title "change in Network Topology (offset by ''' + str(offset) + '''): 1962-2010", \
     "''' + basename + '''.data" using 1:3 w lines ls 5 title "change in Crude Oil Price: 1962-2010" axes x1y2

syscall=sprintf("epstopdf --outfile=''' + basename + '''2.pdf ''' + basename + '''.eps")
system syscall
'''

  return text

###############################
####### End of functions ######
###############################





if (len(sys.argv) != 6):
  print 'Erorr parsing parameters. Usage: python dist_heatmaps.py <input_folder> <basename> <start_year> <end_year> <out_file>'
  exit()

INPUT_FOLDER=sys.argv[1]
BASENAME=sys.argv[2]
START_YEAR=int(sys.argv[3])
END_YEAR=int(sys.argv[4])
OUTPUT_FILE=sys.argv[5]

NR_GRAPHLETS=29

orig_matrix = np.zeros((END_YEAR - START_YEAR, NR_GRAPHLETS, NR_GRAPHLETS))
for year_nr in range(START_YEAR, END_YEAR):
  #print "year=", year_nr
  orig_matrix[year_nr-END_YEAR] = load_matrix( INPUT_FOLDER + "/" + BASENAME + str(year_nr) + ".data")
  #print orig_matrix[year_nr - END_YEAR]

yearly_change=np.zeros(END_YEAR-START_YEAR-1)
for i in range(END_YEAR-START_YEAR-1):
  yearly_change[i] = compute_distance(orig_matrix[i], orig_matrix[i+1]);

OIL_FILE='final_results/crudeoilprices_noslide.csv'

years = []
prices = []
with open(OIL_FILE) as f:
  for line in f:
    words = line.split(",")
    years += [int(words[0])]
    prices += [float(words[1][:-1])]

change_oil = []

for i in range(len(prices)-1):
  change_oil += [abs(prices[i+1] - prices[i])]


#print yearly_change
#print change_oil

#corr, p_value = scipy.stats.spearmanr(yearly_change, change_oil)

#print "#Spearman's rank coefficient: corr:",corr,"   p_value:", p_value
#with open(INPUT_FOLDER + "/" + OUTPUT_FILE + ".data", "w") as f:
#  for i in range(len(yearly_change)):
#    f.write(str(START_YEAR + i + 1) + " " + str(yearly_change[i]) + " " + str(change_oil[i]) + "\n")


#only been aligned, not actually offset
#change at 1993 is computed as (Price_{1993} - Price_{1992})
change_gcv_slided = zip([y+1 for y in years], yearly_change)
change_oil_slided = zip([y+1 for y in years], change_oil)

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

with open(INPUT_FOLDER + "/" + OUTPUT_FILE, "w") as f:
  for i in range(len(change_gcv_offset_align)):
    f.write(str(change_oil_offset_align[i][0]) + " " + str(change_gcv_offset_align[i][1]) + " " + str(change_oil_offset_align[i][1]) + "\n")


basename = INPUT_FOLDER + "/" + OUTPUT_FILE.split(".")[0]

start_year = change_oil_offset_align[0][0]
print "#start year",start_year
print genPlot(basename, start_year, best_offset)

