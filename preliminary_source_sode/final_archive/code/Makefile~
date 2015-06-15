CC=g++
CFLAGS=-funroll-loops
THREADS=8

##Compiling commands

all: g++_opt

g++_opt:
	$(CC) -O3 $(CFLAGS) avg_gdv.cpp -o avg_gdv
	$(CC) -O3 $(CFLAGS) e_gdv.cpp -o e_gdv
	$(CC) -O3 $(CFLAGS) genAvgEgdvRndNets.cpp -o genAvgEgdvRndNets
	$(CC) -O3 $(CFLAGS) pears_coeff.cpp -o pears_coeff
	$(CC) -O3 $(CFLAGS) pears_coeff_gdv.cpp -o pears_coeff_gdv
	$(CC) unit_tests.cpp -o unit_tests -lboost_unit_test_framework
	
# keep ncount separate as it yields a lot of warnings at compile time
g++_ncount:	
	$(CC) -O3 $(CFLAGS) ncount.cpp -o ncount

g++_gdb:
	$(CC) -g $(CFLAGS) avg_gdv.cpp -o avg_gdv
	$(CC) -g $(CFLAGS) e_gdv.cpp -o e_gdv
	$(CC) -g $(CFLAGS) genAvgEgdvRndNets.cpp -o genAvgEgdvRndNets
	$(CC) -g $(CFLAGS) ncount.cpp -o ncount
	$(CC) -g $(CFLAGS) pears_coeff.cpp -o pears_coeff
	$(CC) unit_tests.cpp -o unit_tests -lboost_unit_test_framework

##########################
## Running commands ######
##########################

#### Evaluation ####

# number of threads vs time - how paralalisation scales 
time_egdv:
	echo "1,2,4,8" | xargs -i -d, /usr/bin/time -o /dev/tty ./e_gdv trade_2010_thresholded.gw test {} 1 > /dev/null 2>&1

eval_life_cycle:
	make eval_all_rnd_calc_other_sigs && make eval_all_rnd_cmp_dist && make eval_all_rnd_aupr


# computes the 150x150 distance matrix between 30 networks x 5 types (ER, ERDD, GEO, SF, STICKY)
eval_rnd_net_dist:
	python eval_dist.py 2 final_results/trade_2010_thresholded/gcv_dist.matrix

# computes the mds positions in 3D, writes them to an output file and plots them in 3D
eval_rnd_net_mds:
	python eval_mds.py full final_results/trade_2010_thresholded/eval_results/gcv_pears_dist.matrix final_results/trade_2010_thresholded/eval_results/eval_mds_pos_rnd_nets.data

# computes the precision-recall graphs, plots them and calculates the AUPR
eval_rnd_net_aupr:
	python eval_aupr.py final_results/trade_2010_thresholded/eval_results/gcv_pears_dist.matrix final_results/trade_2010_thresholded/eval_results/precision_recall.data | gnuplot

# calculates all the sigs for all the random nets networks
eval_all_rnd_calc_other_sigs:
	python eval_all_rnd_nets_sigs.py model_nets_rand_generated 2 1

# computes all the 150x150 distance matrices for the deg dist, clust coeff etc (excluding GCV dist) and writes the distance matrices to final_results folder .. assumes trade_2010_thresholded
eval_all_rnd_cmp_dist:
	python eval_all_rnd_cmp_dist.py 2 

eval_all_rnd_aupr:
	python eval_aupr_all_rnd.py | gnuplot

###################################################################
###### Metabolic network CCA on the Kegg categories - "the sugars"
###################################################################

a_level_net:
	cd code/indicators/hsa_metabolic_network && less hsa00001.keg | grep -v "C  " | grep -v "B  " | awk '{if (substr($1,0,4) == "A<b>") print $0; else print $NF;}' > a_level_annotations.txt

a_level_create_indicator_file_kegg:
	python create_indicators.py a_level_annotations.txt a_level_indicator_list.txt

b_level_create_indicator_file_kegg:
	echo "metabolism,genetic,environmental,cellular,organismal,human," | xargs -i -d, python create_indicators_b_level.py b_{}_annot.txt b_{}.indicator


canon_meta_kegg_b_level_norm1:
	echo "metabolism,genetic,environmental,cellular,organismal,human," | xargs -i -d, make INDICATOR_FILE=b_{}.indicator CCA_FOLDER=b_{} FINAL_FOLDER=final_results_norm1 GEN_FOLDER=generated_results_norm1/hsa_metabolic_kegg_CCA NET=hsa_metabolic_network canon_meta_kegg_helper

canon_meta_kegg_a_level_norm1:
	make INDICATOR_FILE=a_level_indicator_list.txt CCA_FOLDER=a_level FINAL_FOLDER=final_results_norm1 GEN_FOLDER=generated_results_norm1/hsa_metabolic_kegg_CCA NET=hsa_metabolic_network canon_meta_kegg_helper


canon_meta_kegg_b_level:
	echo "metabolism,genetic,environmental,cellular,organismal,human," | xargs -i -d, make INDICATOR_FILE=b_{}.indicator CCA_FOLDER=b_{} FINAL_FOLDER=final_results GEN_FOLDER=generated_results/hsa_metabolic_kegg_CCA NET=hsa_metabolic_network canon_meta_kegg_helper


