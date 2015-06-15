set output "hsa_metabolic_network/heatmap_hsa_metabolic_network.png"
set terminal png size 1200,900

set xlabel "Graphlets"
set ylabel "Graphlets"

set tic scale 0

set palette rgbformulae 22,13,10
set palette negative

set cbrange [-1:1]
#unset cbtics

set xrange [-0.5:28.5]
set yrange [-0.5:28.5]

set view map

splot 'hsa_metabolic_network/pearsons_hsa_metabolic_network.data' matrix with image title "hsa metabolic heatmap"

set output "hsa_metabolic_network/heatmap_hsa_metabolic_network.ps"
set terminal postscript

splot 'hsa_metabolic_network/pearsons_hsa_metabolic_network.data' matrix with image title "hsa metabolic heatmap"
