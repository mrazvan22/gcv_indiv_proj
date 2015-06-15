/* script that calculates a 30x30 matrix of pearson's sample correlation coefficients 
for a given network. Entry C(i,j) of the matrix is the correlation coeffciient 
between the vertical vector of graphlets Gi and Gj from the network. 

Node | G1 G2 G3 ... G30
1    | 2  4  1  ...    
2    | 3  2  6  ...    
3    | 9  4  2  ...    
4    | 0  4  9  ...    
5    | 2  2  6  ...    
6    | 2  4  7  ...    
...
...

*/

#include <list>
#include "utils.cpp"
#include "algo_utils_gdv.cpp"
#include <cmath>
#include <string.h>
#include <math.h>


std::list<double*>* parse_egdv_file(char* filename)
{
  FILE* in = fopen(filename, "r");
  if(!in)
    printf("Could not open file %s", filename);

  int node_nr;
  std::list<double*>* egdvs = new std::list<double*>;
  
  double* tmp_egdv; 
  char tmp_str[30];
  int tmp_res;
  int64 tmp_int;    

  while(!feof(in))
  {
    tmp_res = fscanf(in, "\nNode %d\n\n", &node_nr); 
    if(feof(in))
      break;

    tmp_egdv = new double[NR_GRAPHLETS_GDV];    

    for (int i = 0; i < NR_GRAPHLETS_GDV; i++)
    {
      tmp_res = fscanf(in, "%s\t%lld", tmp_str, &tmp_int);
      tmp_egdv[i] = (double) tmp_int;   

      if (!tmp_res)
      {
        printf("Error while parsing the file");
        return NULL;
      }  
    }

    egdvs->push_back(tmp_egdv);
  
  }
  
  fclose(in);
  
  return egdvs;
}


std::list<double*>* parse_ndump_file(char* filename)
{
  FILE* in = fopen(filename, "r");
  if(!in)
    printf("Could not open file %s", filename);

  int node_nr;
  std::list<double*>* egdvs = new std::list<double*>;
  
  double* tmp_egdv; 
  char tmp_str[30];
  int tmp_res;

  while(!feof(in))
  {
    tmp_res = fscanf(in, "%s", tmp_str); 
    if(feof(in))
      break;

    tmp_egdv = new double[NR_GRAPHLETS_GDV];    

    for (int i = 0; i < NR_GRAPHLETS_GDV; i++)
    {
      tmp_res = fscanf(in, "%lf", &tmp_egdv[i]);

      if (!tmp_res)
      {
        printf("Error while parsing the file");
        return NULL;
      }  
    }

    egdvs->push_back(tmp_egdv);
  
  }
  
  fclose(in);
  
  return egdvs;
}




double** calc_pears_matrix(std::list<double*>* egdvs, double* avg_egdv)
{
  double** pears_matrix = new double*[NR_GRAPHLETS_GDV];

  std::list<double*>::const_iterator egdv_it;
  double* egdv;

  /* pearson's coeff r = upperSum/ (sqrt (lowerSumX) * sqrt (lowerSumY)) */
  double upperSum, lowerSumX, lowerSumY;

  #if DEBUG
  int c = 0;  
  #endif

  printf("\nsize of egdv list: %d\n", egdvs->size());

  for(int i = 0; i < NR_GRAPHLETS_GDV; i++)
  {
    pears_matrix[i] = new double[NR_GRAPHLETS_GDV];
    for(int j = 0; j < NR_GRAPHLETS_GDV; j++)
    {
      upperSum = 0;
      lowerSumX = 0;
      lowerSumY = 0;
      for(egdv_it = egdvs->begin(); egdv_it != egdvs->end(); egdv_it++)
      {
        egdv = *egdv_it;
        upperSum += (egdv[i] - avg_egdv[i]) * ( egdv[j] - avg_egdv[j]);
        lowerSumX += pow((egdv[i] - avg_egdv[i]),2);
        lowerSumY += pow((egdv[j] - avg_egdv[j]),2);
        
        #if DEBUG
        if(i == 0 && j == 1)
        {
          printf("egdv[i]=%f   egdv[j]=%f\n", egdv[i], egdv[j]);        
          printf("upperTerm=%f\n",(egdv[i] - avg_egdv[i]) * ( egdv[j] - avg_egdv[j]));        
          printf("lowerTermX=%f\n", pow((egdv[i] - avg_egdv[i]),2));        
          printf("lowerTermY=%f\n", pow((egdv[j] - avg_egdv[j]),2));        
        }
        #endif

        #if DEBUG
        c++;
        if(c%500 == 0)
        {
          printf("egdv_it:%d   egdv[i]:%f   avg[i]:%f  egdv[j]:%f   avg[j]:%f\n", egdv_it,  egdv[i], avg_egdv[i], egdv[j], avg_egdv[j]);
          printf("Iterating for elements: (%d,%d)", i, j);
        }
        #endif
      }     
      #if DEBUG
      if(i == 0 && j == 1)
      {
        printf("avg_egdv[i]=%f   avg_egdv[j] = %f\n", avg_egdv[i], avg_egdv[j] );
        printf("upper Sum %f\n", upperSum);
        printf("lowerSumX %f\n", lowerSumX);
        printf("lowerSumY %f\n", lowerSumY);
      }
      #endif       

      if(lowerSumX * lowerSumY != 0)
        pears_matrix[i][j] = upperSum/ (sqrt (lowerSumX) * sqrt (lowerSumY));
      else
        pears_matrix[i][j] = 0;
        

    }
  }  
  

  return pears_matrix;
}

