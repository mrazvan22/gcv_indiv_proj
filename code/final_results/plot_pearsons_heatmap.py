#! /usr/bin/env python
# usage python plot_pearsons_heatmap.py <network_name>

import sys

def genText(net_name, perm):
  text = r'''
set output "''' + net_name + '/heatmap_' + net_name + '''.png"
set terminal png size 1200,900

set x2label "Graphlets" font "Times-Roman, 20"
set ylabel "Graphlets" font "Times-Roman, 20"


set tic scale 0

set palette rgbformulae 22,13,10

set cbrange [0:1]
#unset cbtics

set x2tics font "Times-Roman, 20"
set ytics font "Times-Roman, 20"

# place x axis on top
set xtics format ""
set x2tics offset -3,0
set ytics offset 0,1.3
set x2tics 1,1,30
set ytics 1,1,30

set xrange [-0.5:28.5]
set yrange [28.5:-0.5]

set view map

set title "''' + net_name + '''" font "Times-Roman, 20"

plot "''' + net_name + '/pearsons_' + net_name + '''.data" matrix with image

set output "''' + net_name + '/heatmap_normalized_' + net_name + '''.png"
set terminal png size 1200,900
plot "''' + net_name + '/pearsons_normalized_' + net_name + '''.data" matrix with image

set output "''' + net_name + '/heatmap_' + net_name + '''.ps"
set terminal postscript
plot "''' + net_name + '/pearsons_' + net_name + '''.data" matrix with image

set output "''' + net_name + '/heatmap_normalized_' + net_name + '''.ps"
set terminal postscript
plot "''' + net_name + '/pearsons_normalized_' + net_name + '''.data" matrix with image


'''

  return text

if (len(sys.argv) != 2):
  print 'Erorr parsing parameters. Usage: python plot_pearsons_heatmap.py <network_name>'
  exit()

net_name = sys.argv[1];

print genText(net_name, range(29))
