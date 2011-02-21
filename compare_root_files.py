import sys
import re
import ROOT
import math
import ctypes
import pdb


""" 
Mapping dict
provides a mapping between the old tree and
new tree, ensuring that data saved in one is
equivalent to data saved in the new tree.
""" 
mapping_dict = {
    "nr" : "@event@.fRunNumber",   
    "ne" : "@event@.fEventNumber",   
    "fidev" : "@event@.fIsFiducialEvent", 
    "bb0n" : "@event@.fIsbb0nCandidate", 
    "bb2n" : "@event@.fIsbb2nCandidate",  
    "alpha" : "@event@.fIsAlphaCandidate", 
    "nsite" : "@event@.fNumberOfSites", 
    "errec" : "@event@.fTotalRawEnergy", 
    "eprec" : "@event@.fTotalPurityCorrectedEnergy", 
    "ecrec" : "@event@.fTotalGridEffCorrectedEnergy", 
    "depth" : "@event@.fDepth", 
    "ecsum" : "@event@.fCorrectedEnergySum", 
    "header" : "@event@.fEventHeader.fHeaderString",        
    "svn_rev" : "@event@.fEventHeader.fSVNRevision",       
    "build_id" : "@event@.fEventHeader.fBuildID",      
    "compressionid" : "@event@.fEventHeader.fCompressionID", 
    "frameid" : "@event@.fEventHeader.fFrameID",       
    "framerev" : "@event@.fEventHeader.fFrameRevision",      
    "cc" : "@event@.fEventHeader.fCardCount",            
    "trigcount" : "@event@.fEventHeader.fTriggerCount",     
    "trigsec" : "@event@.fEventHeader.fTriggerSeconds",       
    "trigsub" : "@event@.fEventHeader.fTriggerMicroSeconds",       
    "trigdrift" : "@event@.fEventHeader.fTriggerDrift",     
    "sn" : "@event@.fEventHeader.fSumTriggerThreshold",            
    "sr" : "@event@.fEventHeader.fSumTriggerRequest",            
    "trigsum" : "@event@.fEventHeader.fSumTriggerValue",       
    "in" : "@event@.fEventHeader.fIndividualTriggerThreshold",            
    "ir" : "@event@.fEventHeader.fIndividualTriggerRequest",            
    "indsum" : "@event@.fEventHeader.fMaxValueChannel",        
    "trigchan" : "@event@.fEventHeader.fOfflineTriggerChannel",      
    "trigoff" : "@event@.fEventHeader.fTriggerOffset",       
    "ebit" : "@event@.fEventHeader.fFrameIsEmpty",          
    "src" : "@event@.fEventHeader.fTriggerSource",           
    "samplecount" : "@event@.fEventHeader.fSampleCount",   
    "g4ne" : "@event@.fEventHeader.fGeant4EventNumber",          
    "subne" : "@event@.fEventHeader.fGeant4SubEventNumber",         
    "is_mc" : "@event@.fEventHeader.fIsMonteCarloEvent",         
    "mcfid" : "@event@.fEventHeader.fMonteCarloFiducialFlag",         
    "muontag" : "@event@.fEventHeader.fTaggedAsMuon",            
    "muon_driftvelocity" : "@event@.fEventHeader.fMuonDriftVelocity", 
    "muon_purity" : "@event@.fEventHeader.fMuonPurity",       
    "muon_purity_err" : "@event@.fEventHeader.fMuonPurityError",    
    "muon_theta" : "@event@.fEventHeader.fMuonTheta",    
    "muon_phi" : "@event@.fEventHeader.fMuonPhi",    
    "qbeta" : "@event@.fMonteCarloData.fBetaDecayQValue", 
    "x0" : "@event@.fMonteCarloData.fPrimaryEventX",    
    "y0" : "@event@.fMonteCarloData.fPrimaryEventY",    
    "z0" : "@event@.fMonteCarloData.fPrimaryEventZ",    
    
    "totalph" : "@event@.fMonteCarloData.fTotalPhotons", 
    "hitsp1" : "@event@.fMonteCarloData.fTotalHitsArrayOne",  
    "hitsp2" : "@event@.fMonteCarloData.fTotalHitsArrayTwo",  
    "esalt" : "@event@.fMonteCarloData.fTotalEnergyInSalt",                 
    "eshield" : "@event@.fMonteCarloData.fTotalEnergyInShield",               
    "eoutcry" : "@event@.fMonteCarloData.fTotalEnergyInOuterCryostat",               
    "eincry" : "@event@.fMonteCarloData.fTotalEnergyInInnerCryostat",               
    "ehfe" : "@event@.fMonteCarloData.fTotalEnergyInHFE",                  
    "evessel" : "@event@.fMonteCarloData.fTotalEnergyInVessel",               
    "elxet" : "@event@.fMonteCarloData.fTotalEnergyInLiquidXe",                 
    "elxei" : "@event@.fMonteCarloData.fTotalIonizationEnergyInLiquidXe",                 
    "ecathode_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInCathode",      
    "eanodes_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInBothAnodes",       
    "ewire_supports_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInBothWireSupports",
    "ecathode_ring_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInCathodeRing", 
    "ereflector_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInTeflonReflector",    
    "eapd_frames_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInBothAPDFrames",   
    "elxe_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInLiquidXe",          
    "evessel_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInLiquidXeVessel",       
    "eremoved_apds_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInRemovedAPDs", 
    "efield_rings_photons" : "@event@.fMonteCarloData.fTotalEnergyOptPhotonsInFieldShapingRings",  
    "npart" :  "@event@.fMonteCarloData.GetNumParticleInformation()",
    "nq" :  "@event@.fMonteCarloData.GetNumPixelatedChargeDeposit()",
    "idpart" : "@event@.fMonteCarloData.GetParticleInformation(%i).fID", 
    "apart" :  "@event@.fMonteCarloData.GetParticleInformation(%i).fAtomicNumber",  
    "epart" :  "@event@.fMonteCarloData.GetParticleInformation(%i).fKineticEnergykeV",  
    "qpart" :  "@event@.fMonteCarloData.GetParticleInformation(%i).fCharge",  
    "expart" : "@event@.fMonteCarloData.GetParticleInformation(%i).fExcitedStatekeV", 


    #"napd" :  "@event@.fMonteCarloData.GetNumAPDHits()",
    #"apd_hits" : "@event@.fMonteCarloData.GetAPDHit(%i).fNumHits", 
    #"eapd" : "@event@.fMonteCarloData.GetAPDHit(%i).fEnergy",     
    #"qapd" : "@event@.fMonteCarloData.GetAPDHit(%i).fCharge",     

    "ixq" : "@event@.fMonteCarloData.GetPixelatedChargeDeposit(%i).fX", 
    "iyq" : "@event@.fMonteCarloData.GetPixelatedChargeDeposit(%i).fY", 
    "izq" : "@event@.fMonteCarloData.GetPixelatedChargeDeposit(%i).fZ", 
    "etq" : "@event@.fMonteCarloData.GetPixelatedChargeDeposit(%i).fTotalEnergykeV", 
    "eiq" : "@event@.fMonteCarloData.GetPixelatedChargeDeposit(%i).fTotalIonizationEnergykeV", 

    "c1sc" : "@event@.GetScintillationCluster(%i).fCountsOnAPDPlaneOne",       
    "c1errsc" : "@event@.GetScintillationCluster(%i).fCountsOnAPDPlaneOneError",    
    "c2sc" : "@event@.GetScintillationCluster(%i).fCountsOnAPDPlaneTwo",       
    "c2errsc" : "@event@.GetScintillationCluster(%i).fCountsOnAPDPlaneTwoError",    
    "c1sumsc" : "@event@.GetScintillationCluster(%i).fCountsSumOnAPDPlaneOne",    
    "c1sumerrsc" : "@event@.GetScintillationCluster(%i).fCountsSumOnAPDPlaneOneError", 
    "c2sumsc" : "@event@.GetScintillationCluster(%i).fCountsSumOnAPDPlaneTwo",    
    "c2sumerrsc" : "@event@.GetScintillationCluster(%i).fCountsSumOnAPDPlaneTwoError", 

    "chi2_APD1" : "@event@.fChiSquaredAPDOne",  
    "chi2_APD2" : "@event@.fChiSquaredAPDTwo",  

    "xsc" : "@event@.GetScintillationCluster(%i).fX",        
    "ysc" : "@event@.GetScintillationCluster(%i).fY",        
    "zsc" : "@event@.GetScintillationCluster(%i).fZ",        
    "tsc" : "@event@.GetScintillationCluster(%i).fTime",        
    "rsc" : "@event@.GetScintillationCluster(%i).fRadius",        
    "esc" : "@event@.GetScintillationCluster(%i).fEnergy",        
    "thsc" : "@event@.GetScintillationCluster(%i).fTheta",        
    "ssc" : "@event@.GetScintillationCluster(%i).fRawEnergy",        
    #"sssc" : "@event@.GetScintillationCluster(%i).fCountsSumOnAPDPlaneOne + @event@.GetScintillationCluster(%i).fCountsSumOnAPDPlaneTwo", 
    "sssc" : "@event@.GetScintillationCluster(%i).fSumCounts",
    "algsc" : "@event@.GetScintillationCluster(%i).fAlgorithmUsed",      

    "xcl" : "@event@.GetChargeCluster(%i).fX",  
    "ycl" : "@event@.GetChargeCluster(%i).fY",  
    "ucl" : "@event@.GetChargeCluster(%i).fU",  
    "vcl" : "@event@.GetChargeCluster(%i).fV",  
    "zcl" : "@event@.GetChargeCluster(%i).fZ",  
    "dtcl" : "@event@.GetChargeCluster(%i).fDriftTime", 
    "tcl" : "@event@.GetChargeCluster(%i).fCollectionTime",  


    "ercl" : "@event@.GetChargeCluster(%i).fRawEnergy",   
    "eccl" : "@event@.GetChargeCluster(%i).fCorrectedEnergy",   
    "epcl" : "@event@.GetChargeCluster(%i).fPurityCorrectedEnergy",   
    "eerrcl" : "@event@.GetChargeCluster(%i).fCorrectedEnergyError", 
    "ncscl" : "@event@.GetChargeCluster(%i).GetNumUWireSignals()",   
    "iu1cl" : "@event@.GetChargeCluster(%i).GetUWireSignalChannelAt(0)",   
    "iu2cl" : "@event@.GetChargeCluster(%i).GetUWireSignalChannelAt(1)",   
    "iu3cl" : "@event@.GetChargeCluster(%i).GetUWireSignalChannelAt(2)",   
    "iu4cl" : "@event@.GetChargeCluster(%i).GetUWireSignalChannelAt(3)",   
    "nvchcl" : "@event@.GetChargeCluster(%i).fNumberOfVChannels",  
    "iv1cl" : "@event@.GetChargeCluster(%i).fVChannelNumberOne",   
    "iv2cl" : "@event@.GetChargeCluster(%i).fVChannelNumberTwo",   
    "dhalfcl" : "@event@.GetChargeCluster(%i).fDetectorHalf", 
    "evcl" : "@event@.GetChargeCluster(%i).fEnergyInVChannels",    


    "nusig" : "@event@.GetNumUWireSignals()",             
    "ncl" : "@event@.GetNumChargeClusters()",             
    "nsc" : "@event@.GetNumScintillationClusters()",             
    "usig_ch" : "@event@.GetUWireSignal(%i).fChannel",             
    "usig_e" : "@event@.GetUWireSignal(%i).fEnergy",              
    "usig_deltae" : "@event@.GetUWireSignal(%i).fEnergyError",         
    "usig_t" : "@event@.GetUWireSignal(%i).fTime",              
    "usig_deltat" : "@event@.GetUWireSignal(%i).fTimeError",         
    "usig_baseline" : "@event@.GetUWireSignal(%i).fBaseline",       
    "usig_deltabaseline" : "@event@.GetUWireSignal(%i).fBaselineError",  
    "usig_chi2" : "@event@.GetUWireSignal(%i).fChiSquare",           
    "nsig" : "@event@.GetWaveformData().GetNumWaveforms()",

    "napd" :  "@event@.GetNumAPDSignals()",
    #"chi2_APD_gang" : "@event@.GetAPDSignal(%i).fChiSquareGang",

    "compton_e" : "@event@.fCompton.fEnergy",
    "compton_fom" : "@event@.fCompton.fFOM",
    "compton_ncl" : "@event@.fCompton.fNumClustersUsed",
    "compton_phi" : "@event@.fCompton.fHalfAnglePhi",
    "compton_phi_err" : "@event@.fCompton.fHalfAnglePhiErr",
    "compton_x1" : "@event@.fCompton.fX1",
    "compton_y1" : "@event@.fCompton.fY1",
    "compton_z1" : "@event@.fCompton.fZ1",
    "compton_dx1" : "@event@.fCompton.fX1Err",
    "compton_dy1" : "@event@.fCompton.fY1Err",
    "compton_dz1" : "@event@.fCompton.fZ1Err",
    "compton_x2" : "@event@.fCompton.fX2",
    "compton_y2" : "@event@.fCompton.fY2",
    "compton_z2" : "@event@.fCompton.fZ2",
    "compton_dx2" : "@event@.fCompton.fX2Err",
    "compton_dy2" : "@event@.fCompton.fY2Err",
    "compton_dz2" : "@event@.fCompton.fZ2Err",
    "nsample" : "@event@.GetWaveformData()->fNumSamples",
     
    #"chan" : "@event@.GetWaveformData().GetNumWaveforms()",
# Must handle data specially...
    #"nsample" : "",
    #"nele" : "", 
    #"data" : "", 
    #"nqele" : "", 
    #"qdata" : "", 
    }

