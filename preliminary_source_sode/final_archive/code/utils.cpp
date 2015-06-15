#ifndef UTILS
#define UTILS

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <cmath>

#define PROGRESS_INFO_EGDV 0
#define NR_GRAPHLETS 29
#define DEBUG 0
#define DEBUG2 0
#define COUNT_WHOLE_GRAPH 0
#define STEP_SIZE 1

#define Connect_neighbours(i,j) (neighbours_graph.adjmat[i][(j)/8] |= 1<<((j)%8))
#define Connected_neighbours(i,j) (neighbours_graph.adjmat[i][(j)/8] & (1<<((j)%8)))



typedef long long int64; // sadly, long long is not standard in C++ ... yet

struct temp_data /* linked list of edges */
{
    struct temp_data *next;
    int dst;
};

struct graph 
{ 
  char** adjmat; 
  int* edges; // stores all the edges sequentially, so the last edge of node n is followed by the first edge of node n+1
  int** edges_for; // it might be that edges_for[i] is a pointer to the first edge of i
  int V; // nr of vertices
  int E; // nr of total edges
  int E_undir; // nr of undirected edges 
  char** node_names; // node labels
};




/* function declarations */
void free_graph_struct(struct graph graph);
void zero_egdv(int64* egdv);
void print_graph_struct(struct graph g);
void free_adj_mat(struct graph graph);
void write_egdv_node_to_file(FILE* out,int64* egdv, int v);  
void print_conditional_zero_vector(FILE* out, int node_nr);
void add_vectors(int64* sum_edgv, int64* new_egdv);
void write_egdv_node_to_file_double(FILE* out, double* egdv, int node_nr);


/* given an output file, a node egdv and node nr, writes them to the file */
void write_egdv_node_to_file(FILE* out, int64* egdv, int node_nr)
{
    /* print graphlet counts */
    assert(out);
    fprintf(out, "\nNode %d\n\n", node_nr);
    for(int g = 0; g < NR_GRAPHLETS; g++)
       fprintf(out, "G%d\t%lld\n", g+1, egdv[g]);
    fflush(out); 
}

/* given an output file, a node egdv and node nr, writes them to the file */
void write_egdv_ndump(FILE* out, int64* egdv, char* node_label)
{
    assert(out);
    fprintf(out, "%s", node_label);
    for(int g = 0; g < NR_GRAPHLETS; g++)
       fprintf(out, " %lld", egdv[g]);
    fprintf(out, "\n");
    fflush(out); 
}


/* given an output file, a node egdv and node nr, writes them to the file */
void write_egdv_ndump_d(FILE* out, double* egdv, char* node_label)
{
    assert(out);
    fprintf(out, "%s", node_label);
    for(int g = 0; g < NR_GRAPHLETS; g++)
       fprintf(out, " %.6f", egdv[g]);
    fprintf(out, "\n");
    fflush(out); 
}

void write_egdv_node_to_stdout( int64* egdv, int node_nr)
{
  write_egdv_node_to_file( stdout, egdv, node_nr);
}

void write_egdv_node_to_stdout_double( double* egdv, int node_nr)
{
  write_egdv_node_to_file_double( stdout, egdv, node_nr);
}

void write_egdv_node_to_file_double(FILE* out, double* egdv, int node_nr)
{
    /* print graphlet counts */
    assert(out);
    fprintf(out, "\nNode %d\n\n", node_nr);
    for(int g = 0; g < NR_GRAPHLETS; g++)
       fprintf(out, "G%d\t%f\n", g+1, egdv[g]);
    fflush(out);
}

void write_egdv_to_file_no_header_d(FILE* out, double* egdv)
{
    /* print graphlet counts */
    assert(out);
    for(int g = 0; g < NR_GRAPHLETS; g++)
       fprintf(out, "G%d\t%f\n", g+1, egdv[g]);
}




/* prints a zero egdv to output file. called when the neighbouring set has 
   zero edges or at most 1 node */
void print_conditional_zero_vector(FILE* out, int node_nr)
{
    assert(out);

    if(node_nr % STEP_SIZE == 0)
    {
      fprintf(out, "\nNode %d\n\n", node_nr);
      for(int g = 0; g < NR_GRAPHLETS; g++)
        fprintf(out, "G%d\t%d\n", g+1, 0);

    }
}

/* sets the values in the egdv back to zero */
void zero_egdv(int64* egdv)
{
  for (int i = 0; i < NR_GRAPHLETS; i++)
    egdv[i] = 0;
}

/* sets the values in the egdv back to zero */
void zero_egdv_d(double* egdv)
{
  for (int i = 0; i < NR_GRAPHLETS; i++)
    egdv[i] = 0.0;
}

/* prints a 2D adjacency matrix to STDOUT */
void print_adjmat(struct graph neighbours_graph)
{
  printf("Adjacency matrix:\n");
  for(int i = 0; i < neighbours_graph.V; i++)
  {
    for(int j = 0; j < neighbours_graph.V; j++)
    {
      if(Connected_neighbours(i,j))
        printf("1 ");
      else
        printf("0 ");
    }
    printf("\n");
  }
}

/* prints the graph structure to STDOUT */
void print_graph_struct(struct graph g)
{
  printf("   Graph Struct: \n V:%d  E:%d  E_undir:%d\n", g.V, g.E, g.E_undir);

  printf("edges:");
  for(int e = 0; e < g.E; e++)
  {
    printf("%d ", g.edges[e]);
  }

  print_adjmat(g);
}

/* frees the memory allocated for the arrays inside a graph structure */
void free_graph_struct(struct graph graph)
{
  delete[] graph.edges;
  delete[] graph.edges_for;
  free_adj_mat(graph);  
  
}

void free_adj_mat(struct graph graph)
{
  for(int i = 0; i < graph.V; i++)
  {
    free(graph.adjmat[i]);
  }

  delete[] graph.adjmat;
}

/* dumps the egdv of all the nodes in the network to a file */
void write_egdv_to_file(FILE* out, int64** egdv, int nr_nodes)
{
  for (int i = 0; i < nr_nodes; i++)
    write_egdv_node_to_file(out, egdv[i], i);
}


void add_vectors(int64* sum_egdv, int64* new_egdv)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    sum_egdv[i] += new_egdv[i];

}

void add_vectors_d(double* sum_egdv, double* new_egdv)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    sum_egdv[i] += new_egdv[i];

}

void subtract_vectors_d(double* dest_egdv, double* new_egdv)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    dest_egdv[i] -= new_egdv[i];

}


void multiply_vector_by_scalar_d(double* egdv, double scalar)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    egdv[i] *= scalar;

}

void raise_vect_to_power_d(double* dest_egdv, double p)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    dest_egdv[i] = pow(dest_egdv[i], p);

}


void add_egdv(int64* dest_egdv, int64* tmp_egdv)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    dest_egdv[i] += tmp_egdv[i];

}

void add_egdv_d(double* dest_egdv, double* tmp_egdv)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    dest_egdv[i] += tmp_egdv[i];
}

void divide_egdv_by_scalar(double* dest_egdv, double scalar)
{
  for(int i = 0; i < NR_GRAPHLETS; i++)
    dest_egdv[i] /= scalar;

}


#endif
