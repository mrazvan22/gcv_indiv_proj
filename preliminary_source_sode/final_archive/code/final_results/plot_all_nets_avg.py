#! /usr/bin/env python
# usage python plot_pearsons_heatmap.py <network_name>

import sys


nets = ['Human PPI', 'Human Metabolic network', '2010 WTN']

FILE='all_nets_average'


# no arguments need to be passed

OUTPUT="all_nets_average"

text = r'''

########## PNG PLOTS ###############

set output "''' + OUTPUT + r'''.png"
set terminal png size 1200,500

set xlabel "Frequency" font "Times-Roman, 20"
set ylabel "Graphlets" font "Times-Roman, 20"


set key font "Times-Roman, 20"
set key spacing 1.5

#set key at 100,100

#set x2tics ""
set xtics nomirror
'''

for axis in ['x']:
  text += 'set ' + axis + 'tics ('
  for i in range(29):
    if i!=0:
      text += ','
    text += '"' + str(i+1) + '" ' + str(i)

  text += ')\n'

text += r'''


#set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"

#set log x 2

set lmargin 9
set rmargin 9

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black
set style line 7 lc rgb '#000000' lt 1 lw 3 pt 7 ps 2.0     # --- black

plot "all_nets_average.data" using 1 w lines ls 1 title "Human PPI network", \
     "all_nets_average.data" using 2 w lines ls 2 title "Human Metabolic network", \
     "all_nets_average.data" using 4 w lines ls 4 title "2010 World Trade network"


########## POSTSCRIPT PLOTS ###############

set output "''' + OUTPUT + r'''.eps"
set terminal postscript enhanced color
set size 1.0,0.6

plot "all_nets_average.data" using 1 w lines ls 1 title "Human PPI network", \
     "all_nets_average.data" using 2 w lines ls 2 title "Human Metabolic network", \
     "all_nets_average.data" using 4 w lines ls 4 title "2010 World Trade network"



'''


text += r'''

syscall=sprintf("epstopdf --outfile=''' + OUTPUT + '''2.pdf ''' + OUTPUT + '''.eps")
system syscall

'''

print text
