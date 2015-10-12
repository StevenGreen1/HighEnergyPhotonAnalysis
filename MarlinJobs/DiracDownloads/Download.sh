#!/bin/bash

source ../../env.sh

recoVar=68
detModel=38
evtType=Photon
jobDescription=HighEnergyPhotons

for i in 1000 1500 # 10 20 50 100 200 500
do 
    cd /r06/lc/sg568/${jobDescription}/Detector_Model_${detModel}/Reco_Stage_${recoVar}/${i}GeV 
    dirac-ilc-find-in-FC /ilc/user/s/sgreen JobDescription=${jobDescription} Energy=${i} EvtType=${evtType} Type=Rec MokkaJobNumber=${detModel} ReconstructionVariant=${recoVar} > "tmp.txt"
    while read line 
    do
        if [[ $line == *'.root'* ]]
        then
            if [ ! -f "${line##*/}" ] && [ ! -f "/r06/lc/sg568/${jobDescription}/Detector_Model_${detModel}/Reco_Stage_${recoVar}/${i}GeV/${line##*/}" ];
            then
                dirac-dms-get-file $line
            fi
        fi
    done < "tmp.txt"
    rm "tmp.txt"
done
