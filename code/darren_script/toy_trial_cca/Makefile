
#runs the matlab and the R code on a small dataset with X - 4x3 and Y = 4x2 
#outputs the CCA weights from both the R code and the matlab library function
all:
	make cca_matlab; make cca_R; echo "--------------------------\nComparison between matlab and R outputs\n\n--------\nX weights - matlab" && cat matlab_weights_X.csv && echo "Y weights - matlab" && cat matlab_weights_Y.csv; 	echo "--------\nVS\n--------\nX weights - R" && cat CCA_out2/toy1_reg=\[0.001,\ 0.001]_X-weights.csv && echo "Y weights - R" && cat CCA_out2/toy1_reg=\[0.001,\ 0.001]_Y-weights.csv && echo "----------"

#runs the R_code. The function called and the arguments passed are found at the end of the gcv_analyze_correlation.R script 
cca_R:
	cd code/ && Rscript R/gcv_analyze_correlation.R 

#runs the CCA from matlab and outputs 2 files: 
#matlab_weights_X.csv 
#matlab_weights_Y.csv
cca_matlab:
	matlab -nojvm -nodisplay -nosplash -r "canon_corr"
