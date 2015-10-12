import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

evtType = 'Photon'
jobDescription = 'HighEnergyPhotons'
detNumber = 38
recoStage = 68
fileType = 'Rec'

energies = [1000,1500]

fc = FileCatalogClient()
for energy in energies:
    path = '/ilc/user/s/sgreen/' + jobDescription + '/MarlinJobs/Detector_Model_' + str(detNumber) + '/Reco_Stage_' + str(recoStage) + '/' + evtType + '/' + str(energy) + 'GeV'
    pathdict = {'path':path, 'meta':{'Energy':energy, 'EvtType':evtType, 'JobDescription':jobDescription, 'MokkaJobNumber':detNumber, 'ReconstructionVariant':recoStage, 'Type':fileType}}
    res = fc.setMetadata(pathdict['path'], pathdict['meta'])
