#include "utils.cpp"
#include <stdio.h>      /* printf */
#include <stdlib.h>     /* system, NULL, EXIT_FAILURE */
#include <unistd.h>
#include <string.h>
#include "algo_utils.cpp"


void genEGDVs(int netType);
void genAvgEGDV(int netType);
struct spread_res calcSpreads(double*** avg_egdvs);
void printSpreads(struct spread_res, int netType);


const char* FOLDER = "model_nets_rand_generated";

const char* NETWORKS[] = {"hsa_metabolic_network", "human_ppi", "trade_2010_thresholded"};

const char* TYPES[] = {"er", "er_dd", "geo", "sf", "sticky"};

int NR_RAND_NETS = 30;
//int NR_RAND_NETS = 1;
int RAND_NET_TYPES = 5;
int NR_THREADS = 2;

int msInSec = 1000000;


struct spread_res{
  double** avg;
  double** spreads;
};


void genPearsDist(int netType)
{

  char* source = new char[200];
  char* dest = new char[200];
  char* command = new char[2000];

  //int DIST_MAT_LEN = NR_RAND_NETS * RAND_NET_TYPES;

  //float** dist_matrix = new float*[DIST_MAT_LEN];

    for(int randType = 0; randType < RAND_NET_TYPES; randType++)
      for(int randNetNr = 1; randNetNr <= NR_RAND_NETS; randNetNr++)
      {
      sprintf(source, "%s/%s/models/%s/%s-%s-%d/gcv_list.ndump2", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr);
      sprintf(dest, "%s/%s/models/%s/%s-%s-%d/pearsons_matrix.data", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr);
      sprintf(command, "./pears_coeff %s %s test_matrix 0", source, dest);
      printf("\n Running: %s", command);
      int res = system(command);
      //usleep(10 * msInSec);   //1000 microseconds in a millisecond.
      }



}


void genEGDVs(int netType)
{

  char* source = new char[200];
  char* dest = new char[200];
  char* command = new char[2000];

    for(int randType = 0; randType < RAND_NET_TYPES; randType++)
      for(int randNetNr = 1; randNetNr <= NR_RAND_NETS; randNetNr++)
      {
      sprintf(source, "%s/%s/models/%s/%s-%s-%d/graph.gw", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr);
      sprintf(dest, "%s/%s/models/%s/%s-%s-%d/gcv_list", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr);
      sprintf(command, "./e_gdv %s %s %d 0", source, dest, NR_THREADS);
      printf("\n Running: %s", command);
      int res = system(command);
      //usleep(10 * msInSec);   //1000 microseconds in a millisecond.
      }

}

void genAvgEGDV(int netType)
{

  char* source = new char[200];
  char* dest = new char[200];
  char* command = new char[2000];

    for(int randType = 0; randType < RAND_NET_TYPES; randType++)
      for(int randNetNr = 1; randNetNr <= NR_RAND_NETS; randNetNr++)
      {
      sprintf(source, "%s/%s/models/%s/%s-%s-%d/edgvs.res.egdvs", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr);
      sprintf(dest, "%s/%s/models/%s/%s-%s-%d/avg_egdv.res", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr);
      sprintf(command, "./avg_gdv %s > %s", source, dest);
      printf("\n Running: %s", command);
      int res = system(command);
      //usleep(10 * msInSec);   //1000 microseconds in a millisecond.
      }
}

struct spread_res calcSpreads(double*** avg_egdvs)
{

  /* the average of the avg_egdv across the 30 generated networks. We should get a GDV for each random type: ER, ER-DD, SF, GEO .. */
  double** avg = new double*[RAND_NET_TYPES];
  /* the standard deviation of the average GCVs for all the generated networks, by type*/
  double** spreads = new double*[RAND_NET_TYPES];

  double* tmp_egdv = new double[NR_GRAPHLETS];
  
  /* first calculate the average vector */
  for(int randType = 0; randType < RAND_NET_TYPES; randType++)
  {
    avg[randType] = new double[NR_GRAPHLETS];
    zero_egdv_d(avg[randType]);
    for(int randNetNr = 0; randNetNr < NR_RAND_NETS; randNetNr++)
    {
      add_vectors_d(avg[randType], avg_egdvs[randType][randNetNr]);
    }
    divide_egdv_by_scalar(avg[randType], (double) NR_RAND_NETS);
  }

  /* then compute the standard deviation*/
  for(int randType = 0; randType < RAND_NET_TYPES; randType++)
  {
    spreads[randType] = new double[NR_GRAPHLETS];
    zero_egdv_d(spreads[randType]);
    for(int randNetNr = 0; randNetNr < NR_RAND_NETS; randNetNr++)
    {
      zero_egdv_d(tmp_egdv);
      add_vectors_d(tmp_egdv, avg_egdvs[randType][randNetNr]);
      subtract_vectors_d(tmp_egdv, avg[randType]);
      raise_vect_to_power_d(tmp_egdv, 2.0);
      add_vectors_d(spreads[randType], tmp_egdv);
    }
  
    #if DEBUG
    if(randType == 4)
    {
      for(int i = 0; i < NR_RAND_NETS; i++)
      {
        printf("G10  %f\n", avg_egdvs[randType][i][9]);
      }      

      printf("spread so far G10 %f\n", spreads[randType][9]);
      printf("testing pow(2,0.5) %f\n", pow(2,0.5));
    }   
    #endif

    // divide by N-1 (unbiased estimator) and then take sqrt
    divide_egdv_by_scalar(spreads[randType], (double) NR_RAND_NETS - 1);
    raise_vect_to_power_d(spreads[randType], 0.5);
  }
  struct spread_res results;
  results.avg = avg;
  results.spreads = spreads;
  
