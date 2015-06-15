// SYNOPSYS: ./e_gdv <input_net.gw> <output_file> <nr_threads> <norm_type/nothing>

#include "ncount_new_gdv.cpp" 
#include "utils.cpp" 
#include "algo_utils.cpp"
#include <time.h> 
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/wait.h>


#define NDUMP_MODE 1

int NORM_TYPE = 0;
/* 
 0 - no normalisation
 1 - normalised so that the vector elements sum to 1
*/

/* defines how many node egdvs to skip for printing. If value is 10, then it 
   will print once every 10 nodes. If debugging small graphs, set this to 1. */


/* function declarations */
void compute_egdv_all_nodes(struct graph graph_res, FILE* out);
int calc_egdv_each_node(int argc, char *argv[]);


/* --------------------------------------- */

/* given a graph struct, computes the E-GDV for each node and writes them to file FILE.

   For calculating the E-GDV for one node N, we take the neighbouring set of 
   N and compute how many of each graphlet types are found in that neighbouring 
   set. 

   The neighbouring set does not include the node N itself, and is an 
   induced subgraph of the whole_graph. Furthermore, we have carefully decided 
   not to normalize the results, because that wouldn't add any value to the 
   E-GDV metric */
void compute_egdv_all_nodes(struct graph graph_res, FILE* out, 
                            int proc_index, int nr_proc)
{

  
  // get graph variables from the input structure
  char** adjmat = graph_res.adjmat; 
  int** edges_for = graph_res.edges_for;
  int* edges = graph_res.edges;
  int V = graph_res.V;
  int E = graph_res.E; 
  int E_undir = graph_res.E_undir;
  char** node_names = graph_res.node_names;

  // allocate space for the extended gdv and for the neighbour graph
  int64* egdv; //= new int64[29];
  struct graph neighbours_graph;

  #if DEBUG
  printf("Initial graph structure\n\n");
  //print_graph_struct(graph_res);
  #endif

  //multi-core logic
  int min = (V/nr_proc) * proc_index;
  int max = (V/nr_proc) * (proc_index + 1);
 
  /* fix for the precision loss in max. 
     if last process, then calculate until the end */
  if (proc_index == nr_proc - 1)
  {
    max = V;
  }
 
  //initialise sum of egdv's to 0s
  int64 egdv_sum[NR_GRAPHLETS];
  zero_egdv(egdv_sum);
  int64 tmp_zero_egdv[NR_GRAPHLETS];
  zero_egdv(tmp_zero_egdv);  
  double tmp_zero_egdv_d[NR_GRAPHLETS];
  zero_egdv_d(tmp_zero_egdv_d);  

  //printf("Starting the count\n\n");

  // start timing
  time_t start_time = time(0);
  for (int v = min; v < max; v++) // for each vertex in the big graph
  {
  /* v is a vertex from the big graph, iteration will be 1, 2, 7, 8, 3, 4, .. */
    #if PROGRESS_INFO_EGDV
    fprintf(stderr, "\rnode # %5d (%.1f%%) [%ld min elapsed]", v, 
              100.0 * (float) (v - min) / (max - min), (time(0) - start_time) / 60);
    #endif

    neighbours_graph.V = edges_for[v+1] - edges_for[v];

    //if the node only has one or zero neighbours, print zero vector and continue to next iteration  
    if(neighbours_graph.V <= 1)
    {
      #if DEBUG
      printf("  Node %d has One or Zero neighbours!\n", v);
      #endif
      
      if(NDUMP_MODE)
      {
        if(NORM_TYPE == 0)
        {
          write_egdv_ndump(out, tmp_zero_egdv, node_names[v]);
        }
        else
        {
          write_egdv_ndump_d(out, tmp_zero_egdv_d, node_names[v]);
        }
      }
      else
      {
        /* but still print the zero vector, if the STEP_SIZE is good this round */
        print_conditional_zero_vector(out, v);
      }
      continue;
    }

    /* allocate some space for the adjacency matrix */
    neighbours_graph.adjmat = new char*[V]; 
    /* Use a bit vector to store each row of the adjancency matrix, so
     * that each edge takes up only one bit.
     */
   for(int i = 0; i < neighbours_graph.V; i++)
    {
        /* calloc zeroes the memory for us */
        neighbours_graph.adjmat[i] = (char *) calloc(neighbours_graph.V/8+1, sizeof(char));
        if(!neighbours_graph.adjmat[i]) { perror("calloc"); exit(1); }

        Connect_neighbours(i,i); /* optimization hack */
    }

    /* for each pair (src,dst) of 2 nodes from the neighbour vector list, 
       if they are connected in the big graph, then also connect them in 
       the neighbours_graph */
    int src, dst, nr_edges = 0;
    for(int src_index = 0; src_index < neighbours_graph.V; src_index++)
    {
      src = edges_for[v][src_index];
      for(int dst_index = 0; dst_index < neighbours_graph.V; dst_index++)
      {
        dst = edges_for[v][dst_index];
        
        if(Connected(src, dst))
        {
          Connect_neighbours(src_index, dst_index);
          Connect_neighbours(dst_index, src_index);

          //keep track of how many edges are in the neighbours graph
          nr_edges++;
        }

      }  
    }   
    
    //compute E and E_undir
    neighbours_graph.E = nr_edges - neighbours_graph.V;
    assert(neighbours_graph.E % 2 == 0);
    neighbours_graph.E_undir = neighbours_graph.E / 2;

    //continue to next iteration if there are no edges in the neighbouring set
    if(neighbours_graph.E == 0)
    {
      #if DEBUG
      printf("Neighbouring set for node %d has Zero edges!\n", v);
      #endif
      free_adj_mat(neighbours_graph);

      if(NDUMP_MODE == 1)
      {
        if(NORM_TYPE == 0)
        {
          write_egdv_ndump(out, tmp_zero_egdv, node_names[v]);
        }
        else
        {
          write_egdv_ndump_d(out, tmp_zero_egdv_d, node_names[v]);
        }
      }
      else
      {
        /* but still print the zero vector, if the STEP_SIZE is good this round */
        print_conditional_zero_vector(out, v);
      }
      
      continue;
    }

    assert(out);
    /* allocate space for the adjacency lists of edges. 
  
       edges is a sequential list of all the edges in the graph, such that after 
       the last edge of node N follows the first edge of node N+1. */
    neighbours_graph.edges     = new int [neighbours_graph.E];
    /* edges_for contains pointers in the edges arrray. edges_for[v][k] returns 
       k-th edge for vertex v. */
    neighbours_graph.edges_for = new int*[neighbours_graph.V + 1];

    //edge_last iterates over the edges vector and is used to set the boundaries
    int* edge_last = &neighbours_graph.edges[0];
  
    int i = 0;
    for(i = 0; i < neighbours_graph.V; i++)
    {
      neighbours_graph.edges_for[i] = edge_last;
      for(int j = 0; j < neighbours_graph.V; j++)
      {
        if( i != j && Connected_neighbours(i,j))
        {
          *edge_last = j;
          edge_last++;      
        }  
      }
    }

    #if DEBUG
    assert(out);
    printf("\ni:%d\n", i);
    #endif

    neighbours_graph.edges_for[i] = edge_last;

    #if DEBUG
    //print_graph_struct(neighbours_graph);
    printf("Running count_graphlets");
    #endif
    
    egdv = count_graphlets(neighbours_graph); 
    free_graph_struct(neighbours_graph);

    //add the egdv to the egdv_sum
    add_vectors(egdv_sum, egdv);

    if(NDUMP_MODE == 1)
    {
      if(NORM_TYPE == 0)
      {
        write_egdv_ndump(out, egdv, node_names[v]);
      }
      else if(NORM_TYPE == 1)
      {
        double* norm_egdv = normalize_egdv_int(egdv);
        write_egdv_ndump_d(out, norm_egdv, node_names[v]);
      } 
    }
    else
    {
      write_egdv_node_to_file(out, egdv, v);  
    }    

    #if DEBUG
    printf("Test <4>");
    #endif

    delete[] egdv;
  } 

}