canon_meta_kegg_a_level:
	make INDICATOR_FILE=a_level_indicator_list.txt CCA_FOLDER=a_level FINAL_FOLDER=final_results GEN_FOLDER=generated_results/hsa_metabolic_kegg_CCA NET=hsa_metabolic_network canon_meta_kegg_helper

canon_meta_kegg_helper:
	make canon_filehandling_kegg && make canon_convert_ndump_to_csv_kegg && make canon_copy_indicator_kegg && make canon_align_instances_kegg && make canon_run_R_kegg

canon_filehandling_kegg:
	cd $(GEN_FOLDER) && mkdir $(CCA_FOLDER) && cd $(CCA_FOLDER)/ && mkdir CCA_in && mkdir CCA_out && cd $(PROJECT_FOLDER)

canon_convert_ndump_to_csv_kegg:
	python cca/ndump_to_nodeinfo.py $(FINAL_FOLDER)/hsa_meta_ec_omer/hsa_meta_ec_omer.ndump2 $(CANON_NET_PATH)/gcv_list.csv

canon_copy_indicator_kegg:
	cp indicators/$(NET)/$(INDICATOR_FILE) $(CANON_NET_PATH) && mv $(CANON_NET_PATH)/$(INDICATOR_FILE) $(CANON_NET_PATH)/indicator_list.csv

canon_align_instances_kegg:
	python cca/align_instances.py $(CANON_NET_PATH)/gcv_list.csv $(CANON_NET_PATH)/indicator_list.csv $(CANON_NET_PATH)/CCA_in

canon_run_R_kegg:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET) reg_off

canon_run_R_regularised_kegg:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET) reg_given 0.001 0.001

canon_clean_kegg:
	rm -rf $(CANON_NET_PATH)

#### Extra results ####

saudi_oil:
	cd /extra_results/saudi_oil && python saudi_oil_vs_gcv.py saudi_norm1_gcv_over_years.txt ../../final_results/crudeoilprices.csv saudi_norm1_gcv_oil.data | gnuplot

saudi_cca:
	make NET=saudi_oil CANON_NET_PATH=extra_results/saudi_oil/cca_oil/ canon_run_R_regularised_single


# this is how I should use redirection with xargs 
gen_ndump_all_countries_per_year:
	awk '{print $1}' 1962.ndump2 | xargs -I xxxx sh -c 'grep "xxxx" *.ndump2 > ../../extra_results/trading_partner_density/norm1_gcv_files/"xxxx".ndump2'


### CCA figure generation ###


create_cca_figure:
	make NET=all_trade_thresh CCA_FOLDER=final_results_norm1/all_trade_thresh/CCA_out NEG_SIGNS=0 cca_figure_helper_all

convert_cca_to_attrs:
	python cca_figures/convert_cca_to_attrs.py $(CCA_FOLDER)/$(NET).txt

cca_figure_helper:
	python cca_figures/visAttrsVsGraphlets.py $(CCA_FOLDER)/attrs.txt $(CCA_FOLDER)/graphlets.txt $(CCA_FOLDER)/cca_figure $(NEG_SIGNS)

cca_figure_helper_all:
	make convert_cca_to_attrs && make cca_figure_helper


############################


#not working yet
plot_pearsons_all:
	cd final_results && echo "hsa_metabolic_network,human_ppi,trade_2010" | xargs -d, -L 1 python plot_pearsons_heatmap.py | gnuplot

plot_pearsons_trade:
	cd final_results && python plot_pearsons_heatmap.py trade_2010 | gnuplot

convert_all_to_gw:
	python input_nets/convert_all_to_gw.py input_nets/FOOD_AND_LIVE_ANIMALS 1962 2011

create_ppi_nets:
	python input_nets/create_ppi_nets.py $(INPUT_NET) $(OUTPUT_NET) $(TYPE)

create_human_ppi_full_biogrid:
	make INPUT_NET=input_nets/human_ppi_all/biogrid-ppi/human_ppi_full.txt OUTPUT_NET=input_nets/human_ppi_all/biogrid-ppi/biogrid_human_ppi_full.txt TYPE=normal create_ppi_nets

cut_yeast_net_biogrid:
	cat input_nets/yeast_ppi_all/biogrid-ppi/BIOGRID-ORGANISM-Saccharomyces_cerevisiae-3.2.111.tab2.txt| grep physical | cut -f6,7,15 | sort | uniq | wc -l


#################################################################
##### Canonical correlation - Metabolic compound networks #######

#NET=human_ppi
#NET=hsa_meta_ec_omer
#NET=cel_metabolic
INDICATOR_TYPE=EC
#INDICATOR_TYPE=GO

#Note: For metabolic networks which have EC numbers as the node labels, move the $(NET).gw file to indicators/$(NET)/final.txt
#cel,dme,eco,hsa,mmu,sce
NET_NAME=cel
NET_CMP=$(NET_NAME)_metabolic_network
CANON_NET_PATH_CMP=$(GEN_FOLDER)/metabolic_nets_compounds/$(NET_NAME)_metabolic_network_CCA
INDICATOR_TYPE_CMP=METABOLIC_COMPOUND
GW_SOURCE=input_nets/metabolic_nets_compounds/$(NET_NAME)_metabolic_network.gw
THREADS=8
INDICATOR_SOURCE=indicators/metabolic_nets_compounds/$(NET_NAME)_metabolic_network_final.txt

