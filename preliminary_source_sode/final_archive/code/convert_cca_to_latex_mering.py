#usage python convert_cca_to_latex.py <..../CCA_out/input_cca_file.txt>

import sys

INPUT=sys.argv[1]
SHIFT=int(sys.argv[2])
# for integration rtas use a shift of -3


annots = {}
annots['E'] = 'Energy production'
annots['G'] = 'Amino acid metabolism'
annots['M'] = 'Other - metabolism'
annots['P'] = 'Translation'
annots['T'] = 'Transcription'
annots['B'] = 'Transcriptional control'
annots['F'] = 'Protein fate'
annots['O'] = 'Cellular organisation'
annots['A'] = 'Transport and sensing'
annots['R'] = 'Stress and defence'
annots['D'] = 'Genome maintenance'
annots['C'] = 'Cellular fate / organisation'
annots['U'] = 'Uncharacterised'

with open(INPUT) as f:

  lines = f.readlines()[17+SHIFT:]

  p_values_line= lines[0].split(" ")
  canon_corr_line = lines[5].split(" ")
  canon_corr = canon_corr_line[-1][:-1]

  print "\n\n",INPUT

  print "\n"
  print r'''\begin{figure}[H]'''
  print r'''\centering'''
  print r'''\begin{tabular}{ c c | c c }'''
  #print canon_corr_line
  print r'''  \multicolumn{2}{c}{Canonical Correlation} & ''', ('''\multicolumn{2}{c}{%.5f}''' % float(canon_corr)), r'''\\'''
  print r'''  \multicolumn{2}{c}{p-value} & ''', ('''\multicolumn{2}{c}{%.5f}''' % float(p_values_line[3][:-1])), r'''\\'''
  #print r'''  \multicolumn{2}{c}{p-value} & ''', ('''\multicolumn{2}{c}{%.5f}''' % 0.0), r'''\\'''
  print "  \hline"
  print r'''  \multicolumn{2}{c}{X variate} & \multicolumn{2}{c}{Y variate}\\'''

  x_variate = []
  y_variate = []

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

  #print x_variate
  #print y_variate

  if (x_variate[0][0][0] == 'G' ):
    y_backup = [x for x in y_variate]
    y_variate = x_variate
    x_variate = y_backup

  x_variate = [(" ".join(x.split(".")), y) for (x,y) in x_variate]

  x_variate = [(annots[lab[2]],coeff) for (lab, coeff) in x_variate]

  #print x_variate


  lenX = len(x_variate)
  lenY = len(y_variate)

  for i in range(max(lenX, lenY)):
    if(i < lenX):
      print ''' %s & %.5f & ''' % x_variate[i],
    else:
      print ''' & & ''',

    if(i < lenY):
      print '''%s & %.5f\\\\''' % y_variate[i]
    else:
      print '''& \\\\'''


  print r'''\end{tabular}'''
  print r'''\caption{}'''
  print r'''\label{''' + INPUT.split(".")[0].split("/")[-1] +'''_cca}'''
  print r'''\end{figure}'''



