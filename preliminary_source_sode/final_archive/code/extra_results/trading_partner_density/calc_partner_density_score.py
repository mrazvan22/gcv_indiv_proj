import sys
import os

# converts the file with entries like 1979.ndump2:SAU 1022 23 23525 626 2325 into gcv_list.csv with entries like 1979_SAU,1022,23, ..
if(len(sys.argv) != 3):
  print ("Usage python calc_partner_density_score <input_folder> <output_folder>")
  exit()


nr_graphlets_keep = 8


INPUT_FOLDER = sys.argv[1].rstrip('/')
OUTPUT_FOLDER = sys.argv[2]

country_to_gcv = {} # country_to_gcv[POL] = [(1973, [gcv]), ..]
fileList = os.listdir(INPUT_FOLDER)
for file in fileList:
  if file.endswith('.ndump2'):

    country = file.split(".")[0]
    country_to_gcv[country] = []
    with open(INPUT_FOLDER + "/" + file) as f:
      for line in f:
        words = line.split(" ")

        words[-1] = words[-1][:-1]

        year = int(words[0].split(".")[0])
        gcv = [float(x) for x in words[1:]]
        country_to_gcv[country] += [(year, gcv)]

print country_to_gcv.keys()

density_graphlets = [(12,0.9045), (10,0.8933),(14,0.8753),  # good graphlets
                     (2,-0.4865), (29, -0.5246),(8, -0.6374)] # bad graphlets

density_graphlets_indices = [x for (x,y) in density_graphlets]

density_scores = {}
for country in country_to_gcv.keys():
  density_scores[country] = []
  for i in range(len(country_to_gcv[country])):
    year = country_to_gcv[country][i][0]
    gcv = country_to_gcv[country][i][1]
    scores = [ w * gcv[nr-1] for (nr,w) in density_graphlets ]
    final_score = sum(scores)
    density_scores[country] += [(year, final_score)]

  print density_scores

  with open(OUTPUT_FOLDER + "/" + country + ".scores", "w") as f:

    for i in range(len(density_scores[country])):
      f.write("%d" % density_scores[country][i][0] + (" %.5f" % density_scores[country][i][1]) + "\n")