# WARNING: the CCA R script sometimes doesn't work on my personal laptop. run on the lab machines instead!!

# use thic command and only set NET_NAME=cel .. dme,eco,mmu,sce
canon_lc_meta:
	 make canon_filehandling_cmp && make canon_compute_egdv_cmp && make canon_convert_ndump_to_csv_cmp && make canon_convert_indicators_to_csv_cmp && make canon_align_instances_cmp && make canon_run_R_cmp_reg_given

#don't use the cmd below .. instead, change the parameters above
canon_lc_meta_cel:
	make NET=cel_metabolic_network CANON_NET_PATH_CMP=generated_results/metabolic_nets_compounds/cel_metabolic_network_CCA INDICATOR_TYPE_CMP=METABOLIC_COMPOUND GW_SOURCE=input_nets/metabolic_nets_compounds/cel_metabolic_network.gw THREADS=4 INDICATOR_SOURCE=indicators/metabolic_nets_compounds/cel_metabolic_network_final.txt canon_filehandling_meta && make canon_compute_egdv_cmp && make canon_convert_ndump_to_csv_cmp && make canon_convert_indicators_to_csv_cmp && make canon_align_instances_cmp && make canon_run_R_regularised_cmp

canon_filehandling_cmp:
	cd $(GEN_FOLDER)/metabolic_nets_compounds && mkdir $(NET_CMP)_CCA && cd $(NET_CMP)_CCA/ && mkdir CCA_in && mkdir CCA_out && cd ../../../ && pwd && cp $(GW_SOURCE) $(CANON_NET_PATH_CMP)

canon_convert_indicators_to_csv_cmp:
	python cca/convert_indicators_to_csv_single.py $(INDICATOR_TYPE_CMP) $(INDICATOR_SOURCE) $(CANON_NET_PATH_CMP)/indicator_list.csv
	
canon_compute_egdv_cmp:
	./e_gdv $(CANON_NET_PATH_CMP)/$(NET_CMP).gw $(CANON_NET_PATH_CMP)/$(NET_CMP) $(THREADS) $(NORM_TYPE)

canon_convert_ndump_to_csv_cmp:
	python cca/ndump_to_nodeinfo.py $(CANON_NET_PATH_CMP)/$(NET_CMP).ndump2 $(CANON_NET_PATH_CMP)/gcv_list.csv

canon_align_instances_cmp:
	python cca/align_instances.py $(CANON_NET_PATH_CMP)/gcv_list.csv $(CANON_NET_PATH_CMP)/indicator_list.csv $(CANON_NET_PATH_CMP)/CCA_in

canon_run_R_cmp_reg_on:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH_CMP)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET_CMP) reg_on

canon_run_R_cmp_reg_off:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH_CMP)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET_CMP) reg_off


canon_run_R_cmp_reg_given:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH_CMP)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET_CMP) reg_given 0.001 0.001

canon_clean_cmp:
	rm -rf $(CANON_NET_PATH_CMP)



#######################################################
##### Canonical correlation - PPI network series ######

#NET=human_ppi
#NET=hsa_meta_ec_omer
#NET=cel_metabolic
INDICATOR_TYPE=EC
#INDICATOR_TYPE=GO

CANON_NET_PATH_PPI=generated_results_norm1/all_ppi/$(FOLDER)_CCA


GEN_FOLDER_CANON_PPI=generated_results_norm1/all_ppi/
NORM_TYPE_PPI=1

# WARNING: the CCA R script sometimes doesn't work on my personal laptop. run on the lab machines instead!!

#Note: For metabolic networks which have EC numbers as the node labels, move the $(NET).gw file to indicators/$(NET)/final.txt

all_ppi_latex:
	cd final_results/all_ppi/ && find . -name "*.txt" | grep CCA_out | sort | xargs -i  python ../../convert_cca_to_latex.py {} > all_ppi_latex.txt

# ppi_lifecycle_cca.py <part1/part2/all> <annotations_folder> <nr_threads> <net_nr>
canon_lc_ppi:
	echo "1" | xargs -i -d, python ppi_lifecycle_cca.py part2 indicators/ppi_annotations_all/ 4 {} generated_results_norm1/all_ppi/

canon_lc_ppi_bionets:
	echo "1" | xargs -i -d, python ppi_lifecycle_cca.py all indicators/ppi_annotations_all/ 64 {} generated_results_norm1/all_ppi/

canon_yeast_lc_ppi:
	make NET=yeast_lc GW_SOURCE= INDICATOR_SOURCE= THREADS= canon_lc_ppi_all

canon_lc_ppi_part1:
	make canon_filehandling_ppi && make canon_compute_egdv_ppi

canon_lc_ppi_part2:
	make canon_convert_ndump_to_csv_ppi && make canon_convert_indicators_to_csv_ppi && make canon_align_instances_ppi && make canon_run_R_regularised_ppi

