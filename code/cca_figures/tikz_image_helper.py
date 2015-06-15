#usage python convert_cca_to_latex.py <..../CCA_out/input_cca_file.txt>

import sys

INPUT="../final_results/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_out/yeast_apms_collins.txt"
#INPUT="../final_results/all_trade_thresh/CCA_out/all_trade_thresh.txt"
#INPUT="../final_results_norm1/all_trade_thresh/CCA_out/all_trade_thresh.txt"
SHIFT=0
# for integration rtas use a shift of -3

x_variate = []
y_variate = []

with open(INPUT) as f:

  lines = f.readlines()[17+SHIFT:]

  p_values_line= lines[0].split(" ")
  canon_corr_line = lines[5].split(" ")
  canon_corr = canon_corr_line[-1][:-1]


  c = 0
  for line in lines[12:]:
    words = line.split(" ")

    #strip the newline
    words[-1]=words[-1][:-1]
    left = " ".join(words[:-1])
    left = "".join([x for x in left if x !='_' and x!='"'])
    right = words[-1][:-1]

    if("match" in left):
      break


    if(left == ""):
      #print "----->>>> ", right
      c += 1
      if c == 1:
        print "  \hline"
      continue

    if(left[:3] == "sig"):
      left = "G" + left[3:]

    right = float(right)

    if(c == 0):
      x_variate += [(left, right)]
    else:
      y_variate += [(left, right)]

  if (x_variate[0][0][0] == 'G' ):
    y_backup = [x for x in y_variate]
    y_variate = x_variate
    x_variate = y_backup

  x_variate = [(" ".join(x.split(".")), y) for (x,y) in x_variate]

  lenX = len(x_variate)
  lenY = len(y_variate)


#######################################


weights = [float(5 - x)/5 for x in range(11)]
print weights

for i in range(6):
  w = weights[i]

  red = 1 - w
  green = 1

  print "\definecolor{ccacol%d}{rgb}{%.2f,%.2f,0}" % (i, red, green)


for i in range(6,11):
  w = weights[i]

  red = 1
  green = w + 1

  print "\definecolor{ccacol%d}{rgb}{%.2f,%.2f,0}" % (i, red, green)


x_cross_loads = [-y for (x,y) in x_variate][::-1]
#x_cross_loads = [y for (x,y) in x_variate]

# scale the data
x_cross_loads = [1.8 * x for x in x_cross_loads]

print "x_cross_loads:",x_cross_loads

# calibration for WTN figures
#top_indicator_pos = (0, 4.8)
#cell_size = 0.475

# calibration for PPI figure
top_indicator_pos = (0.85, 4.10)
cell_size = 0.630

top_bar_pos = (4.0,5.0)
bottom_bar_pos = (4.0,-5.0)

lambda_mid = 0.25
pos2y_start = top_indicator_pos[0] * lambda_mid + bottom_bar_pos[0]* (1-lambda_mid)
pos2y_end = top_indicator_pos[0]* (1-lambda_mid) + bottom_bar_pos[0] * lambda_mid


N = len(x_cross_loads)

mid_weights = [abs(float(x) - float(N)/2)/(float(N)/2) for x in range(N)]

print "mid_weights", mid_weights

color_scaling = 1.0

for i in range(N):

  pos1 = (top_indicator_pos[0], top_indicator_pos[1] - i * cell_size)
  pos3 = (bottom_bar_pos[0], top_bar_pos[1] * x_cross_loads[i])

  #mid_weight = mid_weights[i]
  mid_weight = abs(pos1[1] - pos3[1])/3

  pos2y = (1 - mid_weight) * pos2y_end + mid_weight * pos2y_start
  pos2 = (pos2y, 5 * x_cross_loads[i])



  color = int(color_scaling * (10 - 5 * (x_cross_loads[i] + 1)))

  print "    \draw[line,color=ccacol%d] (%.2f,%.2f) -| (%.2f,%.2f) -- (%.2f,%.2f);" % (color, pos1[0], pos1[1],pos2[0], pos2[1],pos3[0], pos3[1],)

