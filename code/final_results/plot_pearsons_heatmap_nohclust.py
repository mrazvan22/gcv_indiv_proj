import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.spatial.distance import *
import scipy.cluster.hierarchy as sch
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram

import sys
#from plot_pearsons_heatmap_hclust import *



def genText(data_in, perm, coeff_range):
  #print 'Network input file', data_in
  image_out = data_in.split('.')[0].split('/')
  image_out = '/'.join(image_out[:len(image_out)-1]) + '/heatmap_' + image_out[-1]
  text = r'''
set output "''' + image_out + '''.png"
set terminal png size 900,900

set x2label "Graphlets" font "Times-Roman, 23"
set ylabel "Graphlets" font "Times-Roman, 23"


set tic scale 0

set palette rgbformulae 22,13,10

set cbrange [''' + str(coeff_range[0]) +":" + str(coeff_range[1]) + ''']
#unset cbtics

set x2tics font "Times-Roman, 20"
set ytics font "Times-Roman, 20"

# place x axis on top
set xtics format ""

set lmargin 7
set rmargin 1
set tmargin 4


'''
  for axis in ['x2', 'y']:
    text += 'set ' + axis + 'tics ('
    for i in range(len(perm)):
      if i!=0:
        text += ','
      text += '"' + str(perm[i]+1) + '" ' + str(i)

    text += ')\n'


  #for i in range(len(perm)):
  #  text += 'set ytics (' + str(perm[i]) + ' ' + str(i) + ')\n'

  text += '''

show x2tics

set xrange [-0.5:28.5]
set yrange [28.5:-0.5]


set view map
#plot "''' + data_in + '''" matrix with image

#set terminal latex
set terminal postscript eps color 20
set size 1.2,1.4

set output "''' + image_out + '''.eps"
file = "''' + data_in + '''"
plot file matrix with image

syscall=sprintf("epstopdf --outfile=''' + image_out + '''2.pdf ''' + image_out + r'''.eps")
system syscall


'''

  return text



if (len(sys.argv) != 2):
  print 'Erorr parsing parameters. Usage: python plot_pearsons_heatmap_nohclust.py <orig_matrix_path>'
  exit()

orig_matrix = sys.argv[1]
#print orig_matrix

x_range = 0
y_range = 1

perm = range(30)
print genText(orig_matrix, perm, [x_range, y_range])