canon_lc_ppi_all:
	make canon_filehandling_ppi && make canon_compute_egdv_ppi && make canon_convert_ndump_to_csv_ppi && make canon_convert_indicators_to_csv_ppi && make canon_align_instances_ppi && make canon_run_R_regularised_ppi

# Assumes folder generated_results/all_ppi/
canon_filehandling_ppi:
	cd $(GEN_FOLDER_CANON_PPI) && mkdir $(FOLDER)_CCA && cd $(FOLDER)_CCA/ && mkdir CCA_in && mkdir CCA_out && cd ../../../ && cp $(GW_SOURCE) $(CANON_NET_PATH_PPI)

canon_compute_egdv_ppi:
	./e_gdv $(CANON_NET_PATH_PPI)/$(NET).gw $(CANON_NET_PATH_PPI)/$(NET) $(THREADS) $(NORM_TYPE_PPI)

canon_convert_ndump_to_csv_ppi:
	python cca/ndump_to_nodeinfo.py $(CANON_NET_PATH_PPI)/$(NET).ndump2 $(CANON_NET_PATH_PPI)/gcv_list.csv

canon_convert_indicators_to_csv_ppi:
	python cca/convert_indicators_to_csv_single.py FUNCTIONAL_SIMPLE $(INDICATOR_SOURCE) $(CANON_NET_PATH_PPI)/indicator_list.csv

canon_align_instances_ppi:
	python cca/align_instances.py $(CANON_NET_PATH_PPI)/gcv_list.csv $(CANON_NET_PATH_PPI)/indicator_list.csv $(CANON_NET_PATH_PPI)/CCA_in

canon_run_R_ppi_reg_on:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH_PPI)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET) reg_on

canon_run_R_regularised_ppi:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH_PPI)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET) reg_given 0.001 0.001

canon_clean_ppi:
	rm -rf $(CANON_NET_PATH_PPI)



#######################################################
##### Canonical correlation - Single network ##########

# used for metabolic networks - enzyme based .. DO not use for compound metabolic networks

#NET=human_ppi
#NET=hsa_meta_ec_omer
#NET=cel_metabolic
INDICATOR_TYPE=EC
#INDICATOR_TYPE=GO

# for unnormalized vectors 
#FINAL_FOLDER=final_results/

# for norm1
#FINAL_FOLDER=final_results_norm1/
CANON_NET_PATH=$(GEN_FOLDER)/$(CCA_FOLDER)

#Note: For enzyme metabolic networks which have EC numbers as the node labels, move the $(NET).gw file to indicators/$(NET)/final.txt Do not use this framework for compound metabolic networks .. they have a separate section above  

# WARNING: the CCA R script sometimes doesn't work on my personal laptop. run on the lab machines instead!!

# trade integration using the RTAs file I got from the WTO website
canon_trade_integr_rtas:
	make INDICATOR_FILE=rtas-wto-final4.csv CCA_FOLDER=integration_norm1_rtas FINAL_FOLDER=final_results_norm1 GEN_FOLDER=generated_results_norm1/trade_2010_thresholded_CCAS NET=trade_2010_thresholded canon_trade_integr_helper

# integration with the values I got from the wikipedia map
canon_trade_integr:
	make INDICATOR_FILE=indicator_list_zero_centered.csv CCA_FOLDER=integration_unnorm_zero_centered FINAL_FOLDER=final_results GEN_FOLDER=generated_results_norm1/trade_2010_thresholded_CCAS NET=trade_2010_thresholded canon_trade_integr_helper

canon_trade_integr_helper:
	make canon_filehandling_single && make canon_convert_ndump_to_csv_single && make canon_copy_indicator && make canon_align_instances_single && make canon_run_R_single

canon_cel_enz_norm1:
	make GEN_FOLDER=generated_results_norm1/metabolic_nets_enzymes FINAL_FOLDER=final_results_norm1/metabolic_nets_enzymes NET=cel_metabolic canon_lc_single_reg_given

canon_lc_single_reg_given:
	make canon_filehandling_single && make canon_convert_ndump_to_csv_single && make canon_convert_indicators_to_csv_single && make canon_align_instances_single && make canon_run_R_regularised_single

canon_lc_single_reg_off:
	make canon_filehandling_single && make canon_convert_ndump_to_csv_single && make canon_convert_indicators_to_csv_single && make canon_align_instances_single && make canon_run_R_single

canon_filehandling_single:
	cd $(GEN_FOLDER) && mkdir $(CCA_FOLDER) && cd $(CCA_FOLDER)/ && mkdir CCA_in && mkdir CCA_out && cd $(PROJECT_FOLDER)

canon_convert_ndump_to_csv_single:
	python cca/ndump_to_nodeinfo.py $(FINAL_FOLDER)/$(NET)/$(NET).ndump2 $(CANON_NET_PATH)/gcv_list.csv

canon_copy_indicator:
	cp indicators/trade_2010_thresholded_integration/$(INDICATOR_FILE) $(CANON_NET_PATH) && mv $(CANON_NET_PATH)/$(INDICATOR_FILE) $(CANON_NET_PATH)/indicator_list.csv

