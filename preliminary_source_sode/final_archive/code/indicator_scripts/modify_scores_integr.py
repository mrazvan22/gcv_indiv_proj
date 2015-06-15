

import sys

INPUT=sys.argv[1]
OUTPUT=sys.argv[2]

map_scores=[-3,-2,-1,0,1,2,3]

map_scores = [2*x for x in map_scores]
print map_scores

countries=[]
scores=[]

with open(INPUT) as f:
  next(f)
  for line in f:
    words = line.split(",")
    #print line
    #print words
    countries += [words[0]]
    scores += [int(words[1][0])]

with open(OUTPUT, "w") as f:
  f.write("ID,Integration_score\n")
  for i in range(len(countries)):
    f.write("%s,%d\n" % (countries[i] ,map_scores[scores[i]]))
