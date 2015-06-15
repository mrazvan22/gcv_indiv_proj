#! /usr/bin/env python
# usage python plot_pearsons_heatmap.py <network_name>

import sys


net = sys.argv[1]

THREADS = [1,2,4,8,16,32,64]

IN_FILES=['prob_size_%s_threads_%d.data' % (net, threads) for (net, threads) in zip([net] * len(THREADS), THREADS)]


# no arguments need to be passed

OUTPUT="problem_size_" + net

text = r'''

########## PNG PLOTS ###############

set output "''' + OUTPUT + r'''.png"
set terminal png size 1200,500

set xlabel "Network size (%)" font "Times-Roman, 20"
set ylabel "Execution Time (s)" font "Times-Roman, 20"


set key font "Times-Roman, 20"
set key spacing 1.5

#set key outside;
set key left top;

#set key at 100,100

#set x2tics ""
set xtics nomirror
#set xtics (1,2,4,8,16,32,64)

set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"
set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"

#set log y 2


set lmargin 9
set rmargin 9

set style line 1 lc rgb '#0060ad' lt 1 lw 4 pt 1 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 4 pt 2 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 4 pt 3 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 4 pt 4 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 4 pt 5 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 4 pt 6 ps 1     # --- black
set style line 7 lc rgb '#FFA500' lt 1 lw 4 pt 6 ps 1     # --- black
set style line 8 lc rgb '#000000' lt 1 lw 4 pt 7 ps 2.0     # --- black

#plot "time.dat" using 1:2 w lines ls 1 title "Human PPI network", \
#     "time.dat" using 1:3 w lines ls 2 title "Human Metabolic network", \
#     "time.dat" using 1:4 w lines ls 3 title "2010 Trade network"


########## POSTSCRIPT PLOTS ###############

set output "''' + OUTPUT + r'''.eps"
set terminal postscript enhanced color
set size 1.0,0.7


plot [50:]'''

for i in range(len(THREADS)):
  text += '"' + IN_FILES[i] + r'''" using ($1 * 10):2 w linespoints ls ''' + str(i+1) + ''' title "''' + str(THREADS[i]) + r''' processes"'''
  if (i < len(THREADS) - 1):
    text += r''', \
      '''


text += r'''

syscall=sprintf("epstopdf --outfile=''' + OUTPUT + '''2.pdf ''' + OUTPUT + '''.eps")
system syscall

'''

print text
