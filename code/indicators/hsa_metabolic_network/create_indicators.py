import sys

INPUT = sys.argv[1]
OUTPUT = sys.argv[2]

categories = []
ec_to_indicator = {}
with open(INPUT) as f:
  for line in f:
    if (line[:4] == "A<b>"):
      categories += [line[4:len(line) - 5]]


cur_category = -1
with open(INPUT) as f:
  for line in f:

    if (line[:4] == "A<b>"):
      cur_category += 1

    if (len(line) > 3 and line[-2] == "]" and "." in line):
      if(line[0] == "["):
        ec = "ec" + line[3:-2]
      else:
        #print "corrected ec:"
        ec = "ec:" + line[0:-2]

      print ec
      if (ec not in ec_to_indicator.keys()):
        ec_to_indicator[ec] = [0] * len(categories)

      ec_to_indicator[ec][cur_category] += 1


print categories

print ec_to_indicator.items()[:10]

with open(OUTPUT, "w") as f:
  f.write("ID")
  for cat in categories:
    f.write(",%s" % cat)

  f.write("\n")

  for ec in ec_to_indicator.keys():
    f.write("%s" % ec)
    for i in range(len(categories)):
      f.write(",%d" % ec_to_indicator[ec][i])
    f.write("\n")


