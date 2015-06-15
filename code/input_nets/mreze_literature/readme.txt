I first removed the commas from some of the edge lists:
awk  '{print substr($1,0,length($1)-1), $2}' lesMiserables_network.txt | uniq > miserables_unfinished.txt

Then I ran them through the filter_literature_nets.py script from ../ => This removed self-loops and other stuff

Then I ran them through list2leda and converted them to .gw
