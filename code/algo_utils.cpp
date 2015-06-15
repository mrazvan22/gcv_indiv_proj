#ifndef ALGO_UTILS
#define ALGO_UTILS

int NR_NODES;

/* computes the average E-GDV for the whole network by calculating
   sum first and then normalising so that all entries sum to 1. This
   is useful when comparing networks that are not comparable in size */
int64* compute_sum_egdv_egdvs(char* filename)
{
  FILE* in = fopen(filename, "r");
  int node_nr;
  int64* sum_egdv = new int64[NR_GRAPHLETS];
  int64 tmp_egdv[NR_GRAPHLETS]; 
  char tmp_str[30];
  int tmp_res;

  zero_egdv(sum_egdv);
  zero_egdv(tmp_egdv);
  
  NR_NODES = 0;
  while(!feof(in))
  {
    tmp_res = fscanf(in, "\nNode %d\n\n", &node_nr); 
    if(feof(in))
      break;
  
    for (int i = 0; i < NR_GRAPHLETS; i++)
    {
      tmp_res = fscanf(in, "%s\t%lld", tmp_str, &tmp_egdv[i]);
    
      if (!tmp_res)
      {
        printf("Error while parsing the file");
        return NULL;
      }  

  
    }
    
    #if DEBUG
    //printf("looping");
    write_egdv_node_to_stdout(tmp_egdv, node_nr);
    #endif

    add_egdv(sum_egdv, tmp_egdv);  
    NR_NODES++;  
  }
  
  printf("Nr of nodes analysed: %d\n", NR_NODES);
  
  fclose(in);
  
  #if DEBUG
  printf("Sum egdv\n");
  for (int i = 0; i < NR_GRAPHLETS; i++)
    printf("%d ", sum_egdv[i]);  
  #endif


  return sum_egdv;
}



/* same as compute_sum_egdv but parses an .ndump2 file instead of .egdvs */
double* compute_sum_egdv_ndump(char* filename)
{
  FILE* in = fopen(filename, "r");
  int node_nr;
  double* sum_egdv = new double[NR_GRAPHLETS];
  double tmp_egdv[NR_GRAPHLETS]; 
  char tmp_str[30];
  int tmp_res;

  zero_egdv_d(sum_egdv);
  zero_egdv_d(tmp_egdv);
  
  NR_NODES = 0;
  while(!feof(in))
  {
    tmp_res = fscanf(in, "%s", tmp_str); 
    if(feof(in))
      break;
  
    for (int i = 0; i < NR_GRAPHLETS; i++)
    {
      tmp_res = fscanf(in, "%lf", &tmp_egdv[i]);
    
      if (!tmp_res)
      {
        printf("Error while parsing the file");
        return NULL;
      }  

  
    }
    
    #if DEBUG
    //printf("looping");
    write_egdv_node_to_stdout(tmp_egdv, node_nr);
    #endif

    add_egdv_d(sum_egdv, tmp_egdv);  
    NR_NODES++;  
  }
  
  printf("Nr of nodes analysed: %d\n", NR_NODES);
  
  fclose(in);
  
  #if DEBUG
  printf("Sum egdv\n");
  for (int i = 0; i < NR_GRAPHLETS; i++)
    printf("%d ", sum_egdv[i]);  
  #endif


  return sum_egdv;
}


/* averages the egdv sum */
double* calc_avg_egdv(double* sum_egdv)
{
  double* avg_egdv = new double[NR_GRAPHLETS];

  if(NR_NODES != 0)
  {
    for(int i = 0; i < NR_GRAPHLETS; i++)
      avg_egdv[i] =  sum_egdv[i] / NR_NODES;
  }
  else
  {
    printf("Error: NR_NODES in avg_gdv.cpp is zero");
    zero_egdv_d(avg_egdv); 
  } 

  return avg_egdv;
}


double* calc_avg_from_file_ndump(char* filename)
{
  return calc_avg_egdv(compute_sum_egdv_ndump(filename));

}

void normalize_egdv(double* egdv)
{
   double sum_graphlets = 0;
 
   for(int i = 0; i < NR_GRAPHLETS; i++)
     sum_graphlets += egdv[i];
 
   if(sum_graphlets != 0)
   {
     for(int i = 0; i < NR_GRAPHLETS; i++)
       egdv[i] = egdv[i] / sum_graphlets;
   }   
   else  
   {
     zero_egdv_d(egdv);
   }     
           
}

double* normalize_egdv_int(int64* egdv)
{
   double sum_graphlets = 0;
   double* norm_egdv = new double[NR_GRAPHLETS];  

   for(int i = 0; i < NR_GRAPHLETS; i++)
     sum_graphlets += egdv[i];
 
   if(sum_graphlets != 0)
   {
     for(int i = 0; i < NR_GRAPHLETS; i++)
       norm_egdv[i] = ((double) egdv[i]) / sum_graphlets;
   }   
   else  
   {
     zero_egdv_d(norm_egdv);
   }     
           
  return norm_egdv;
    
}




#endif
