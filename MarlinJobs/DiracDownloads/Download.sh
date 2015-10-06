#!/bin/bash

cd ..
source env.sh

for i in 10 20 50 100 200 500
do 
    cd /r06/lc/sg568/HighEnergyPhotons/DefaultDetectorModel/RecoStage43/${i}GeV 
    dirac-ilc-find-in-FC /ilc/user/s/sgreen JobDescription=HighEnergyPhotons Energy=${i} EvtType=Photon > "tmp.txt"
    while read line 
    do
        if [[ $line == *'.root'* ]]
        then
            if [ ! -f "${line##*/}" ] && [ ! -f "/r06/lc/sg568/HighEnergyPhotons/DefaultDetectorModel/RecoStage43/${i}GeV/${line##*/}" ];
            then
                dirac-dms-get-file $line
            fi
        fi
    done < "tmp.txt"
    rm "tmp.txt"
done
