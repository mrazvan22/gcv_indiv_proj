#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE MyTest
#include <boost/test/unit_test.hpp>

#include <stdlib.h>
#include <stdio.h>


int add( int i, int j ) { return i+j; }


/* executed command cmd and returns the stdout output as a string */
std::string exec_and_get_output(char* cmd) {
    FILE* pipe = popen(cmd, "r");
    if (!pipe) return "ERROR";
    char buffer[128];
    std::string result = "";
    while(!feof(pipe)) {
      if(fgets(buffer, 128, pipe) != NULL)
        result += buffer;
    }
    pclose(pipe);
    return result;
}

char* convert_to_char_array(std::string str){
  char* out_res_char = new char[200];
  strncpy(out_res_char, str.c_str(), sizeof(out_res_char));
  out_res_char[sizeof(out_res_char) - 1] = 0;

  return out_res_char;
}

// Note that out_file should have no extension
void compare_egdvs(char* net_name, char* in_file, char* out_file, int nr_threads) {

  char command[200];
  sprintf(command, "./e_gdv %s %s %d", in_file, out_file, nr_threads);
  fprintf(stderr, "Running: %s\n", command);
  int res = system(command);  

  char diff_cmd[200];
  char correct_output_file[100];
  sprintf(correct_output_file, "final_results/%s/%s.ndump2",net_name, net_name);
  sprintf(diff_cmd, "diff %s.ndump2 %s", out_file, correct_output_file);
  std::string output_res_str = exec_and_get_output(diff_cmd);

  if(!output_res_str.empty())
  { 
    char boost_error[200];
    sprintf(boost_error, "%s ndump2 files don't match", net_name);
    BOOST_ERROR(boost_error);
    char* char_output = convert_to_char_array(output_res_str);
    printf("%s", char_output);
    free(char_output);
  }  
  else
  {
    printf("\n\nTest successful\n\n");
  }

}


BOOST_AUTO_TEST_SUITE(egdvs)

BOOST_AUTO_TEST_CASE(egdv_human_small) {
  // args
  int nr_threads = 1;
  char in_file[100] = "small_nets/human_ppi_small.gw";
  char out_file[100] = "test_bank/human_ppi_small";
  //

  char command[200];
  sprintf(command, "./e_gdv %s %s %d", in_file, out_file, nr_threads);
  fprintf(stderr, "Running: %s\n", command);
  int res = system(command);  

  char diff_cmd[200];
  char correct_output_file[100] = "final_results/small_nets/human_ppi_small.ndump2";
  sprintf(diff_cmd, "diff %s.ndump2 %s", out_file, correct_output_file);
  fprintf(stderr, "\nComparing files %s %s\n", out_file, correct_output_file);
  std::string output_res_str = exec_and_get_output(diff_cmd);

  if(!output_res_str.empty())
  { 
    BOOST_ERROR("egdv human small ndump2 files don't match");
    char* char_output = convert_to_char_array(output_res_str);
    printf("%s", char_output);
    free(char_output);
  }  
  else
  {
    printf("\n\nTest successful\n\n");
  }

}


BOOST_AUTO_TEST_CASE(human_ppi_egdvs) {

  int nr_threads = 2;
  char net_name[50] = "human_ppi";

  char in_file[100];
  sprintf(in_file, "%s.gw", net_name);

  char out_file[100];
  sprintf(out_file, "test_bank/%s", net_name);
  
  compare_egdvs(net_name, in_file, out_file, nr_threads);

}

BOOST_AUTO_TEST_CASE(hsa_metabolic_egdvs) {

  int nr_threads = 2;
  char net_name[50] = "hsa_metabolic_network";

  char in_file[100];
  sprintf(in_file, "%s.gw", net_name);

  char out_file[100];
  sprintf(out_file, "test_bank/%s", net_name);
  
  compare_egdvs(net_name, in_file, out_file, nr_threads);

}

BOOST_AUTO_TEST_CASE(trade_egdvs) {

  int nr_threads = 2;
  char net_name[50] = "trade_2010_thresholded";

  char in_file[100];
  sprintf(in_file, "%s.gw", net_name);

  char out_file[100];
  sprintf(out_file, "test_bank/%s", net_name);
  
  compare_egdvs(net_name, in_file, out_file, nr_threads);

}

BOOST_AUTO_TEST_CASE(varying_nr_of_threads){
 
  for(int nr_threads = 1; nr_threads <= 32; nr_threads *= 2)
  {
    char net_name[50] = "trade_2010_thresholded";

    char in_file[100];
    sprintf(in_file, "%s.gw", net_name);

    char out_file[100];
    sprintf(out_file, "test_bank/%s", net_name);
  
    compare_egdvs(net_name, in_file, out_file, nr_threads);

  }

}

BOOST_AUTO_TEST_SUITE_END()


BOOST_AUTO_TEST_CASE( my_test )
{
    // seven ways to detect and report the same error:
    BOOST_CHECK( add( 2,2 ) == 4 );        // #1 continues on error

    BOOST_REQUIRE( add( 2,2 ) == 4 );      // #2 throws on error

    if( add( 2,2 ) != 4 )
      BOOST_ERROR( "Ouch..." );            // #3 continues on error

    if( add( 2,2 ) != 4 )
      BOOST_FAIL( "Ouch..." );             // #4 throws on error

    if( add( 2,2 ) != 4 ) throw "Ouch..."; // #5 throws on error

    BOOST_CHECK_MESSAGE( add( 2,2 ) == 4,  // #6 continues on error
                         "add(..) result: " << add( 2,2 ) );

    BOOST_CHECK_EQUAL( add( 2,2 ), 4 );   // #7 continues on error
}

