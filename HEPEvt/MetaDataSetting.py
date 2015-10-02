import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

energies = [1000,1500]

fc = FileCatalogClient()

for energy in energies:
    path = '/ilc/user/s/sgreen/HEPEvtFiles/Photon/' + str(energy) + 'GeV'
    pathdict = {'path':path, 'meta':{'JobDescription':'HEPEvt','EvtType':'Photon','Energy':energy}}
    res = fc.setMetadata(pathdict['path'], pathdict['meta'])
