set output "spreads_rnd_test.png"
set terminal png

set style line 1 lc rgb '#0060ad' lt 1 lw 3 pt 7 ps 1.5   # --- blue
set style line 2 lc rgb '#dd181f' lt 1 lw 3 pt 7 ps 1   # --- red
set style line 3 lc rgb '#000000' lt 1 lw 3 pt 7 ps 1   # --- black

plot "input_spreads.txt" using 1:2:3 with yerrorbars ls 3 notitle, '' using 1:2 w lines ls 1 title "hsa meta - sf - avg over 30 trials", \
     "input_spreads.txt" using 1:4:5 with yerrorbars ls 3 notitle, '' using 1:4 w lines ls 2 title "hsa meta - sticky - avg over 30 trials"
