#usage python convert_cca_to_attrs.py <..../CCA_out/input_cca_file.txt>

import sys

INPUT=sys.argv[1]

attrs_out="/".join(INPUT.split("/")[:-1]) + "/attrs.txt"
graphlets_out="/".join(INPUT.split("/")[:-1]) + "/graphlets.txt"

print "Writing to files: " + attrs_out + "\n" + graphlets_out

attrs_lines = []
graphlet_lines = []

with open(INPUT) as f:
  lines = f.readlines()[17:]

 # print lines[:5]

  d = 0
  while (d < len(lines)):
    if (lines[d] == "\"x\"\n"):
      break

    d += 1
    #print d

  #print lines[d:d+5]

  c = 0
  for line in lines[d:]:
    words = line.split(" ")

    #strip the newline
    words[-1]=words[-1][:-1]
    left = " ".join(words[:-1])
    #left = "".join([x for x in left if x !='_' and x!='"'])
    right = words[-1][:-1]

    if("match" in left):
      break


    if(left == ""):
      #print "----->>>> ", right
      c += 1
      continue

    right = float(right)

    #print left

    if(left[:4] == "\"sig"):
      graphlet_lines += [(left, right)]
    else:
      attrs_lines += [(left, right)]

print "attrs_lines:", attrs_lines
print "graphlet_lines", graphlet_lines

with open(attrs_out, "w") as f:
  for line in attrs_lines:
    f.write(line[0] + " " +  str(line[1]) + "\n")

with open(graphlets_out, "w") as f:
  for line in graphlet_lines:
    f.write(line[0] + " " + str(line[1]) + "\n")