void write_matrix_to_file(double** pears_matrix, char* filename)
{
  
  FILE* out;
  if(!strcmp(filename,"stdout"))
    out = stdout;
  else    
    out = fopen(filename, "w");
  
  if(out == NULL)
  {
    printf("Error opening file %s", filename);
    return;
  }

  for(int i = 0; i < NR_GRAPHLETS_GDV; i++)
  {  
    for(int j = 0; j < NR_GRAPHLETS_GDV; j++)
      fprintf(out, "%f ", pears_matrix[i][j]);  
  
    fprintf(out, "\n");
  }
  
  fclose(out);

}

/* Every element is rescaled according to where it lies in the (min, max) interval */
double** normalize_matrix(double** pears_matrix)
{
  /* max is always 1 because of diagonal elements*/
  double max = 1;

  double min = 1;
  for(int i = 0; i < NR_GRAPHLETS_GDV; i++)
    for(int j = 0; j < NR_GRAPHLETS_GDV; j++)
      if(min > pears_matrix[i][j])
        min = pears_matrix[i][j];

  #if DEBUG2
  printf("min=%f\n", min);  
  #endif

  for(int i = 0; i < NR_GRAPHLETS_GDV; i++)
    for(int j = 0; j < NR_GRAPHLETS_GDV; j++)
      pears_matrix[i][j] = (pears_matrix[i][j] - min)/(max - min);

  return pears_matrix;
}

/* uses a polynomial function to further normalize the pearsons correlation matrix */
double** normalize_polynomial(double** pears_matrix, double power)
{
  double** final_matrix = new double*[NR_GRAPHLETS_GDV];

  for(int i = 0; i < NR_GRAPHLETS_GDV; i++)
  {
    final_matrix[i] = new double[NR_GRAPHLETS_GDV];
  
    for(int j = 0; j < NR_GRAPHLETS_GDV; j++)
      final_matrix[i][j] = pow(pears_matrix[i][j], power) ;
  }

  return final_matrix;
}

int main(int argc, char** argv)
{
  if(argc != 5)
    printf("Error .. Usage: ./pears_coeff <input_network_egdvs> <out_file> <out_file_normalized> <norm_type>");
  
  char* in_filepath = argv[1];
  char* out_filepath = argv[2];
  char* out_filepath_norm = argv[3];


  std::list<double*>* egdvs = parse_ndump_file(in_filepath); 

  double* avg_egdv = calc_avg_from_file_ndump(in_filepath);
  
  double** pears_matrix = calc_pears_matrix(egdvs, avg_egdv);
  write_matrix_to_file(pears_matrix, out_filepath);

  pears_matrix = normalize_matrix(pears_matrix);
  write_matrix_to_file(pears_matrix, out_filepath_norm);
  
  char out_path_norm_poly[300];

  int NR_OF_NORMALISATIONS = 1;

  double*** norm_matrices = new double**[NR_OF_NORMALISATIONS];
  
  char* out_path_norm_poly_prefix = strtok(out_filepath_norm, ".");
  
  int norm_type = atoi(argv[4]);

  if(norm_type == 0)
  {
    for(int i = 2; i < NR_OF_NORMALISATIONS; i++)
    {
      sprintf(out_path_norm_poly, "%s-poly-%d.data", out_path_norm_poly_prefix, i);
      printf("Writing matrix file: %s\n", out_path_norm_poly);
      norm_matrices[i] = normalize_polynomial(pears_matrix, (double) i);
      write_matrix_to_file(norm_matrices[i] , out_path_norm_poly);
    }
  }
 
  if(norm_type == 1)
  {
    for(int i = 2; i < NR_OF_NORMALISATIONS; i++)
    {
      sprintf(out_path_norm_poly, "%s-poly-%d.data", out_path_norm_poly_prefix, i);
      printf("Writing matrix file: %s\n", out_path_norm_poly);
      norm_matrices[i] = normalize_polynomial(pears_matrix, 1.0/ (2 * i));
      write_matrix_to_file(norm_matrices[i] , out_path_norm_poly);
    }
  }
 
}
