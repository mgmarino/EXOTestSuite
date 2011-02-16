import sys
import re
import ROOT
import math
import ctypes


""" 
Mapping dict
provides a mapping between the old tree and
new tree, ensuring that data saved in one is
equivalent to data saved in the new tree.
""" 
mapping_dict = {
    "nr" : "fRunNumber",   
    "ne" : "fEventNumber",   
    "fidev" : "fIsFiducialEvent", 
    "bb0n" : "fIsbb0nCandidate", 
    "bb2n" : "fIsbb2nCandidate",  
    "alpha" : "fIsAlphaCandidate", 
    "nsite" : "fNumberOfSites", 
    "errec" : "fTotalRawEnergy", 
    "eprec" : "fTotalPurityCorrectedEnergy", 
    "ecrec" : "fTotalGridEffCorrectedEnergy", 
    "depth" : "fDepth", 
    "ecsum" : "fCorrectedEnergySum", 
    "header" : "fEventHeader.fHeaderString",        
    "svn_rev" : "fEventHeader.fSVNRevision",       
    "build_id" : "fEventHeader.fBuildID",      
    "compressionid" : "fEventHeader.fCompressionID", 
    "frameid" : "fEventHeader.fFrameID",       
    "framerev" : "fEventHeader.fFrameRevision",      
    "cc" : "fEventHeader.fCardCount",            
    "trigcount" : "fEventHeader.fTriggerCount",     
    "trigsec" : "fEventHeader.fTriggerSeconds",       
    "trigsub" : "fEventHeader.fTriggerMicroSeconds",       
    "trigdrift" : "fEventHeader.fTriggerDrift",     
    "sn" : "fEventHeader.fSumTriggerThreshold",            
    "sr" : "fEventHeader.fSumTriggerRequest",            
    "trigsum" : "fEventHeader.fSumTriggerValue",       
    "in" : "fEventHeader.fIndividualTriggerThreshold",            
    "ir" : "fEventHeader.fIndividualTriggerRequest",            
    "indsum" : "fEventHeader.fMaxValueChannel",        
    "trigchan" : "fEventHeader.fOfflineTriggerChannel",      
    "trigoff" : "fEventHeader.fTriggerOffset",       
    "ebit" : "fEventHeader.fFrameIsEmpty",          
    "src" : "fEventHeader.fTriggerSource",           
    "samplecount" : "fEventHeader.fSampleCount",   
    "g4ne" : "fEventHeader.fGeant4EventNumber",          
    "subne" : "fEventHeader.fGeant4SubEventNumber",         
    "is_mc" : "fEventHeader.fIsMonteCarloEvent",         
    "mcfid" : "fEventHeader.fMonteCarloFiducialFlag",         
    "muontag" : "fEventHeader.fTaggedAsMuon",            
    "muon_driftvelocity" : "fEventHeader.fMuonDriftVelocity", 
    "muon_purity" : "fEventHeader.fMuonPurity",       
    "muon_purity_err" : "fEventHeader.fMuonPurityError",    
    "qbeta" : "fMonteCarloData.fBetaDecayQValue", 
    "x0" : "fMonteCarloData.fPrimaryEventX",    
    "y0" : "fMonteCarloData.fPrimaryEventY",    
    "z0" : "fMonteCarloData.fPrimaryEventZ",    
    
    "totalph" : "fMonteCarloData.fTotalPhotons", 
    "hitsp1" : "fMonteCarloData.fTotalHitsArrayOne",  
    "hitsp2" : "fMonteCarloData.fTotalHitsArrayTwo",  
    "esalt" : "fMonteCarloData.fTotalEnergyInSalt",                 
    "eshield" : "fMonteCarloData.fTotalEnergyInShield",               
    "eoutcry" : "fMonteCarloData.fTotalEnergyInOuterCryostat",               
    "eincry" : "fMonteCarloData.fTotalEnergyInInnerCryostat",               
    "ehfe" : "fMonteCarloData.fTotalEnergyInHFE",                  
    "evessel" : "fMonteCarloData.fTotalEnergyInVessel",               
    "elxet" : "fMonteCarloData.fTotalEnergyInLiquidXe",                 
    "elxei" : "fMonteCarloData.fTotalIonizationEnergyInLiquidXe",                 
    "ecathode_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInCathode",      
    "eanodes_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInBothAnodes",       
    "ewire_supports_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInBothWireSupports",
    "ecathode_ring_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInCathodeRing", 
    "ereflector_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInTeflonReflector",    
    "eapd_frames_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInBothAPDFrames",   
    "elxe_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInLiquidXe",          
    "evessel_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInLiquidXeVessel",       
    "eremoved_apds_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInRemovedAPDs", 
    "efield_rings_photons" : "fMonteCarloData.fTotalEnergyOptPhotonsInFieldShapingRings",  
    "npart" :  "fMonteCarloData.GetNumParticleInformation()",
    "nq" :  "fMonteCarloData.GetNumPixelatedChargeDeposit()",
    "napd" :  "fMonteCarloData.GetNumAPDHits()",
    "idpart" : "fMonteCarloData.GetParticleInformation(%i).fID", 
    "apart" :  "fMonteCarloData.GetParticleInformation(%i).fAtomicNumber",  
    "epart" :  "fMonteCarloData.GetParticleInformation(%i).fKineticEnergykeV",  
    "qpart" :  "fMonteCarloData.GetParticleInformation(%i).fCharge",  
    "expart" : "fMonteCarloData.GetParticleInformation(%i).fExcitedStatekeV", 


    "apd_hits" : "fMonteCarloData.GetAPDHit(%i).fNumHits", 
    "eapd" : "fMonteCarloData.GetAPDHit(%i).fEnergy",     
    "qapd" : "fMonteCarloData.GetAPDHit(%i).fCharge",     

    "ixq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i).fX", 
    "iyq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i).fY", 
    "izq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i).fZ", 
    "etq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i).fTotalEnergykeV", 
    "eiq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i).fTotalIonizationEnergykeV", 

    "c1sc" : "GetScintillationCluster(%i).fCountsOnAPDPlaneOne",       
    "c1errsc" : "GetScintillationCluster(%i).fCountsOnAPDPlaneOneError",    
    "c2sc" : "GetScintillationCluster(%i).fCountsOnAPDPlaneTwo",       
    "c2errsc" : "GetScintillationCluster(%i).fCountsOnAPDPlaneTwoError",    
    "c1sumsc" : "GetScintillationCluster(%i).fCountsSumOnAPDPlaneOne",    
    "c1sumerrsc" : "GetScintillationCluster(%i).fCountsSumOnAPDPlaneOneError", 
    "c2sumsc" : "GetScintillationCluster(%i).fCountsSumOnAPDPlaneTwo",    
    "c2sumerrsc" : "GetScintillationCluster(%i).fCountsSumOnAPDPlaneTwoError", 

    "chi2_APD1" : "fChiSquaredAPDOne",  
    "chi2_APD2" : "fChiSquaredAPDTwo",  

    "xsc" : "GetScintillationCluster(%i).fX",        
    "ysc" : "GetScintillationCluster(%i).fY",        
    "zsc" : "GetScintillationCluster(%i).fZ",        
    "tsc" : "GetScintillationCluster(%i).fTime",        
    "rsc" : "GetScintillationCluster(%i).fRadius",        
    "esc" : "GetScintillationCluster(%i).fEnergy",        
    "algsc" : "GetScintillationCluster(%i).fAlgorithmUsed",      

    "xcl" : "GetChargeCluster(%i).fX",  
    "ycl" : "GetChargeCluster(%i).fY",  
    "ucl" : "GetChargeCluster(%i).fU",  
    "vcl" : "GetChargeCluster(%i).fV",  
    "zcl" : "GetChargeCluster(%i).fZ",  
    "dtcl" : "GetChargeCluster(%i).fDriftTime", 
    "tcl" : "GetChargeCluster(%i).fCollectionTime",  


    "ercl" : "GetChargeCluster(%i).fRawEnergy",   
    "eccl" : "GetChargeCluster(%i).fCorrectedEnergy",   
    "epcl" : "GetChargeCluster(%i).fPurityCorrectedEnergy",   
    "eerrcl" : "GetChargeCluster(%i).fCorrectedEnergyError", 
    "ncscl" : "GetChargeCluster(%i).fNumberOfCollectionSignals",   
    "iu1cl" : "GetChargeCluster(%i).fChanNumOfFirstSignal",   
    "iu2cl" : "GetChargeCluster(%i).fChanNumOfSecondSignal",   
    "iu3cl" : "GetChargeCluster(%i).fChanNumOfThirdSignal",   
    "iu4cl" : "GetChargeCluster(%i).fChanNumOfFourthSignal",   
    "nvchcl" : "GetChargeCluster(%i).fNumberOfVChannels",  
    "iv1cl" : "GetChargeCluster(%i).fVChannelNumberOne",   
    "iv2cl" : "GetChargeCluster(%i).fVChannelNumberTwo",   
    "dhalfcl" : "GetChargeCluster(%i).fDetectorHalf", 
    "evcl" : "GetChargeCluster(%i).fEnergyInVChannels",    


    "nusig" : "GetNumUWireSignals()",             
    "ncl" : "GetNumChargeClusters()",             
    "nsc" : "GetNumScintillationClusters()",             
    "usig_ch" : "GetUWireSignal(%i).fChannel",             
    "usig_e" : "GetUWireSignal(%i).fEnergy",              
    "usig_deltae" : "GetUWireSignal(%i).fEnergyError",         
    "usig_t" : "GetUWireSignal(%i).fTime",              
    "usig_deltat" : "GetUWireSignal(%i).fTimeError",         
    "usig_baseline" : "GetUWireSignal(%i).fBaseline",       
    "usig_deltabaseline" : "GetUWireSignal(%i).fBaselineError",  
    "usig_chi2" : "GetUWireSignal(%i).fChiSquare",           
    "nsig" : "GetWaveformData().GetNumWaveforms()",

    "chi2_APD_gang" : "GetAPDSignal(%i).fChiSquareGang",

    "compton_e" : "fCompton.fEnergy",
    "compton_fom" : "fCompton.fFOM",
    "compton_ncl" : "fCompton.fNumClustersUsed",
    "compton_phi" : "fCompton.fHalfAnglePhi",
    "compton_phi_err" : "fCompton.fHalfAnglePhiErr",
    "compton_x1" : "fCompton.fX1",
    "compton_y1" : "fCompton.fY1",
    "compton_z1" : "fCompton.fZ1",
    "compton_dx1" : "fCompton.fX1Err",
    "compton_dy1" : "fCompton.fY1Err",
    "compton_dz1" : "fCompton.fZ1Err",
    "compton_x2" : "fCompton.fX2",
    "compton_y2" : "fCompton.fY2",
    "compton_z2" : "fCompton.fZ2",
    "compton_dx2" : "fCompton.fX2Err",
    "compton_dy2" : "fCompton.fY2Err",
    "compton_dz2" : "fCompton.fZ2Err",
    "nsample" : "GetWaveformData()->fNumSamples",
     
    #"chan" : "GetWaveformData().GetNumWaveforms()",
# Must handle data specially...
    #"nsample" : "",
    #"nele" : "", 
    #"data" : "", 
    #"nqele" : "", 
    #"qdata" : "", 
    }

