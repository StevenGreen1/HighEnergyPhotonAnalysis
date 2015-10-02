#!/bin/bash

energy=1500

cd HEPEvtFiles

for entry in *
do
    if [[ $entry == *"${energy}_GeV"* ]]
    then
        echo "Uploading file : $entry"
        dirac-dms-add-file /ilc/user/s/sgreen/HEPEvtFiles/Photon/${energy}GeV/${entry} ${entry} DESY-SRM
        mv $entry UploadedFiles
    fi
done

