
import math
import sys
import random
import numpy as np

GCV_INPUT = "final_results/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_in2/gcv_list_matched-to_indicator_list_trimmed.csv"
INDICATOR_INPUT = "final_results/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_in2/indicator_list_trimmed_matched-to_gcv_list.csv"
#GCV_INPUT = "final_results/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_in/gcv_list_matched-to_indicator_list.csv"
#INDICATOR_INPUT = "final_results/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_in/indicator_list_matched-to_gcv_list.csv"
#GCV_INPUT = "final_results_norm1/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_in/gcv_list_matched-to_indicator_list.csv"
#INDICATOR_INPUT = "final_results_norm1/all_ppi/6-yeast_apms_collins_boone_CCA/CCA_in/indicator_list_matched-to_gcv_list.csv"

#GCV_INPUT = "test_classifier/gcv_list.txt"
#INDICATOR_INPUT = "test_classifier/indicator_list.txt"

labels = ['Nucl. trans.', 'Chrom. seg.', 'RNA proc.', 'Chrom. transc.', 'DNA repl.', 'Prot. deg.', 'Golgi sort.', 'Metab.' ,'Rib. transl.' ]

def readFile(myfile):
  res = []
  labels = []
  with open(myfile) as f:
    lines = f.readlines()

    labels = lines[0].split(",")
    labels[-1] = labels[-1][:-1]

    for line in lines[1:]:
      words = line.split(",")

      # strip the
      words[-1] = words[-1][:-1]

      res += [[float(x) for x in words[1:]]]


  return (labels[1:], res)

# points contains [(gcv, class)] while test_data contains [gcv]
def predict(points, test_data):

  gcv_points = [np.array(x) for (x,y) in points]

  predictions = []
  for test_gcv in test_data:
    distances = [np.linalg.norm(gcv - np.array(test_gcv)) for gcv in gcv_points]


    # zip with labels
    distances = zip (distances, [y for (x,y) in points])

    distances.sort()

    #print "distances:", distances[:NR_NEIGHBOURS]

    predicted_labels = [y for (x,y) in distances[:NR_NEIGHBOURS]]

    predicted_label = max(set(predicted_labels), key=predicted_labels.count)
    #print "predicted labels:", predicted_labels
    #print "final label:", predicted_label

    predictions += [predicted_label]

  return predictions


def comp_conf_matrix(pred, actual):

  l = len(pred)
  assert (l == len(actual))

  conf_matrix = np.zeros((NR_CLASSES, NR_CLASSES), int)

  for p, a in zip(pred, actual):
    conf_matrix[a][p] += 1

  return conf_matrix


def calc_stats(conf_matrix):
  prec_all = []
  rec_all = []
  f1_all = []

  for cls in range(NR_CLASSES):
    TP = conf_matrix[cls][cls]
    FP = sum(conf_matrix[:,cls]) - TP
    FN = sum(conf_matrix[cls,:]) - TP

    prec = 0.0
    rec = 0.0
    f1 = 0.0
    if (TP + FP != 0):
      prec = float(TP) / (TP + FP)

    if (TP + FN != 0):
      rec = float(TP) / (TP + FN)

    if (prec + rec != 0):
      f1 = 2 * prec * rec / (prec + rec)

    prec_all += [prec]
    rec_all += [rec]
    f1_all += [f1]

  return (prec_all, rec_all, f1_all)


def print_matrix(matrix):
  for i in range(len(matrix)):
    for j in range(len(matrix)):
      print "%d " % matrix[i][j],
    print "\n"

def print_matrix_latex(matrix):
  print r'''\begin{figure}[H]'''
  print r'''\centering'''
  print r'''\begin{tabular}{p{2.7cm} ''' + "".join(["p{1.0cm} " for x in range(len(matrix))]) + r'''}'''

  print "\cellcolor{header} Classes",
  for i in range(len(matrix)):
    print " & \cellcolor{header} " + labels[i],

  print "\\\\\n"

  for i in range(len(matrix)):
    print "\cellcolor{header} " + labels[i] + " & ",
    for j in range(len(matrix)):

      if (i == j):
        print "\cellcolor{diag} ",

      if j < len(matrix) -1:
        print "%d & " % matrix[i][j],
      else:
        print "%d\\\\" % matrix[i][j],

    print "\n"

  print r'''\end{tabular}'''
  print r'''\caption{}'''
  print r'''\label{conf_matrix}'''
  print r'''\end{figure}'''