ignored = [
   "chan",
   "nsample",
   "nele",
   "data",
   "nqele",
   "qdata",
   "nsig",
   "header",
   "svn_rev",
   "build_id",
   "compressionid",
   "ssc", 
   "sssc", 
   "thsc", 
   ]
tref_list = [
   "usig_ichargecluster",
   "isccl",
   "iu1clcs",
   "iu2clcs",
   "iu3clcs",
   "iu4clcs",
   "scint_ichargecluster",
]
special_bool = {
    "ghcl" : "GetChargeCluster(%i).fIsGhost",    
    "tdcl" : "GetChargeCluster(%i).fIs3DCluster",    
    "fidcl" : "GetChargeCluster(%i).fIsFiducial",   
}
gang_info = {
    "csc" : "GetScintillationCluster(%i).GetGangInfo(%i).fCount",
    "cerrsc" : "GetScintillationCluster(%i).GetGangInfo(%i).fCountErr",
}
not_yet_implemented = []

def compare(old, new, old_branch, new_branch, entry):
    if old != new and not (math.isnan(old) and math.isnan(new)):
        print '*'*60
        print old_branch, new_branch, entry
        print old, new
        print '*'*60

def compare_gang_info(branch, old, new_event):
    temp_str = gang_info[branch]  
    num_apds = 74
    i = 0
    total_num = 0
    #for clus in new_event.GetScintillationClusterArray():
    #    total_num += clus.GetNumGangInfo()
    #print total_num, len(old)
    for val in old:
        new_value =  eval("new_event." + (temp_str % (i/num_apds, i%num_apds))) 
        compare(val, new_value, branch, "", "")
        i += 1
        

