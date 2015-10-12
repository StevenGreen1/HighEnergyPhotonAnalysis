#include "TCanvas.h"
#include "TChain.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TLegendEntry.h"
#include "TROOT.h"
#include "TStyle.h"

#include <sstream> 

std::string IntToString(int a);

//===========================================

void analysis(int energy, int recStage)
{
    gROOT->SetBatch();
    gStyle->SetPadTopMargin(0.15);
    gStyle->SetPadBottomMargin(0.15);
    gStyle->SetPadRightMargin(0.15);
    gStyle->SetPadLeftMargin(0.15);

    std::string inputPhotonRootFiles = "/r06/lc/sg568/HighEnergyPhotons/Detector_Model_38/Reco_Stage_" + IntToString(recStage) + "/" + IntToString(energy) + "GeV/*";
    TChain *pTChain = new TChain("PfoAnalysisTree");

    float pfoECalToEmEnergy(0.f), pfoHCalToEmEnergy(0.f);
    int nPfoTargetsPhotons(0), nPfoTargetsTotal(0);

    pTChain->Add(inputPhotonRootFiles.c_str());
    pTChain->SetBranchAddress("pfoECalToEmEnergy",&pfoECalToEmEnergy);
    pTChain->SetBranchAddress("pfoHCalToEmEnergy",&pfoHCalToEmEnergy);
    pTChain->SetBranchAddress("nPfoTargetsTotal",&nPfoTargetsTotal);
    pTChain->SetBranchAddress("nPfoTargetsPhotons",&nPfoTargetsPhotons);

    TH2F *pTH2F = new TH2F("Name","Title",150,0,1.5,150,0,1.5);
    pTH2F->GetXaxis()->SetTitle("Normalised Electromagentic Energy in ECal");
    pTH2F->GetYaxis()->SetTitle("Normalised Electromagentic Energy in HCal");
    pTH2F->SetTitle("");

    for (unsigned int i = 0; i < pTChain->GetEntries(); i++)
    {
        pTChain->GetEntry(i);

        float ecalEnergyToFill(pfoECalToEmEnergy/(float)(energy));
        float hcalEnergyToFill(pfoHCalToEmEnergy/(float)(energy));
        if (nPfoTargetsTotal == 1 and nPfoTargetsPhotons == 1)
        {
            pTH2F->Fill(ecalEnergyToFill,hcalEnergyToFill);
        }
    }

    std::string plotName = "HighEnergyPhotons_" + IntToString(energy) + "GeV_Reco_Stage_" + IntToString(recStage) + "_EnergySplit.png";
    std::string plotName2 = "HighEnergyPhotons_" + IntToString(energy) + "GeV_Reco_Stage_" + IntToString(recStage) + "_EnergySplit.C";

    TLegend *pTLegend = new TLegend(0.3,0.65,0.7,0.8);
    std::string legendLabel = IntToString(energy) + "GeV Photons";
    pTLegend->SetHeader(legendLabel.c_str());

    TCanvas *pTCanvas = new TCanvas("Name","Title",200,10,3000,3000);
    pTCanvas->cd();
    pTH2F->Draw("COLZ");
    pTLegend->Draw("same");
    pTCanvas->SaveAs(plotName.c_str());
    pTCanvas->SaveAs(plotName2.c_str());
}

//===========================================

std::string IntToString(int a)
{
    std::stringstream ss;
    ss << a;
    std::string str = ss.str();
    return str;
}