canon_convert_indicators_to_csv_single:
	python cca/convert_indicators_to_csv_single.py $(INDICATOR_TYPE) indicators/$(NET)/final.txt $(CANON_NET_PATH)/indicator_list.csv

canon_align_instances_single:
	python cca/align_instances.py $(CANON_NET_PATH)/gcv_list.csv $(CANON_NET_PATH)/indicator_list.csv $(CANON_NET_PATH)/CCA_in

canon_run_R_single:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET) reg_off

canon_run_R_regularised_single:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH)/CCA_out ../CCA_in/gcv_list_matched-to_indicator_list.csv  ../CCA_in/indicator_list_matched-to_gcv_list.csv $(NET) reg_given 0.001 0.001

canon_clean_single:
	rm -rf $(CANON_NET_PATH)

##############################################
##### Canonical correlation - Trade ##########

#CANON_NET_PATH=$(GEN_FOLDER)/$(NET)_CCA
NR_THREADS=8

#NORM_TYPE=0
#GEN_FOLDER=generated_results
#CANON_INPUT_NDUMP=final_results/$(NET)/ndump2_CCA

#NORM1
NET=all_trade_thresh
GEN_FOLDER=generated_results_norm1
INPUT_SOURCE=trade_2010_thresholded.gw
NORM_TYPE=1
CANON_INPUT_NDUMP=final_results_norm1/$(NET)/ndump2_CCA
CANON_INPUT_INDICATORS=indicators/$(NET)

# WARNING: the CCA R script sometimes doesn't work on my personal laptop. run on the lab machines instead!!

canon_toy1:
	cd darren_script/my_trial/code/ && Rscript R/gcv_analyze_correlation.R 

canon_food_lc:
	make NET=FOOD_AND_LIVE_ANIMALS_THRESH_85 CANON_INPUT_INDICATORS=indicators/all_trade_thresh canon_lc

canon_minerals_lc:
	make NET=MINERAL_FUELS_THRESH_85 CANON_INPUT_INDICATORS=indicators/all_trade_thresh canon_lc

canon_trade_lc:
	make NET=all_trade_thresh CCA_FOLDER=all_trade_thresh_CCA CANON_INPUT_INDICATORS=indicators/all_trade_thresh canon_lc

canon_lc:
	make canon_filehandling && make canon_convert_to_csv && make canon_combine_csv && make canon_reformat_indices && make canon_add_extra_vars && make canon_align_instances && make canon_run_R

# Create the necessary directories
canon_filehandling:
	cd $(GEN_FOLDER) && mkdir $(NET)_CCA && cd $(NET)_CCA/ && mkdir CCA_in && mkdir CCA_out && mkdir reformatted_econ_attrs && mkdir reformatted_networks && cd reformatted_networks && mkdir per-year  && cd ../../../	

# Convert the economic networks from ndump2 to csv. The lowest-level output directory should not be created yet.
# convert_all_ndump_to_nodeinfo.py in_dir out_dir
canon_convert_to_csv:
	python cca/convert_all_ndump_to_nodeinfo.py $(CANON_INPUT_NDUMP) $(CANON_NET_PATH)/reformatted_networks/per-year

# Combine the information from the per-year CSVs into a new file
# python join_econ_network_years.py in_dir out_file
canon_combine_csv:
	python cca/join_econ_network_years.py $(CANON_NET_PATH)/reformatted_networks/per-year $(CANON_NET_PATH)/reformatted_networks/combined_network_years.csv

# Reformat the needed data from Vuk's country-info files into a csv
# Country/year instances with incomplete data will be dropped
canon_reformat_indices:
	python cca/econ_node_info_to_year_aggregated_csv.py $(CANON_INPUT_INDICATORS) $(CANON_NET_PATH)/reformatted_econ_attrs/

# Add variables that are products or quotients of other variables (e.g., to get GDP from per-capita GDP x population)
# python augment_with_products.py infile_name outfile_name
canon_add_extra_vars:
	python cca/augment_with_products.py $(CANON_NET_PATH)/reformatted_econ_attrs/1980to2010_complete-countries.csv $(CANON_NET_PATH)/reformatted_econ_attrs/1980to2010_complete-countries_augmented.csv

# Make sure that each instance corresponds to the same row in the network and economic-attribute files. 
# This will remove instances that cannot be matched (i.e., that aren't in both files)
# Two files will be produced in the given output directory.
# python align_instances.py file1 file2 out_dir
canon_align_instances:
	python cca/align_instances.py $(CANON_NET_PATH)/reformatted_econ_attrs/1980to2010_complete-countries_augmented.csv $(CANON_NET_PATH)/reformatted_networks/combined_network_years.csv $(CANON_NET_PATH)/CCA_in

# Run the actual CCA. These commands should be run in an R interpreter. I ran this with R 2.15.2. Results will be placed in R's working directory.
# You may need to install some R packages for this to run.
# Since this automatically chooses regularization coefficients, it will take a little while to run.
canon_run_R:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH)/CCA_out ../CCA_in/1980to2010_complete-countries_augmented_matched-to_combined_network_years.csv  ../CCA_in/combined_network_years_matched-to_1980to2010_complete-countries_augmented.csv $(NET) reg_on

