In order to compute a GCV signature using e_gdv.cpp, the first thing to do is to compile all the C++ files using

make

Afterwards, for computing a GCV signature of a network run

./e_gdv <input_net.gw> <output_file> <nr_threads> <normalisation_type>
	
A lot of commands have been written in the Makefile which perform all the experiments. For example, if you need to run the Pearson's GCV life-cycle for the Human metabolic network execute:

make NET=hsa_metabolic_network life-cycle

This will place the GCV list and the ndump files in the generated_results or generated_results_norm1 folders, depending on the NORM_TYPE variable (0 or 1) that is set in the Makefile.

For running the CCA on the trade network using the normalised GCV signature, simply execute:

make canon_trade_lc

However, this command needs the indicator files and the ndump files.

Many other commands defined in the Makefile are used to execute our experiments. See the Makefile for more info

The python scripts from final_results are used for plotting and calculating heatmaps
