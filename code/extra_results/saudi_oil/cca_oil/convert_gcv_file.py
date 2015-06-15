import sys

# converts the file with entries like 1979.ndump2:SAU 1022 23 23525 626 2325 into gcv_list.csv with entries like 1979_SAU,1022,23, ..
if(len(sys.argv) != 3):
  print ("Usage python covnert_gcv_file input_file output_file")
  exit()

INPUT=sys.argv[1]
OUTPUT=sys.argv[2]

nr_graphlets_keep = 8

lines = []
with open(INPUT) as f:
  for line in f:
    words = line.split(" ")

    words[-1] = words[-1][:-1]

    year = words[0].split(".")[0]
    country = words[0].split(":")[-1]
    lines += [country + "_" + year + "," + ",".join(words[1:nr_graphlets_keep+1])]

with open(OUTPUT, "w") as f:
  f.write("ID")

  for i in range(1,nr_graphlets_keep+1):
    f.write(",sig_" + str(i))

  f.write("\n")

  for line in lines:
    f.write(line + "\n")
