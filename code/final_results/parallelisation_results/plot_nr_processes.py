#! /usr/bin/env python
# usage python plot_pearsons_heatmap.py <network_name>

import sys


nets = ['Human PPI', 'Human Metabolic network', '2010 Trade network']

FILE='nr_processes.data'


# no arguments need to be passed

OUTPUT="nr_processes"

text = r'''

########## PNG PLOTS ###############

set output "''' + OUTPUT + r'''.png"
set terminal png size 1200,500

set xlabel "Number of processes" font "Times-Roman, 20"
set ylabel "Speedup (%)" font "Times-Roman, 20"


set key font "Times-Roman, 20"
set key spacing 1.5

#set key at 100,100

#set x2tics ""
set xtics nomirror
set xtics (1,2,4,8,16,32,64)

set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"
set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"

set log x 2

set lmargin 9
set rmargin 9

set style line 1 lc rgb '#0060ad' lt 1 lw 4 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 4 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 4 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 4 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 4 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 4 pt 7 ps 1     # --- black
set style line 7 lc rgb '#000000' lt 1 lw 4 pt 7 ps 2.0     # --- black

#plot "time.dat" using 1:2 w lines ls 1 title "Human PPI network", \
#     "time.dat" using 1:3 w lines ls 2 title "Human Metabolic network", \
#     "time.dat" using 1:4 w lines ls 3 title "2010 Trade network"


########## POSTSCRIPT PLOTS ###############

set output "''' + OUTPUT + r'''.eps"
set terminal postscript enhanced color
set size 1.0,0.7

plot [:][-20:] "''' + FILE + r'''"  using 1:(816.4/$2 - 100) w linespoints ls 1 title "Human Metabolic network", \
     '' using 1:(9574.6/$4 - 100) w linespoints ls 2 title "Human PPI network" , \
     '' using 1:(885.9/$6 - 100) w linespoints ls 4 title "2010 World Trade network"


'''


text += r'''

syscall=sprintf("epstopdf --outfile=''' + OUTPUT + '''2.pdf ''' + OUTPUT + '''.eps")
system syscall

'''

print text
