# Submit Mokka jobs to the grid: MokkaGridJobs.py 
import re
import os
import sys

### ----------------------------------------------------------------------------------------------------

def setGearFile(mokkaSteeringTemplate,gearFile):
    mokkaSteeringTemplate = re.sub('GEAR_FILE_XXXX',gearFile,mokkaSteeringTemplate)
    return mokkaSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def setStartNumber(mokkaSteeringTemplate,startNumber):
    mokkaSteeringTemplate = re.sub('START_EVENT_NUMBER_XXXX',str(startNumber),mokkaSteeringTemplate)
    return mokkaSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def setOutputFile(mokkaSteeringTemplate,outputFile):
    mokkaSteeringTemplate = re.sub('OUTPUT_FILE_NAME_XXXX',outputFile,mokkaSteeringTemplate)
    return mokkaSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def getMokkaVersion(detectorConfigFile):
    config = {}
    execfile(detectorConfigFile, config)
    return config['MokkaVersion']

### ----------------------------------------------------------------------------------------------------

def getMokkaSteeringFileTemplate(baseFileName,detectorConfigFile):
    config = {}
    execfile(detectorConfigFile, config)

    baseFile = open(baseFileName,'r')
    mokkaSteeringTemplate = baseFile.read()
    baseFile.close()

    # Detector Model
    mokkaSteeringTemplate = re.sub('DETECTOR_MODEL_XXXX',config['DetectorModel'],mokkaSteeringTemplate)

    # Physics List
    mokkaSteeringTemplate = re.sub('PHYSICS_LIST_XXXX',config['PhysicsList'],mokkaSteeringTemplate)

    # HCal absorber material
    mokkaSteeringTemplate = re.sub('HCAL_ABSORBER_MATERIAL_XXXX',str(config['HCalAbsorberMaterial']),mokkaSteeringTemplate)

    # HCal cell size
    mokkaSteeringTemplate = re.sub('HCAL_CELL_SIZE_XXXX',str(config['HCalCellSize']),mokkaSteeringTemplate)

    # Thickness of absorber layers in the HCal
    mokkaSteeringTemplate = re.sub('HCAL_ABSORBER_LAYER_THICKNESS_XXXX',str(config['HCalAbsorberLayerThickness']),mokkaSteeringTemplate)

    # Thickenss of scintillator layers in the HCal
    mokkaSteeringTemplate = re.sub('HCAL_SCINTILLATOR_LAYER_THICKNESS_XXXX',str(config['HCalAbsorberLayerThickness']),mokkaSteeringTemplate)

    # Number of layers in the HCal
    mokkaSteeringTemplate = re.sub('HCAL_NUMBER_OF_LAYERS_XXXX',str(config['NumberHCalLayers']),mokkaSteeringTemplate)

    # Coil extra size, has to be varied if expanding HCal
    mokkaSteeringTemplate = re.sub('COIL_EXTRA_SIZE_XXXX',str(config['CoilExtraSize']),mokkaSteeringTemplate)

    # Strength of B field in tracker
    mokkaSteeringTemplate = re.sub('BFIELD_XXXX',str(config['BField']),mokkaSteeringTemplate)

    # Outer radius of the tracker/ inner radius of the ECal
    mokkaSteeringTemplate = re.sub('TPC_OUTER_RADIUS_XXXX',str(config['TPCOuterRadius']),mokkaSteeringTemplate)

    # Detailed shower mode
    mokkaSteeringTemplate = re.sub('DETAILED_SHOWER_MODE_XXXX',config['DetailedShowerMode'],mokkaSteeringTemplate)

    return mokkaSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def getHEPEvtFiles(energy, eventType):
    hepevtFiles = []
#    os.system('dirac-ilc-find-in-FC /ilc JobDescription="HEPEvt" Energy=' + str(energy) + ' EvtType="' + eventType + '" > tmp.txt')
#    with open('tmp.txt') as f:
#        lines = f.readlines()
#        for idx, line in enumerate(lines):
#            line = line.strip()
#            hepevtFiles.append(line)
#    os.system('rm tmp.txt')

    hepevtFiles.append('/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_1.HEPEvt')
    return hepevtFiles

### ----------------------------------------------------------------------------------------------------