def compare_tref(branch, old, new_event, old_tree):
    # Unfortunately, have to do this by hand
    i = 0
    if branch == "usig_ichargecluster":
        for index in old: 
            uwire_signal = new_event.GetUWireSignal(i)
            charge_cluster = uwire_signal.GetChargeCluster()
            compare(old_tree.xcl[index], charge_cluster.fX, "usig_ichargecluster", "", "")
            compare(old_tree.ycl[index], charge_cluster.fY, "usig_ichargecluster", "", "")
            i += 1
    elif branch == "isccl":
        for index in old: 
            if index == -999: continue
            charge_cluster = new_event.GetChargeCluster(i)
            scint_cluster = charge_cluster.GetScintillationCluster()
            compare( old_tree.xsc[index], scint_cluster.fX, "isccl", "", "")
            compare( old_tree.ysc[index], scint_cluster.fY, "isccl", "", "")
            i += 1
    elif branch == "iu1clcs":
        for index in old: 
            if index == -1: continue
            charge_cluster = new_event.GetChargeCluster(i)
            uwire_signal = charge_cluster.GetFirstUWireSignal()
            compare(old_tree.usig_t[index], uwire_signal.fTime, "iu1clcs", "", "")
            compare(old_tree.usig_e[index], uwire_signal.fEnergy, "iu1clcs", "", "")
            i += 1
    elif branch == "iu2clcs":
        for index in old: 
            if index == -1: continue
            charge_cluster = new_event.GetChargeCluster(i)
            uwire_signal = charge_cluster.GetSecondUWireSignal()
            compare(old_tree.usig_t[index], uwire_signal.fTime, "iu2clcs", "", "")
            compare(old_tree.usig_e[index], uwire_signal.fEnergy, "iu2clcs", "", "")
            i += 1
    elif branch == "iu3clcs":
        for index in old: 
            if index == -1: continue
            charge_cluster = new_event.GetChargeCluster(i)
            uwire_signal = charge_cluster.GetThirdUWireSignal()
            compare(old_tree.usig_t[index], uwire_signal.fTime, "iu3clcs", "", "")
            compare(old_tree.usig_e[index], uwire_signal.fEnergy, "iu3clcs", "", "")
            i += 1
    elif branch == "iu4clcs":
        for index in old: 
            if index == -1: continue
            charge_cluster = new_event.GetChargeCluster(i)
            uwire_signal = charge_cluster.GetFourthUWireSignal()
            compare(old_tree.usig_t[index], uwire_signal.fTime, "iu4clcs", "", "")
            compare(old_tree.usig_e[index], uwire_signal.fEnergy, "iu4clcs", "", "")
            i += 1
    elif branch == "scint_ichargecluster":
        for index in old: 
            if index == -1: continue
            scint_cluster = new_event.GetScintillationCluster(i)
            j = 0
            for more in index: 
                if more.GetVal() >= len(old_tree.xcl):
                    print "Problem with old tree"
                    j += 1
                    continue
                if more.GetVal() < 0: continue
                charge_cluster = scint_cluster.GetChargeClusterAt(j)
                compare(old_tree.xcl[more.GetVal()], charge_cluster.fX, "scint_ichargecluster", "", "")
                compare(old_tree.ycl[more.GetVal()], charge_cluster.fY, "scint_ichargecluster", "", "")
                j += 1
            i += 1

