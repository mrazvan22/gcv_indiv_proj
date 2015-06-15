set output "metabolic_spreads_rnd.png"
set terminal png size 1200,900
#set output "metabolic_spreads_rnd.ps"
#set terminal postscript

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1.5   # --- red
set style line 3 lc rgb '#FF00FF' lt 1 lw 3 pt 7 ps 1.5   # --- purple
set style line 4 lc rgb '#194719' lt 1 lw 3 pt 7 ps 1.5   # --- green
set style line 5 lc rgb '#993300' lt 1 lw 3 pt 7 ps 1.5   # --- brown
set style line 6 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1     # --- black

plot "hsa_metabolic_network_spreads.data" using 1:2:3 with yerrorbars ls 6 notitle, '' using 1:2 w lines ls 1 title "avg hsa meta - er - 30 trials", \
     "hsa_metabolic_network_spreads.data" using 1:4:5 with yerrorbars ls 6 notitle, '' using 1:4 w lines ls 2 title "avg hsa meta - er-dd - 30 trials", \
     "hsa_metabolic_network_spreads.data" using 1:6:7 with yerrorbars ls 6 notitle, '' using 1:6 w lines ls 3 title "avg hsa meta - geo - 30 trials", \
     "hsa_metabolic_network_spreads.data" using 1:8:9 with yerrorbars ls 6 notitle, '' using 1:8 w lines ls 4 title "avg hsa meta - sf - 30 trials", \
     "hsa_metabolic_network_spreads.data" using 1:10:11 with yerrorbars ls 6 notitle, '' using 1:10 w lines ls 5 title "avg hsa meta - sticky - 30 trials"