ignored = [
   "iu1cl" ,
   "iu2cl" ,
   "iu3cl" ,
   "iu4cl" ,
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
    "ghcl" : "@event@.GetChargeCluster(%i).fIsGhost",    
    "tdcl" : "@event@.GetChargeCluster(%i).fIs3DCluster",    
    "fidcl" : "@event@.GetChargeCluster(%i).fIsFiducial",   
}
gang_info = {
    "csc" : "@event@.GetScintillationCluster(%i).GetGangInfo(%i).fCount",
    "cerrsc" : "@event@.GetScintillationCluster(%i).GetGangInfo(%i).fCountErr",
}
special_iu = [
]
not_yet_implemented = []

def compare(old, new, old_branch, new_branch, entry):
    if old != new and not (math.isnan(old) and math.isnan(new)):
        print '*'*60
        print old_branch, new_branch, entry
        print "old", old, "new", new
        print '*'*60

def compare_gang_info(branch, old, new_event, old_nsc):
    temp_str = gang_info[branch]  
    num_apds = 74
    i = 0
    total_num = 0
    for val in old:
        if (i/num_apds) >= old_nsc: continue 
        new_value =  eval((temp_str.replace("@event@", "new_event") % (i/num_apds, i%num_apds))) 
        compare(val, new_value, branch, str(i), str(old_nsc))
        i += 1
        