def compare_trees(old_tree, new_tree):
    for i in range(old_tree.GetEntries()):
        old_tree.GetEntry(i)
        new_tree.GetEntry(i)
        print i
        for branch in old_tree.GetListOfBranches():
            if branch.GetName() in tref_list:
                compare_tref(branch.GetName(), getattr(old_tree, branch.GetName()), new_tree.EventBranch, old_tree) 
                continue
            if branch.GetName() in gang_info:
                compare_gang_info(branch.GetName(), getattr(old_tree, branch.GetName()), new_tree.EventBranch) 
                continue
            if branch.GetName() in ignored:
                continue
            if branch.GetName() in special_bool.keys():
                aleaf = old_tree.GetBranch(branch.GetName()).GetListOfLeaves()[0]
                temp_str = special_bool[branch.GetName()]
                for j in range(old_tree.ncl):
                    temp = temp_str % j
                    new_value =  eval("event." + temp) 
                    compare(aleaf.GetValue(j) > 0, new_value, branch.GetName(), temp, i)
                continue
            if branch.GetName() not in mapping_dict.keys():
                if branch.GetName() not in not_yet_implemented:
                    not_yet_implemented.append(branch.GetName())
                continue
            event = new_tree.EventBranch
            old_value = getattr(old_tree, branch.GetName())
            temp_str = mapping_dict[branch.GetName()]
            try:
                for j in range(len(old_value)):
                    temp = temp_str % j
                    new_value =  eval("event." + temp) 
                    compare(old_value[j], new_value, branch.GetName(), temp, i)
            except TypeError:
                new_value =  eval("event." + temp_str) 
                compare(old_value, new_value, branch.GetName(), temp_str, i)
            

if __name__ == '__main__':
    ROOT.gSystem.Load("libEXOUtilities")
    compare_trees(ROOT.TFile.Open(sys.argv[1]).Get("tree"), ROOT.TFile.Open(sys.argv[2]).Get("tree")) 
    for branch in not_yet_implemented:
        print branch