  return results;
}

double*** parseAvg(int netType)
{
  FILE* in;
  char srcFile[200];
  int node_nr;
  double*** avg_egdvs = new double**[RAND_NET_TYPES]; 
  char tmp_str[10];
  int tmp_res;
  char tmp_buffer[200];
  char* tmp_buffer2;
 
  for(int randType = 0; randType < RAND_NET_TYPES; randType++)
  {
    avg_egdvs[randType] = new double*[NR_RAND_NETS];
    for(int randNetNr = 0; randNetNr < NR_RAND_NETS; randNetNr++)
    {
      avg_egdvs[randType][randNetNr] = new double[NR_GRAPHLETS];
      sprintf(srcFile, "%s/%s/models/%s/%s-%s-%d/avg_egdv.res", FOLDER, NETWORKS[netType], TYPES[randType], NETWORKS[netType], TYPES[randType], randNetNr+1);
    
      
      in  = fopen(srcFile, "r");

      if(in == NULL)
      {
        printf("Could not find file %s", srcFile);
        return NULL;
      }

      // skip the first 3 lines
      tmp_buffer2 = fgets(tmp_buffer, 200, in);
      tmp_buffer2 = fgets(tmp_buffer, 200, in);
      tmp_buffer2 = fgets(tmp_buffer, 200, in);

      tmp_res = fscanf(in, "\nNode %d\n\n", &node_nr); 

      for (int i = 0; i < NR_GRAPHLETS; i++)
      {
        tmp_res = fscanf(in, "%s\t%lf", tmp_str, &avg_egdvs[randType][randNetNr][i]);

        if (!tmp_res)
        {
          printf("Error while parsing the file");
          return NULL;
        }  
      }  
      fclose(in);
    }
  }   

  return avg_egdvs;
}

void writeSpreadsToOutFile(FILE* out, struct spread_res res, double* avg_egdv_real_net, int netType)
{
  double** avg_avg_egdv = res.avg;
  double** spreads = res.spreads;
  
  fprintf(out, "#Average network GCVs and the spreads for the %s network.", NETWORKS[netType]);
  fprintf(out, "\n# graphlet nr <ER_AVG> <ER_SPREADS> <ER_DD_AVG> <ER_DD_SPREADS> ..  GEO SF STICKY REAL_NET_AVG\n");

  for(int graphletNr = 0; graphletNr < NR_GRAPHLETS; graphletNr++)
  {
    fprintf(out, "\n%d ", graphletNr);
    for(int randType = 0; randType < RAND_NET_TYPES; randType++)
    {
      fprintf(out, "%f ", avg_avg_egdv[randType][graphletNr]);
      fprintf(out, "%f ", spreads[randType][graphletNr]);
    }
    fprintf(out, "%f", avg_egdv_real_net[graphletNr]);
  }

}

void printSpreads(struct spread_res res, int netType)
{
  double** avg_avg_egdv = res.avg;
  double** spreads = res.spreads;
  for(int randType = 0; randType < RAND_NET_TYPES; randType++)
  {
    printf("\nAverage GCVs %s-%s\n\n", NETWORKS[netType], TYPES[randType]);
    write_egdv_to_file_no_header_d(stdout, avg_avg_egdv[randType]);
    printf("\n\nStandard deviations per graphlet %s-%s\n\n", NETWORKS[netType], TYPES[randType]);
    write_egdv_to_file_no_header_d(stdout, spreads[randType]);
  }

}

int main(int argc, char** argv)
{
  if(argc != 3)
  {
    printf("Error parsing arguments. Usage: ./genAvgEgdvRndNets <egdvs/avg/spreads> <netType> ... Instead, you used %d parameters\n", argc);
    printf("Command run: ");
    for(int i = 0; i < argc; i++)
      printf("%s ", argv[i]);
  }
  else
  {  
    int netType = atoi(argv[2]);
    if(!strcmp(argv[1],"egdvs"))
      genEGDVs(netType);
    else if(!strcmp(argv[1],"avg"))
      genAvgEGDV(netType);
    else if(!strcmp(argv[1],"spreads"))
    {
      double*** avg_egdvs = parseAvg(netType);
      struct spread_res res = calcSpreads(avg_egdvs);
      //printSpreads(res, netType);
      char outFileName[300];
      sprintf(outFileName, "model_nets_rand_generated/%s_spreads.data", NETWORKS[netType]);
      FILE* out = fopen(outFileName,"w");
      //FILE* out = stdout;
      if(out == NULL)
      {
        printf("Error: File %s could not be opened", outFileName);
        return 0;
      }
    
      char real_net_file[300];
      sprintf(real_net_file, "final_results/%s/%s.ndump2", NETWORKS[netType], NETWORKS[netType]);
      double* avg_egdv_real_net = calc_avg_from_file_ndump(real_net_file);
      normalize_egdv(avg_egdv_real_net);

      writeSpreadsToOutFile(out, res, avg_egdv_real_net, netType);
    }
    else if(!strcmp(argv[1],"pears_dist"))
      genPearsDist(netType);

    else
      printf("usage: ./genAvgEgdvRndNets.cpp <egdvs/avg/spreads>");
  }

  return 0;
}