# Same as above but uses the 0.001-0.001 regularization parameters. When running an experiment for the first time, first run the above command canon_run_R which lets the algorithm find the best regularization parameters and the plug them in here. 
canon_run_R_regularised:
	cd cca/ && Rscript R/gcv_analyze_correlation.R ../$(CANON_NET_PATH)/CCA_out ../CCA_in/1980to2010_complete-countries_augmented_matched-to_combined_network_years.csv  ../CCA_in/combined_network_years_matched-to_1980to2010_complete-countries_augmented.csv $(NET) reg_given 0.001 0.001

	

#########################################
## Whole life-cycle for one network #####

#change this to anything
#NET=human_ppi_small
#NET=hsa_metabolic_network
#NET=human_ppi
#NET=trade_2010
#NET=trade_2010_thresholded
#NET=all_trade_thresh
##

LIT_TYPE=knuth
#NET_PATH=$(GEN_FOLDER)/$(LIT_TYPE)_literature/$(NET)
#NET_SOURCE=input_nets/$(LIT_TYPE)_literature

NET_PATH=$(GEN_FOLDER)/$(NET)
NET_SOURCE=.
NORM_TYPE=1

#PROJECT_FOLDER=~/4-th_year/gdv_extension_proj/code
PROJECT_FOLDER=/vol/bio-nets/users/rvm10/gdv_extension_proj/code


# When running the life-cycle, one might want to change the generated_results subfolder and NETPATH

lit_anna:
	make NET=anna GEN_FOLDER=generated_results NORM_TYPE=0 life-cycle

# change cel to dme,eco, etc .. xargs doesn't work
# enzyme version
cel_meta_enz_lc:
	make GEN_FOLDER=generated_results_norm1/metabolic_nets_enzymes NET_SOURCE=input_nets/metabolic_nets_enzymes NET=cel_metabolic life-cycle

# compound version
cel_meta_cmp_lc:
	make GEN_FOLDER=generated_results_norm1/metabolic_nets_compounds NET_SOURCE=input_nets/metabolic_nets_compounds NET=cel_metabolic_network life-cycle

# Runs the life cycle for all the basic nets
all_lc_3:
	make NET=hsa_metabolic_network life-cycle && make NET=human_ppi life-cycle && make NET=trade_2010_thresholded life-cycle

# Runs the whole Egdv - Avg - Pearsons - Hierarchical clustering - Heatmap - Poly normalization life cycle 
life-cycle:
	make initial_filehandling && make egdv_lc && make avg_egdv_lc && make pearsons_lc && make hclust_lc && make hclust_poly && make hclust_lc_orig

# Assumes directory generated_results exists in the current folder. If not, create it. This has not been added to the repository. This command creates the necessary directories in generated_results/  
initial_filehandling:
	cd $(GEN_FOLDER) && mkdir $(NET) && cd $(PROJECT_FOLDER) && cp $(NET_SOURCE)/$(NET).gw $(NET_PATH)

# Calculate the list of GCVs by spacifying the input graph, output file and the nr of threads
egdv_lc:
	./e_gdv $(NET_PATH)/$(NET).gw $(NET_PATH)/$(NET) $(THREADS) $(NORM_TYPE)

# Instead of calculating the e_gdv using the command above, copy it from the final_results directory	
copy_egdv_from_final_lc:
	cp final_results/$(NET)/$(NET).ndump2 $(NET_PATH)/

# Calculate the average GCV across all the nodes in the network. This average might also be normalized so that it sums to 1. Note that this normalization is not actually used by the pearsons script below. Instead, that script uses some methods from algo_utils in order to calculate the true average of the GCV vectors
avg_egdv_lc:
	./avg_gdv $(NET_PATH)/$(NET).ndump2 > $(NET_PATH)/$(NET).avg

# Calculae the Pearsons's correlation coefficient from the .ndump2 file and output both the (NR_GRAPHLETS x NR_GRAPHLETS) correlation matrix and a normalised version of this matrix in which the range (min-max) has been scaled to (0-1)
pearsons_lc:
	./pears_coeff $(NET_PATH)/$(NET).ndump2 $(NET_PATH)/pearsons_$(NET).data $(NET_PATH)/pearsons_normalized_$(NET).data $(NORM_TYPE)

# Perform hierarchical clustering on the original pears matrix, write the .data file and the plot it with gnuplot
hclust_lc_orig:
	python final_results/h_clust.py $(NET_PATH)/pearsons_$(NET).data $(NET_PATH)/pearsons_hclust_orig_$(NET).data -1 1 | gnuplot


# Perform hierarchical clustering on the normalised matrix, write the .data file and the plot it with gnuplot
hclust_lc:
	python final_results/h_clust.py $(NET_PATH)/pearsons_normalized_$(NET).data $(NET_PATH)/pearsons_hclust_$(NET).data 0 1 | gnuplot

# Same as above but perform it also for when the matrix has been extra normalized using a polynomial function. Each matrix that has been normalised with a polynomial function has also been normalised before with the standard method (min,max) -> (0,1)
hclust_poly:
	echo "2,3,4," | xargs -i -d, python final_results/h_clust.py $(NET_PATH)/pearsons_normalized_$(NET)-poly-{}.data $(NET_PATH)/pearsons_hclust_$(NET)-poly-{}.data 0 1 | gnuplot  

