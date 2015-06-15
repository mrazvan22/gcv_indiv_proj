import sys

INPUT=sys.argv[1]
OUTPUT=sys.argv[2]


flat_list=[]

with open(INPUT) as f:
  years = f.readline().split(",")[1:]

  #strip the last '\n' character
  years[-1] = years[-1][:-1]

  nr_years = len(years)

  print years

  for line in f:
    words = line.split(",")
    #print line
    #print words
    country = words[0]
    scores = words[1:]

    #strip the last score from the '\n' character
    scores[-1] = scores[-1][:-1]
    print scores

    for i in range(nr_years):
      flat_list += [(country + "_" + years[i],scores[i])]


with open(OUTPUT, "w") as f:
  f.write("ID,Globalisation_score\n")
  for i in range(len(flat_list)):
    f.write("%s,%s\n" % (flat_list[i][0] ,flat_list[i][1]))



