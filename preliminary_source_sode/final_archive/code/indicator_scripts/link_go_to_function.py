#usage: link_go_to_function <output_file>

import sys

PROT_TO_GO="annotation_biogrid_id2_to_GO.txt"
GO_TO_FUNC="map2MGIslim.txt"

OUTPUT=sys.argv[1]

func_map = {}
with open(GO_TO_FUNC) as f:
  for line in f:
    words = line.split("\t")

    go_term, funct = words[0], words[2]
    ptype = words[-1][0]

    #print [go_term, funct, ptype]

    if(ptype == "P"):
      func_map[go_term] = funct

linesList=[]
with open(PROT_TO_GO) as f:
  for line in f:
    linesList += [line.split(" ")]

print "Starting to write to the output file"
all_keys = func_map.keys()
with open(OUTPUT, "w") as f:
  maxLines = len(linesList)
  c = 0
  for line in linesList:
    go_term = line[2][:-1]
    if(go_term in all_keys):
      #print line[0] + " " + line[1] + " " + func_map[go_term]
      f.write(line[0] + "\t" + func_map[go_term] + "\n")

    if (c % (maxLines/100) == 0):
      print str(c / (maxLines/100)) + "%"
    c +=1