move_to_final_pearsons:
	cp $(NET_PATH)/pearsons_$(NET).data final_results/$(NET)/

clean_lc:
	cd generated_results && rm -rf $(NET)

# Adapted from h_clust.py, but it doesn't do any permutation
gen_normal_heatmap:
	python final_results/gen_normal_pears_heatmap.py $(NET_PATH)/pearsons_$(NET).data

all_trade_lc_part1:
	python all_trade_life_cycle.py part1 all_trade_thresh trade_nets 1962 2011 2 generated_results_norm1 1

all_trade_lc_part2:
	python all_trade_life_cycle.py part2 all_trade_thresh trade_nets 1962 2011 2 generated_results_norm1 1

see_trade_heatmaps:
	gnome-open final_results/all_trade_thresh/heatmap_pearsons_hclust_1962.png &

#python h_clust.py <input_folder> <basename> <start_year> <end_year> <out_file_base>'
dist_heatmaps:
	python dist_heatmaps.py final_results_norm1/all_trade_thresh pearsons_ 1962 2011 change_over_time | gnuplot

#NET=FOOD_AND_LIVE_ANIMALS_THRESH_85

# runs the life-cycle for the comodity nets, thresholded to 85% 
all_commodity_lc_part1:
	python all_trade_life_cycle.py part1 $(NET) input_nets/$(NET) 1962 2011 4

###################################################
#################### Tests ########################

# Assumes a directory test_bank/ exists under code/
test:
	./unit_tests

specific_test_example:
	./unit_tests --run_test=egdvs/trade_egdvs


test_extra_node:
	./e_gdv tests/trade_2010_thresholded_extra_node.gw tests/trade_2010_thresholded_extra_node.out $(THREADS) && ./ncount tests/trade_2010_thresholded.gw tests/trade_2010_thresholded_gdv.res && rm tests/trade_2010_thresholded_gdv.res.* && tail -n 29 tests/trade_2010_thresholded_extra_node.out.egdvs > tests/trade_2010_thresholded_extra_node.out.egdvs.last && diff tests/trade_2010_thresholded_extra_node.out.egdvs.last tests/trade_2010_thresholded_gdv.res

