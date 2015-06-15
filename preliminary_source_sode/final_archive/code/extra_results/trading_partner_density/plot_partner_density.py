#import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
from scipy.spatial.distance import *
#import scipy.cluster.hierarchy as sch
import numpy as np
#from scipy.cluster.hierarchy import linkage, dendrogram
import scipy.stats

import sys
#from plot_pearsons_heatmap_hclust import *

# generated the change in time plot (containing the line) . if first entry is change 1962/1963 then start year is 1963
def genPlot(group):
  out_file = group[0]
  countries = group[1]
  text = r'''

#### plotting group:''' + out_file + r''' ########

########## PNG PLOTS ###############

set output "scores/''' + out_file + '''.png"
set terminal png size 1200,500

set xlabel "Years" font "Times-Roman, 20"
set ylabel "Trading partner sparsity score" font "Times-Roman, 20"

set lmargin 11
set rmargin 15

set key font "Times-Roman, 20"
set key spacing 1.5
set key outside
set key right top

set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

#set xtics center offset 0,-1

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#00F2FF' lt 1 lw 3 pt 7 ps 1     # --- cyan
set style line 7 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black

'''
  if (out_file == "eu_accession"):
    text += r'''set xrange [1995:2010]'''
  else:
    text += r'''set xrange [1962:2010]'''

  text += r'''

plot '''
  for i in range(len(countries)):
    country = countries[i]
    text += '''"scores/''' + country + r'''.scores" using 1:2 w lines ls ''' + str(i+1) + ''' title "''' + country + r'''"'''

    if (i < len(countries) - 1):
      text += r''', \
     '''

  text += '''

########## POSTSCRIPT PLOTS ###############

set output "scores/''' + out_file + '''.eps"
set terminal postscript enhanced color
set size 1.0,0.7


plot '''
  for i in range(len(countries)):
    country = countries[i]
    text += '''"scores/''' + country + r'''.scores" using 1:2 w lines ls ''' + str(i+1) + ''' title "''' + country + r'''"'''

    if (i < len(countries) - 1):
      text += r''', \
     '''

  text += '''


syscall=sprintf("epstopdf --outfile=scores/''' + out_file + '''2.pdf scores/''' + out_file + '''.eps"    )
system syscall


'''

  return text

###############################
####### End of functions ######
###############################


# no arguments need to be passed

# I took out BGR and CYP because these countries are too small and had no trading partners at times
g7 = ("g7", ["USA", "CHN", "DEU", "FRA", "GBR"])
eastern_europe = ("eastern_europe", ["RUS", "POL", "DDR", "ROM", "CZE", "HUN", "SUN"])
argentina_related = ("argentina_related", ["ARG", "GRC"])
eu_accession = ("eu_accession", ["CZE", "POL", "SVK", "HUN"])
opec = ("opec", ["IRN", "SAU", "ARE"])

all_groups = [g7, eastern_europe, argentina_related, eu_accession, opec]

for group in all_groups:
  print genPlot(group)
