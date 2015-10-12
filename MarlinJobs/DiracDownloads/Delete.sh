#!/bin/bash

while read line
do
    echo "Deleting : $line"
    dirac-dms-remove-files $line
done < "filesToDelete.txt" 