clean_tests:
	rm tests/trade_2010_thresholded_extra_node.out.* tests/*.res tests/*.res.* 


###################################################
#### Pearson's correlation coefficient matrices ###

pearson_metabolic:
	./pears_coeff hsa_metabolic_network

h_clust_human:
	python final_results/h_clust.py final_results/human_ppi/pearsons_normalized_human_ppi.data final_results/human_ppi/pearsons_hclust_human_ppi.data | gnuplot


## Calculate old-fashioned GDVs - Natasha's stuff

test_for:
	for x in trade_2010.gw human_ppi.gw; do \
		head -n 10 $$x; \
	done

gdv_trade_2010_thresholded:
	./ncount trade_2010_thresholded.gw final_results/trade_2010_thresholded_normal_gdvs.res  

clean_final_res_from_ncount:
	rm final_results/*.cl_* && rm final_results/*.gr_freq && rm final_results/*.ndump2

############################################################
## List containing all E-GDVs for each node in the graph ###


egdv_human_small:
	./e_gdv small_nets/human_ppi_small.gw small_nets/human_ppi_small_egdv.out $(THREADS)

egdv_small1:
	./e_gdv small_nets/small_network_1.gw small_nets/small_network_1.out $(THREADS)

# takes a few seconds with 8 threads
egdv_human_full:
	./e_gdv human_ppi.gw human_ppi.out $(THREADS)

# takes a few seconds with 8 threads
egdv_metabolic_full:
	./e_gdv hsa_metabolic_network.gw hsa_metabolic_network.out $(THREADS)

# note that although it is one of the smallest networks, calculating the EGDVS takes the most (because the network is almost complete)
# average running time: 2.5h with 8 threads
egdv_trade_full:
	./e_gdv trade_2010.gw trade_2010.out $(THREADS)

# takes a few seconds with 8 threads
egdv_trade_thresh_full:
	./e_gdv trade_2010_thresholded.gw trade_2010_thresholded.out $(THREADS)


#############################################
###########GENERATE RANDOM NETS##############

gen_trade:
	cd graphcrunch101 && ./crunch -F ../trade_2010.gw -m "er er_dd geo sf sticky" -n 30 -o trade_2010.tsv

## processed all the .gw networks from /code/ .. don't put any unnecessary ones there
gen_all:
	ls *.gw | xargs -i graphcrunch101/crunch -F {} -m "er er_dd geo sf sticky" -n 30

# 0 - hsa metabolic
# 1 - human_ppi
# 2 - trade_2010_thresholded

egdvs_rnd_all:
	echo "0,1,2" | xargs -d, -L 1 ./genAvgEgdvRndNets egdvs

avg_rnd_all:
	echo "0,1,2" | xargs -d, -L 1 ./genAvgEgdvRndNets avg

spreads_rnd_all:
	echo "0,1,2" | xargs -d, -L 1 ./genAvgEgdvRndNets spreads

spreads_metabolic:
	echo "0" | xargs -d, -L 1 ./genAvgEgdvRndNets spreads

egdvs_rnd_all:
	echo "0" | xargs -d, -L 1 ./genAvgEgdvRndNets pears_dist	
	

gcv_dist:
	python gcv_dist.py final_results/$(NET)/$(NET)_spreads.data final_results/$(NET)/$(NET)_avg_gcv.dist

#############################################
###########EGDV RANDOM NETS##################

## calculates all the EGDVS for TRADE_THRESHOLDED GEO
egdv_trade_thresh_geo_all:
	find model_nets_rand_generated -name "*trade_2010_thresholded-geo*" | xargs -i ./e_gdv {}/graph.gw {}/edgvs.res 2

egdv_human_er:
	./e_gdv model_nets_rand_generated/human_ppi-er-1.gw human_ppi_er-1.out $(THREADS)
	
egdv_human_er_dd:
	./e_gdv model_nets_rand_generated/human_ppi-er_dd-1.gw human_ppi_er_dd-1.out $(THREADS)

egdv_human_geo:
	./e_gdv model_nets_rand_generated/human_ppi-geo-1.gw human_ppi_geo-1.out $(THREADS)
	
egdv_human_sf:
	./e_gdv model_nets_rand_generated/human_ppi-sf-1.gw human_ppi_sf-1.out $(THREADS)
	
egdv_human_sticky:
	./e_gdv model_nets_rand_generated/human_ppi-sticky-1.gw human_ppi_sticky-1.out $(THREADS)
	
egdv_metabolic_er:
	./e_gdv model_nets_rand_generated/hsa_metabolic_network-er-1.gw hsa_metabolic_er-1.out $(THREADS)
	
egdv_metabolic_er_dd:
	./e_gdv model_nets_rand_generated/hsa_metabolic_network-er_dd-1.gw hsa_metabolic_er_dd-1.out $(THREADS)
	
egdv_metabolic_geo:
	./e_gdv model_nets_rand_generated/hsa_metabolic_network-geo-1.gw hsa_metabolic_geo-1.out $(THREADS)
	
egdv_metabolic_sf:
	./e_gdv model_nets_rand_generated/hsa_metabolic_network-sf-1.gw hsa_metabolic_sf-1.out $(THREADS)
	
egdv_metabolic_sticky:
	./e_gdv model_nets_rand_generated/hsa_metabolic_network-sticky-1.gw hsa_metabolic_sticky-1.out $(THREADS)


	
#############################################
##############  AVG-EGDV  ###################

avg_small1:
	./avg_gdv small_network_1.out.egdvs

avg_human_ppi_full:
	./avg_gdv final_results/human_ppi.out.egdvs
	
avg_metabolic_full:
	./avg_gdv final_results/hsa_metabolic_network.out.egdvs

#AVG-EGDV RANDOM NETS

avg_metabolic_er:
	./avg_gdv final_results/hsa_metabolic_er-1.out.egdvs > final_results/hsa_metabolic_er-1.avg
	
avg_metabolic_er_dd:
	./avg_gdv final_results/hsa_metabolic_er_dd-1.out.egdvs > final_results/hsa_metabolic_er_dd-1.avg
	
avg_metabolic_geo:
	./avg_gdv final_results/hsa_metabolic_geo-1.out.egdvs > final_results/hsa_metabolic_geo-1.avg
	
avg_metabolic_sf:
	./avg_gdv final_results/hsa_metabolic_sf-1.out.egdvs > final_results/hsa_metabolic_sf-1.avg
	
avg_metabolic_sticky:
	./avg_gdv final_results/hsa_metabolic_sticky-1.out.egdvs > final_results/hsa_metabolic_sticky-1.avg
	
avg_human_er:
	./avg_gdv final_results/human_ppi_er-1.out.egdvs > final_results/human_ppi_er-1.avg
	
avg_human_er_dd:
	./avg_gdv final_results/human_ppi_er_dd-1.out.egdvs > final_results/human_ppi_er_dd-1.avg
	
avg_human_geo:
	./avg_gdv final_results/human_ppi_geo-1.out.egdvs > final_results/human_ppi_geo-1.avg
	
avg_human_sf:
	./avg_gdv final_results/human_ppi_sf-1.out.egdvs > final_results/human_ppi_sf-1.avg
	
avg_human_sticky:
	./avg_gdv final_results/human_ppi_sticky-1.out.egdvs > final_results/human_ppi_sticky-1.avg
	


#Clean-up stuff, and debugging commands
clean:
	rm *.out*

gdb_avg_small1:
	make g++_gdb && gdb --args avg_gdv small_network_1.out.egdvs

gdb_human_full:
	make g++_gdb && gdb --args e_gdv human_ppi.gw human_ppi.out 1
	
gdb_human_small:
	make g++_gdb && gdb --args e_gdv human_ppi_small.gw human_ppi_small_egdv.out 1

gdb_small:
	make g++_gdb && gdb --args e_gdv small_network_1.gw small_network_1.out 1

valgrind:
	valgrind -v ./e_gdv small_nets/human_ppi_small.gw small_nets/human_ppi_small_egdv.out 1
	
vim:
	vim -O genAvgEgdvRndNets.cpp e_gdv.cpp
