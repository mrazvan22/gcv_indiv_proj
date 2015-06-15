#include "utils.cpp" 
#include "algo_utils.cpp"


/* normalises the egdv so that the elements sum to 1 */
double* normalise_egdv(double* sum_egdv)
{
  double sum_graphlets = 0;
  double* avg_egdv = new double[NR_GRAPHLETS];

  for(int i = 0; i < NR_GRAPHLETS; i++)
    sum_graphlets += sum_egdv[i];

  if(sum_graphlets != 0)
  {
    for(int i = 0; i < NR_GRAPHLETS; i++)
      avg_egdv[i] =  sum_egdv[i] / sum_graphlets;
  }
  else
  {
    zero_egdv_d(avg_egdv); 
  } 

  return avg_egdv;
}

// SYNOPSYS:   ./avg_gdv <input_file_name> 
int main(int argc, char** argv)
{
  printf("Processing file %s", argv[1]);
  double* sum_egdv = compute_sum_egdv_ndump(argv[1]);

  double* avg_egdv = normalise_egdv(sum_egdv);

  printf("\nNormalised GDV:\n");
  write_egdv_node_to_stdout_double(avg_egdv, 0);
  printf("\nGDV SUM:\n");
  write_egdv_node_to_stdout_double(sum_egdv, 0);

  delete[] sum_egdv;
  delete[] avg_egdv;
  

  return 0;

}