def compare_tref(branch, old, new_event, old_tree):
    # Unfortunately, have to do this by hand
    i = 0
    match_it = re.match("iu([0-9])clcs", branch)
    if branch == "usig_ichargecluster":
        for index in old: 
            uwire_signal = new_event.GetUWireSignal(i)
            charge_cluster = uwire_signal.GetChargeCluster()
            compare(old_tree.xcl[index], charge_cluster.fX, "usig_ichargecluster", "", "")
            compare(old_tree.ycl[index], charge_cluster.fY, "usig_ichargecluster", "", "")
            i += 1
    elif branch == "isccl":
        for index in old: 
            if index == -999: 
                i += 1
                continue
            charge_cluster = new_event.GetChargeCluster(i)
            scint_cluster = charge_cluster.GetScintillationCluster()
            if (index >= old_tree.nsc):
                # Means data was tossed by apreshap
                continue
            compare( old_tree.xsc[index], scint_cluster.fX, "isccl", "", "")
            compare( old_tree.ysc[index], scint_cluster.fY, "isccl", "", "")
            i += 1
    elif match_it:
        uwire_idx = int(match_it.group(1)) - 1
        # handle also the channels
        old_channels = getattr(old_tree, "iu%icl" % (uwire_idx+1) )
        for index, chan in zip(old, old_channels): 
            if index == -1: 
                i += 1
                continue
            charge_cluster = new_event.GetChargeCluster(i)
            uwire_signal = charge_cluster.GetUWireSignalAt(uwire_idx)
            compare(old_tree.usig_t[index], uwire_signal.fTime, branch, "", "")
            compare(old_tree.usig_e[index], uwire_signal.fEnergy, branch, "", "")
            compare(chan, charge_cluster.GetUWireSignalChannelAt(uwire_idx), "iu%icl" % (uwire_idx+1), "", "")
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
    limit = 1000
    #if limit < old_tree.GetEntries(): limit = old_tree.GetEntries()
    #old_tree.SetBranchStatus("*", 1)
    #new_tree.SetBranchStatus("*", 1)
    #new_tree.GetEntry(13)
    for i in range(old_tree.GetEntries()):
    #for i in range(4):
        old_tree.GetEntry(i)
        new_tree.GetEntry(i)
        if old_tree.ncl >= 99 or\
           old_tree.nusig >= 999 or\
           old_tree.nsc >= 99 or\
           old_tree.napd >= 99: continue 
        event = new_tree.EventBranch
        for branch in old_tree.GetListOfBranches():
            
            if branch.GetName() in tref_list:
                #if i == 13: pdb.set_trace()
                compare_tref(branch.GetName(), getattr(old_tree, branch.GetName()), event, old_tree) 
                continue
            if branch.GetName() in gang_info:
                compare_gang_info(branch.GetName(), getattr(old_tree, branch.GetName()), new_tree.EventBranch, old_tree.nsc) 
                continue
            if branch.GetName() in ignored:
                continue
            if branch.GetName() in special_bool.keys():
                aleaf = old_tree.GetBranch(branch.GetName()).GetListOfLeaves()[0]
                temp_str = special_bool[branch.GetName()]
                for j in range(old_tree.ncl):
                    temp = temp_str.replace("%i",str(j))
                    new_value =  eval(temp.replace("@event@", "event")) 
                    compare(aleaf.GetValue(j) > 0, new_value, branch.GetName(), temp, i)
                continue
            if branch.GetName() not in mapping_dict.keys():
                if branch.GetName() not in not_yet_implemented:
                    not_yet_implemented.append(branch.GetName())
                continue
            old_value = getattr(old_tree, branch.GetName())
            temp_str = mapping_dict[branch.GetName()]
            try:
                for j in range(len(old_value)):
                    temp = temp_str.replace("%i",str(j))
                    new_value =  eval(temp.replace("@event@", "event")) 
                    compare(old_value[j], new_value, branch.GetName(), temp, i)
            except TypeError:
                new_value =  eval(temp_str.replace("@event@", "event")) 
                compare(old_value, new_value, branch.GetName(), temp_str, i)
            

if __name__ == '__main__':
    ROOT.gSystem.Load("libEXOUtilities")
    first_file = ROOT.TFile.Open(sys.argv[1])
    second_file = ROOT.TFile.Open(sys.argv[2])
    compare_trees(first_file.Get("tree"), second_file.Get("tree")) 
    for branch in not_yet_implemented:
        print branch
