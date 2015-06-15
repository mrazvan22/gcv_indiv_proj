
import numpy as np
import os
import sys

#nets = ["hsa_metabolic_network", "human_ppi", "trade_1970", "trade_1980", "trade_1990", "trade_2000", "trade_2010"]

net = sys.argv[1]

#NR_EXP = 10
NR_EXP = 5

NR_THREADS = int(sys.argv[2])

OUTPUT = "final_results/parallelisation_results/prob_size_%s_threads_%d.data" % (net, NR_THREADS)

THRESHOLDS = range(1,11)

avg_time_all = []
std_dev_all = []

for thr_nr in THRESHOLDS:

  time_samples = []

  print "THRESHOLD_VALUE: %d" % thr_nr
  for j in range(NR_EXP):

    date1 = float(os.popen('(date +%s.%N)').read())
    os.system("./e_gdv thresholded_nets_parallel_testing/%s-%d.gw test%s %d 1 > /dev/null" % (net, thr_nr, net, NR_THREADS))
    date2 = float(os.popen('(date +%s.%N)').read())

    time_samples += [date2 - date1]

  print time_samples

  avg_time = sum(time_samples)/ len(time_samples)
  std_dev = np.std(time_samples)

  print "avg:time %.3f  std_dev:%.6f" % (avg_time, std_dev)


  avg_time_all += [avg_time]
  std_dev_all += [std_dev]


with open(OUTPUT, "w") as f:
  f.write("# nr_threads (first col) and (avg time ,std dev)\n")

  for data_point_nr in range(len(avg_time_all)):
    f.write("%d %.3f %.5f\n" % (THRESHOLDS[data_point_nr], avg_time_all[data_point_nr], std_dev_all[data_point_nr]))
