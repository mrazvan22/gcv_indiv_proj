human_ppi

take columns 2/3(protein name) (A0AVK6 or E2F8) and 4(gene ontology: GO:0006351) from gene_association.goe_human 
take name from gene_ontology_ext.obo

 UniProtKB A0AVK6  E2F8    GO:0006351  GO_REF:0000037  IEA UniProtKB-KW:KW-0804 

Each Protein is mapped to several gene ontology GO codes (which represent  biological functions) - data is binary
The difference between columns 2 and 3 is due to different encoding standards


Metabolic network:
0. analyse the hsa0001.keg file
1. take all the rows that start with D
2. only take the third columns (ENO3) and the last column (EC number)


D      2027 ENO3; enolase 3 (beta, muscle)  K01689 ENO; enolase [EC:4.2.1.11]
