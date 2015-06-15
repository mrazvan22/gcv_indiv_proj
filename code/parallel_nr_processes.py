
import numpy as np
import os

nets = ["hsa_metabolic_network.gw", "human_ppi.gw", "trade_2010_thresholded.gw"]
#nets = ["hsa_metabolic_network.gw", "trade_2010_thresholded.gw"]

#net_nr = sys.argv[1]

#NR_EXP = 10
NR_EXP = 5

#NR_THREADS = [1,2,4,8,16,32,64]
NR_THREADS = [8,16,32,64]
#NR_THREADS = [64,32]

OUTPUT = 'final_results/parallelisation_results/nr_processes.data'

avg_time_all = [0] * len(nets)
std_dev_all = [0] * len(nets)
for i in range(len(nets)):
  net = nets[i]
  avg_time_all[i] = []
  std_dev_all[i] = []

  print "NET:%s" % (nets[i])
  for threads in NR_THREADS:

    time_samples = []

    print "THREADS: %d" % threads
    for j in range(NR_EXP):

      date1 = float(os.popen('(date +%s.%N)').read())
      os.system("./e_gdv %s test %d 1 > /dev/null" % (net, threads))
      date2 = float(os.popen('(date +%s.%N)').read())

      time_samples += [date2 - date1]

    print time_samples

    avg_time = sum(time_samples)/ len(time_samples)
    std_dev = np.std(time_samples)

    print "avg:time %.3f  std_dev:%.6f" % (avg_time, std_dev)


    avg_time_all[i] += [avg_time]
    std_dev_all[i] += [std_dev]


with open(OUTPUT, "w") as f:
  f.write("# nr_threads (first col) and (avg time ,std dev) pairs for the networks in following order")
  for net in nets:
    f.write(" " + net)
  f.write("\n")

  for data_point_nr in range(len(avg_time_all[0])):
    f.write("%d" % NR_THREADS[data_point_nr])
    for net_nr in range(len(nets)):
      f.write(" %.3f %.5f" % (avg_time_all[net_nr][data_point_nr], std_dev_all[net_nr][data_point_nr]))
    f.write("\n")