/* sets up the threads that will compute the egdv for each node. */
int calc_egdv_each_node(int argc, char *argv[])
{
    if(argc != 4 && argc != 5)
    {
        fprintf(stderr, "Usage: %s <input_graph.gw> <output_file> <rn_threads> <norm_type/nothing>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if(!fp) { perror(argv[1]); return 1; }

    if (argc == 5)
    {
      NORM_TYPE = atoi(argv[4]);
    }
   
    // parse LEDA file and return the graph struct
    struct graph graph_res = parse_leda_file(fp);
     
    /* first count the nr of graphlets in the whole graph 
       (i.e. the network GDV) */ 
    #if COUNT_WHOLE_GRAPH
    int64* init_graphlet_count = count_graphlets(graph_res);
    fprintf(out, "Initial graph\n");
    write_gdv_to_file(out, init_graphlet_count);
    delete[] init_graphlet_count;
    #endif    
    
    int nr_procs = 1;

    if (argv[3] != NULL )
      nr_procs = atoi( argv[3] );

    char* out_base_file_name = argv[2];

    int pids[nr_procs];

    for (int proc_index = 0; proc_index < nr_procs; proc_index++)
    {
      pids[proc_index] = fork();
      if (pids[proc_index] == 0)
      {  
        char nr_str[7];
        sprintf(nr_str, ".0%03d", proc_index);
        char* out = (char*) malloc(strlen(out_base_file_name) + 10);
        strcpy(out, out_base_file_name);
        strcat(out, nr_str);
        //printf("outFileName:%s\n", out); 
        
        FILE* fp_out = fopen(out, "w");
        /* count the nr of graphlets in the graph and return them in an 
           integer array dumps some egdvs to file on the way */
        compute_egdv_all_nodes(graph_res, fp_out, proc_index, nr_procs);


        fclose(fp_out);
        free(out);
        return 0;
      }
      
    }

    int status;

    printf("Waiting on the children ...");
    for (int proc_index = 0; proc_index < nr_procs; proc_index++)
      waitpid(pids[proc_index], &status, 0);

    printf("Children have finished processing. Assembling the files...");

    
    char concat_command[2000];
    char extension[20];
  
    if(NDUMP_MODE)
    {
      sprintf(extension, "ndump2");
    }
    else
    {
      sprintf(extension, "egdvs");
    }

    sprintf(concat_command, "cat %s.0* > %s.%s;rm %s.0*", out_base_file_name, out_base_file_name, extension, out_base_file_name);
    printf("Running: %s", concat_command);
    int sys_res = system(concat_command);

    //free allocated memory for graph edges and gcount
    free_graph_struct(graph_res);
  
   //for(int i = 0; i < graph.V; i++)
   //  free(graph.node_names[i]);
 
   delete[] graph_res.node_names;

    fclose(fp);

    return 0;
}

// SYNOPSYS: ./e_gdv <input_net.gw> <output_file.out> <nr_threads>
int main(int argc, char** argv)
{
  return calc_egdv_each_node(argc, argv);
}
