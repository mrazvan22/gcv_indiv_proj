#! /usr/bin/env python
# usage python plot_pearsons_heatmap.py <network_name>

import sys


rnd_nets = ['ER', 'ER-DD', 'GEO', 'SF', 'STICKY']

def plot_data(net, ext, rnd_types_indices):

  text = ''
  for i in rnd_types_indices:

    if(i > 0):
      text += '     '

    c = 2*(i+1)
    text += '''"''' + net + "/" + net + r'''_spreads.data" using 1:'''
    text += str(c) + ":" + str(c +1) + ''' with yerrorbars ls 6 notitle, '' using 1:'''
    text += str(c) + ''' w lines ls ''' + str(i+1) + ''' title "'''
    text += rnd_nets[i] + r'''", \
'''

  text += '     '

  text += '''"''' + net + "/" + net + r'''_spreads.data" using 1:12 w lines ls 7 title "REAL NETWORK"
'''

  return text

def plot_individual(net, ext, rnd_types_indices):

  for i in range(5):
    text += '''

set output "''' + net + "/avg_egdvs_rnd_spreads_figures/spreads_" + rnd_nets[i] + "_" + net + r'''_rnd.''' + ext + r'''"

'''
    c = 2*(i+1)
    text += '''plot [:][0:] "''' + net + "/" + net + r'''_spreads.data" using 1:'''
    text += str(c) + ":" + str(c +1) + ''' with yerrorbars ls 6 notitle, '' using 1:'''
    text += str(c) + ''' w lines ls ''' + str(i+1) + ''' title "'''
    text += rnd_nets[i] + r'''", \
'''
    text += '     '

    text += '''"''' + net + "/" + net + r'''_spreads.data" using 1:12 w lines ls 7 title "REAL NETWORK"
'''



  return text



if (len(sys.argv) != 2):
  print 'Erorr parsing parameters. Usage: python plot_pearsons_heatmap.py <network_name>'
  exit()

net = sys.argv[1];

fig1_indices = [0,1,2]
fig2_indices = [3,4]

suffix1 = "".join([str(x) for x in fig1_indices])
suffix2 = "".join([str(x) for x in fig2_indices])


text = r'''

########## PNG PLOTS ###############

set output "''' + net + "/avg_egdvs_rnd_spreads_figures/spreads_all_" + suffix1 + r'''.png"
set terminal png size 1200,500

set xlabel "Graphlets" font "Times-Roman, 20"
set ylabel "Frequency" font "Times-Roman, 20"

#set logscale y


set key font "Times-Roman, 20"
set key spacing 1.5

#set key at 100,100

#set x2tics ""
set xtics nomirror

set lmargin 9
set rmargin 9

'''

for axis in ['x']:
  text += 'set ' + axis + 'tics ('
  for i in range(29):
    if i!=0:
      text += ','
    text += '"' + str(i+1) + '" ' + str(i)

  text += ')\n'

text += '''

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black
set style line 7 lc rgb '#000000' lt 1 lw 3 pt 7 ps 2.0     # --- black

#stats [1:2] "''' + net + "/" + net + r'''_spreads.data"

'''

OUTPUT_BASE1 = net + "/avg_egdvs_rnd_spreads_figures/spreads_" + suffix1 + r'''_rnd'''
OUTPUT_BASE2 = net + "/avg_egdvs_rnd_spreads_figures/spreads_" + suffix2 + r'''_rnd'''

text += "plot [:][0:] " + plot_data(net, "png", [0,1,2,3,4]) + '''

'''
text += '''
########## POSTSCRIPT PLOTS ###############

set output "''' + OUTPUT_BASE1 + r'''.eps"
set terminal postscript enhanced color
set size 1.1,0.5


plot [:][0:] ''' + plot_data(net, "eps", fig1_indices) + r'''

syscall=sprintf("epstopdf --outfile=''' + OUTPUT_BASE1 + '''2.pdf ''' + OUTPUT_BASE1 + r'''.eps")
system syscall

set output "''' + OUTPUT_BASE2 + r'''.eps"

plot [:][0:] ''' + plot_data(net, "eps", fig2_indices) + r'''

syscall=sprintf("epstopdf --outfile=''' + OUTPUT_BASE2 + '''2.pdf ''' + OUTPUT_BASE2 + r'''.eps")
system syscall



'''

print text
