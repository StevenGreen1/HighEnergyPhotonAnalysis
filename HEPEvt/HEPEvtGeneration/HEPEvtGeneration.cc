#include <cmath>
#include <fstream>
#include <iostream>
#include <sstream> 
#include <stdlib.h>

//==========

std::string IntToString(int a);
std::string FloatToString(float a);

//==========

int main () 
{
    int pdgNumber(0), evtNumber(0), jobSize(0);
    float energy(0.f);

    std::cout << "Which single particle events would you like to simulate? (Kaon = 130, Photon = 22, Muon = 13)" << std::endl;
    std::cin >> pdgNumber;

    std::cout << "What energy (in GeV) particles do you want to make?" << std::endl;
    std::cin >> energy;

    std::cout << "How many events would you like to simulate in total?" << std::endl;
    std::cin >> evtNumber;

    std::cout << "How many events do you want per file?" << std::endl;
    std::cin >> jobSize;

    std::string strPdgNumber = IntToString(pdgNumber); 
    std::string strEnergy = FloatToString(energy);;
    std::string strNumber = IntToString(evtNumber);
    std::string strJobSize = IntToString(jobSize);

    std::string prefixRunfile = strEnergy + "_GeV_Energy_" + strPdgNumber + "_pdg";

    srand(1234576);

    float mass(0.f), pTot(std::sqrt((energy*energy)-(mass*mass))), pi(std::acos(0)*2);
    int numberJobs = floor( ((float)(evtNumber)/(float)(jobSize)) + 0.5);

    if (130 == pdgNumber)
        mass = 0.497614; // PDG 29-9-14

    else if (22 == pdgNumber)
        mass = 0;

    else if (13 == pdgNumber)
        mass =  0.1056583715; // PDG 29-9-14

    else
        std::cout << "Please select from the avaliable particles." << std::endl;

    for (int z = 0; z < numberJobs; z++)
    {
        int start = z * jobSize;
        int end = (z+1) * jobSize;

        std::string strZ = IntToString(z);
        std::string startStr = IntToString(start);
        std::string endStr = IntToString(end);

        std::ofstream jobZFile;
        std::string jobZFilename = "../HEPEvtFiles/" + prefixRunfile + "_" + startStr + "_" + endStr + ".HEPEvt"; 
        jobZFile.open (jobZFilename.c_str());

        for (int  i = 0; i < jobSize; i++)
        {
            const float sign(((static_cast<float>(rand()) / static_cast<float>(RAND_MAX)) > 0.5f) ? 1.f : -1.f);
            float cosTheta = sign * (static_cast<float>(rand()) / static_cast<float>(RAND_MAX));
            float phi = 2 * pi * (static_cast<float>(rand()) / static_cast<float>(RAND_MAX));

            float pX = pTot * std::sin(std::acos(cosTheta)) * std::cos(phi);
            float pY = pTot * std::sin(std::acos(cosTheta)) * std::sin(phi);
            float pZ = pTot * cosTheta;

            jobZFile << "\t" << 1 << "\n";
            jobZFile << "\t\t" << 1 << "\t" << strPdgNumber << "\t\t" << 0 << "\t\t" << 0 << "\t" << pX << "\t\t" << pY << "\t\t" << pZ << "\t\t" << mass << "\n";
        }
        jobZFile.close();
    }
    return 0;
}

//==========

std::string IntToString(int a)
{
    std::stringstream strBuf;
    strBuf << a;
    std::string str(strBuf.str());
    return str;
}

//==========

std::string FloatToString(float a)
{
    std::stringstream strBuf;
    strBuf << a;
    std::string str(strBuf.str());
    return str;
}