def print_stats_latex(precision, recall, f1):
  print "Class & Precision & Recall & F1\\\\\n\hline"
  for i in range(len(precision)):
    print "%s & %.3f & %.3f & %.3f\\\\" % (labels[i], precision[i], recall[i], f1[i])


mat = np.loadtxt("conf_matrix.data")
print_matrix_latex(mat)


(x, gcv_list) = readFile(GCV_INPUT)
(class_labels, annotations) = readFile(INDICATOR_INPUT)

#print annotations

filter_indices = [0,4,5,10,13]
keep_indices = [x for x in range(len(class_labels)) if x not in filter_indices]

#print "filtered_classes:", class_labels[filtered_classes]

#class_labels_filtered = class_labels[keep_indices]

print
annotations = [x.index(1.0) for x in annotations]

#print "annotations", annotations

assert(len(annotations) == len(gcv_list))

#print zip(gcv_list, annotations)[0]


all_data = zip(gcv_list, annotations)
#random.shuffle(all_data)

N = len (annotations)
NR_FOLDS = 10
chunk_size = N / NR_FOLDS
NR_NEIGHBOURS = 5
NR_CLASSES = len(class_labels)
assert(NR_CLASSES == len(set(annotations)))

conf_matrix = np.zeros((NR_CLASSES, NR_CLASSES), int)
for k in range(NR_FOLDS):


  train_data = all_data[: k * chunk_size] + all_data[(k+1) * chunk_size :]
  test_data = all_data[k * chunk_size : (k+1) * chunk_size]

  assert(len(train_data) + len(test_data) == N)

  data_point_nr = 0
  #print "my data point:", test_data[data_point_nr]
  #print "group points:", np.array([x for x in train_data if x[1] == test_data[data_point_nr][1]])

  predictions = predict(train_data, [x for (x,y) in test_data]) # a vector of labels
  true_classes = [y for (x,y) in test_data]

  #pirint "(pred,true_clases) zip:", zip(predictions, true_classes)


  conf_matrix_tmp = comp_conf_matrix(predictions, true_classes)

  print "FOLD %d:\n" % k
  print_matrix(conf_matrix_tmp)

  conf_matrix += conf_matrix_tmp

(precision_all, recall_all, f1_all) = calc_stats(conf_matrix)


print "FINAL MATRIX :\n"
print_matrix_latex(conf_matrix)

print "precision all:", "".join([str(x) + " & " for x in precision_all])
print "recall all:", "".join([str(x) + " & " for x in recall_all])
print "f1 all:","".join([str(x) + " & " for x in f1_all])

print_stats_latex(precision_all, recall_all, f1_all)


assert(len(precision_all) == NR_CLASSES)
assert(len(recall_all) == NR_CLASSES)
assert(len(f1_all) == NR_CLASSES)

avg_prec = [x for x in precision_all if  not math.isnan(x)]
avg_rec = [x for x in recall_all if not math.isnan(x)]
avg_f1 = [x for x in f1_all if not math.isnan(x)]

#avg_prec = [x for x in precision_all if  x!= 0]
#avg_rec = [x for x in recall_all if x != 0]
#avg_f1 = [x for x in f1_all if x!= 0]

avg_prec = sum(avg_prec)/ len(avg_prec)
avg_rec = sum(avg_rec)/ len(avg_rec)
avg_f1 = sum(avg_f1)/ len(avg_f1)

print "\hline\nAverage & %.3f & %.3f & %.3f\\\\" % (avg_prec, avg_rec, avg_f1)

print "avg_prec:", avg_prec
print "avg_rec:", avg_rec
print "avg_f1:", avg_f1

np.savetxt("conf_matrix.data", conf_matrix)
