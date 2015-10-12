# Example to submit Marlin job: MarlinExample.py
import os
import sys

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.DiracILC import  DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *

from MarlinGridJobs import *

#===== User Input =====

jobDescription = 'HighEnergyPhotons'
mokkaJobNumber = 38 # Default detector model
#recoStageNumber = 43 # MHHHE off and large timing cuts -> Template 1
#recoStageNumber = 35 # Original digitsation (truncation in ECal on), MHHHE off and large timing cuts -> Template 4
#recoStageNumber = 3 # Old digitiser, MHHHE off and no large timing cuts -> Template 3
recoStageNumber = 68 # Original digitsation (no truncation), MHHHE off and large timing cuts -> Template 2

eventsToSimulate = [ #{ 'EventType': "Kaon0L"  , 'Energies':  ['1','2','3','4','5','6','7','8','9','10','15','20','25','30','35','40','45','50'] }
                     #{ 'EventType': "Z_uds"   , 'Energies':  [91, 200, 360, 500, 750, 1000, 2000, 3000]                                         },
                     #{ 'EventType': "Photon"  , 'Energies':  ['10','20','50','100','200','500']                                                 }
                     { 'EventType': "Photon"  , 'Energies':  ['1000','1500']                                                                    }
                     #{ 'EventType': "Kaon0L"  , 'Energies':  ['1']                                                                              }
                     #{ 'EventType': "Muon"    , 'Energies':  [10]                                                                               }
                   ]

baseXmlFile = 'TemplateRepository/MarlinSteeringFileTemplate_SingleParticles_2.xml'

pandoraSettingsFiles = {}
pandoraSettingsFiles['Default'] = 'PandoraSettings/PandoraSettingsDefault_SiW_5x5.xml' 
pandoraSettingsFiles['Default_LikelihoodData'] = 'PandoraSettings/PandoraLikelihoodData9EBin_SiW_5x5.xml' 
pandoraSettingsFiles['Muon'] = 'PandoraSettings/PandoraSettingsMuon.xml'
pandoraSettingsFiles['PerfectPhoton'] = 'PandoraSettings/PandoraSettingsPerfectPhoton.xml'
pandoraSettingsFiles['PerfectPhotonNK0L'] = 'PandoraSettings/PandoraSettingsPerfectPhotonNeutronK0L.xml'
pandoraSettingsFiles['PerfectPFA'] = 'PandoraSettings/PandoraSettingsPerfectPFA.xml'

#===== Second level user input =====
# If using naming scheme doesn't need changing 

#gearFile = '/usera/xu/ILCSOFT/myGridDownload/ILD_o1_v06_SiW_5x5.gear'
gearFile = '/usera/sg568/ilcsoft_v01_17_07/HCalToEMCalibrationTesting/MokkaJobs/GearFiles/ILD_o1_v06_Detector_Model_' + str(mokkaJobNumber) + '.gear'
calibConfigFile = 'CalibrationConfigFiles/Stage' + str(recoStageNumber) + 'Config_5x5_30x30.py'

#=====

# Copy gear file and pandora settings files to local directory as is needed for submission.
os.system('cp ' + gearFile + ' .')
gearFileLocal = os.path.basename(gearFile)

pandoraSettingsFilesLocal = {}
for key, value in pandoraSettingsFiles.iteritems():
    os.system('cp ' + value + ' .')
    pandoraSettingsFilesLocal[key] = os.path.basename(value)

# Start submission
JobIdentificationString = jobDescription + '_Detector_Model_' + str(mokkaJobNumber) + '_Reco_' + str(recoStageNumber)
diracInstance = DiracILC(withRepo=True,repoLocation="%s.cfg" %( JobIdentificationString))

for eventSelection in eventsToSimulate:
    eventType = eventSelection['EventType']
    for energy in eventSelection['Energies']:
        #slcioFilesToProcess = getPhotonFiles(energy)
        slcioFilesToProcess = getSlcioFiles(jobDescription,38,energy,eventType)

        #print slcioFilesToProcess
        for slcioFile in slcioFilesToProcess:
            print 'Submitting ' + eventType + ' ' + energy + 'GeV jobs.  Detector model ' + str(mokkaJobNumber) + '.  Reconstruction stage ' + str(recoStageNumber) + '.'  
            marlinSteeringTemplate = ''
            marlinSteeringTemplate = getMarlinSteeringFileTemplate(baseXmlFile,calibConfigFile)
            marlinSteeringTemplate = setPandoraSettingsFile(marlinSteeringTemplate,pandoraSettingsFilesLocal)
            marlinSteeringTemplate = setGearFile(marlinSteeringTemplate,gearFileLocal)

            slcioFileNoPath = os.path.basename(slcioFile)
            marlinSteeringTemplate = setInputSlcioFile(marlinSteeringTemplate,slcioFileNoPath)
            marlinSteeringTemplate = setOutputFiles(marlinSteeringTemplate,'MarlinReco_' + slcioFileNoPath[:-6])

            with open("MarlinSteering.steer" ,"w") as SteeringFile:
                SteeringFile.write(marlinSteeringTemplate)

            ma = Marlin()
            ma.setVersion('ILCSoft-01-17-07')
            ma.setSteeringFile('MarlinSteering.steer')
            ma.setGearFile(gearFileLocal)
            ma.setInputFile('lfn:' + slcioFile)

            outputFiles = []
            outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_Default.root')
            outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '.slcio')
            if eventType == 'Z_uds':
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_Muon.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPhoton.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPhotonNK0L.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPFA.root')

            job = UserJob()
            job.setJobGroup(jobDescription)
            job.setInputSandbox(pandoraSettingsFilesLocal.values()) # Local files
            job.setOutputSandbox(['*.log','*.gear','*.mac','*.steer','*.xml'])
            job.setOutputData(outputFiles,OutputPath='/' + jobDescription + '/MarlinJobs/Detector_Model_' + str(mokkaJobNumber) + '/Reco_Stage_' + str(recoStageNumber) + '/' + eventType + '/' + energy + 'GeV') # On grid
            job.setName(jobDescription + '_Detector_Model_' + str(mokkaJobNumber) + '_Reco_' + str(recoStageNumber))
            job.setBannedSites(['LCG.IN2P3-CC.fr','LCG.IN2P3-IRES.fr','LCG.KEK.jp'])
            job.dontPromptMe()
            res = job.append(ma)

            if not res['OK']:
                print res['Message']
                exit()
            job.submit(diracInstance)
            os.system('rm *.cfg')

# Tidy Up
os.system('rm MarlinSteering.steer')
os.system('rm ' + gearFileLocal)
for key, value in pandoraSettingsFilesLocal.iteritems():
    os.system('rm ' + value)

