#!/bin/sh

#à faire exécuter depuis le code python peut être

#removal of previous labo1 config.
rm ~/.ssh/config.d/openflow-basic 
rm ~/.ssh/config.d/switched_config

#pyhton3 script
python3 ssh_config.py ansible-simple

#hostnames changing
echo "*hostnames*"
for m in R1 R2 H1 H2
do
    echo "ssh "$m "hostname $m";
    ssh -q $m "hostname $m";
done




