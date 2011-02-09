import sys
import re


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
    "errec" : "fTotalRawReconstructedEnergy", 
    "eprec" : "fTotalPurityCorrectedEnergy", 
    "ecrec" : "fTotalGridEfficiencyCorrectedReconstructedEnergy", 
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
    "idpart" : "fMonteCarloData.GetParticleInformation(%i)->fID", 
    "apart" :  "fMonteCarloData.GetParticleInformation(%i)->fAtomicNumber",  
    "epart" :  "fMonteCarloData.GetParticleInformation(%i)->fKineticEnergykeV",  
    "qpart" :  "fMonteCarloData.GetParticleInformation(%i)->fCharge",  
    "expart" : "fMonteCarloData.GetParticleInformation(%i)->fExcitedStatekeV", 


    "apd_hits" : "fMonteCarloData.GetAPDInfo(%i)->fNumHits", 
    "eapd" : "fMonteCarloData.GetAPDInfo(%i)->fEnergy",     
    "qapd" : "fMonteCarloData.GetAPDInfo(%i)->fCharge",     

    "ixq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i)->fX", 
    "iyq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i)->fY", 
    "izq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i)->fZ", 
    "etq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i)->fTotalEnergykeV", 
    "eiq" : "fMonteCarloData.GetPixelatedChargeDeposit(%i)->fTotalIonizationEnergykeV", 

    "c1sc" : "GetReconstructedScintillationCluster(%i)->fCountsOnAPDPlaneOne",       
    "c1errsc" : "GetReconstructedScintillationCluster(%i)->fCountsOnAPDPlaneOneError",    
    "c2sc" : "GetReconstructedScintillationCluster(%i)->fCountsOnAPDPlaneTwo",       
    "c2errsc" : "GetReconstructedScintillationCluster(%i)->fCountsOnAPDPlaneTwoError",    
    "c1sumsc" : "GetReconstructedScintillationCluster(%i)->fCountsSumOnAPDPlaneOne",    
    "c1sumerrsc" : "GetReconstructedScintillationCluster(%i)->fCountsSumOnAPDPlaneOneError", 
    "c2sumsc" : "GetReconstructedScintillationCluster(%i)->fCountsSumOnAPDPlaneTwo",    
    "c2sumerrsc" : "GetReconstructedScintillationCluster(%i)->fCountsSumOnAPDPlaneTwoError", 

    #"csc" : "GetReconstructedScintillationCluster(%i).GetGangInfo(%i).fCounts",
    #"cerrsc" : "GetReconstructedScintillationCluster(%i).GetGangInfo(%i).fCountsErr",
    #"chi2_APD1" : "GetReconstructedScintillationCluster(%i).fChiSquaredAPDOne",  
    #"chi2_APD2" : "GetReconstructedScintillationCluster(%i).fChiSquaredAPDTwo",  

    "xsc" : "GetReconstructedScintillationCluster(%i)->fX",        
    "ysc" : "GetReconstructedScintillationCluster(%i)->fY",        
    "zsc" : "GetReconstructedScintillationCluster(%i)->fZ",        
    "tsc" : "GetReconstructedScintillationCluster(%i)->fTime",        
    "rsc" : "GetReconstructedScintillationCluster(%i)->fRadius",        
    "esc" : "GetReconstructedScintillationCluster(%i)->fEnergy",        
    "algsc" : "GetReconstructedScintillationCluster(%i)->fAlgorithmUsed",      

    "xcl" : "GetReconstructedChargeCluster(%i)->fX",  
    "ycl" : "GetReconstructedChargeCluster(%i)->fY",  
    "ucl" : "GetReconstructedChargeCluster(%i)->fU",  
    "vcl" : "GetReconstructedChargeCluster(%i)->fV",  
    "zcl" : "GetReconstructedChargeCluster(%i)->fZ",  
    "dtcl" : "GetReconstructedChargeCluster(%i)->fDriftTime", 
    "tcl" : "GetReconstructedChargeCluster(%i)->fCollectionTime",  


    "ercl" : "GetReconstructedChargeCluster(%i)->fRawEnergy",   
    "eccl" : "GetReconstructedChargeCluster(%i)->fCorrectedEnergy",   
    "epcl" : "GetReconstructedChargeCluster(%i)->fPurityCorrectedEnergy",   
    "eerrcl" : "GetReconstructedChargeCluster(%i)->fCorrectedEnergyError", 
    "ncscl" : "GetReconstructedChargeCluster(%i)->fNumberOfCollectionSignals",   
    "iu1cl" : "GetReconstructedChargeCluster(%i)->fChannelNumberOfFirstSignal",   
    "iu2cl" : "GetReconstructedChargeCluster(%i)->fChannelNumberOfSecondSignal",   
    "iu3cl" : "GetReconstructedChargeCluster(%i)->fChannelNumberOfThirdSignal",   
    "iu4cl" : "GetReconstructedChargeCluster(%i)->fChannelNumberOfFourthSignal",   
    "nvchcl" : "GetReconstructedChargeCluster(%i)->fNumberOfVChannels",  
    "iv1cl" : "GetReconstructedChargeCluster(%i)->fVChannelNumberOne",   
    "iv2cl" : "GetReconstructedChargeCluster(%i)->fVChannelNumberTwo",   
    "dhalfcl" : "GetReconstructedChargeCluster(%i)->fDetectorHalf", 
    "evcl" : "GetReconstructedChargeCluster(%i)->fEnergyInVChannels",    
    "ghcl" : "GetReconstructedChargeCluster(%i)->fIsGhost",    
    "tdcl" : "GetReconstructedChargeCluster(%i)->fIs3DCluster",    
    "fidcl" : "GetReconstructedChargeCluster(%i)->fIsFiducial",   


    "nusig" : "GetNumReconstructedWires()",             
    "ncl" : "GetNumReconstructedChargeClusters()",             
    "nsc" : "GetNumReconstructedScintillationClusters()",             
    "usig_ch" : "GetReconstructedUWireSignal(%i)->fChannel",             
    "usig_e" : "GetReconstructedUWireSignal(%i)->fEnergy",              
    "usig_deltae" : "GetReconstructedUWireSignal(%i)->fEnergyError",         
    "usig_t" : "GetReconstructedUWireSignal(%i)->fTime",              
    "usig_deltat" : "GetReconstructedUWireSignal(%i)->fTimeError",         
    "usig_baseline" : "GetReconstructedUWireSignal(%i)->fBaseline",       
    "usig_deltabaseline" : "GetReconstructedUWireSignal(%i)->fBaselineError",  
    "usig_chi2" : "GetReconstructedUWireSignal(%i)->fChiSquare",           
    "nsig" : "GetWaveformData()->GetNumWaveforms()",

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
     
}
list_of_keys = [
    "nr",   
    "ne",   
    "fidev", 
    "bb0n", 
    "bb2n",  
    "alpha", 
    "nsite", 
    "errec", 
    "eprec", 
    "ecrec", 
    "depth", 
    "ecsum", 
    "header",        
    "svn_rev",       
    "build_id",      
    "compressionid", 
    "frameid",       
    "framerev",      
    "cc",            
    "trigcount",     
    "trigsec",       
    "trigsub",       
    "trigdrift",     
    "sn",            
    "sr",            
    "trigsum",       
    "in",            
    "ir",            
    "indsum",        
    "trigchan",      
    "trigoff",       
    "ebit",          
    "src",           
    "samplecount",   
    "g4ne",          
    "subne",         
    "is_mc",         
    "mcfid",         
    "muontag",            
    "muon_driftvelocity", 
    "muon_purity",       
    "muon_purity_err",    
    "qbeta", 
    "x0",    
    "y0",    
    "z0",    
    
    "totalph", 
    "hitsp1",  
    "hitsp2",  
    "esalt",                 
    "eshield",               
    "eoutcry",               
    "eincry",               
    "ehfe",                  
    "evessel",               
    "elxet",                 
    "elxei",                 
    "ecathode_photons",      
    "eanodes_photons",       
    "ewire_supports_photons",
    "ecathode_ring_photons", 
    "ereflector_photons",    
    "eapd_frames_photons",   
    "elxe_photons",          
    "evessel_photons",       
    "eremoved_apds_photons", 
    "efield_rings_photons",  
    "npart",
    "nq",
    "napd",
    "idpart", 
    "apart",  
    "epart",  
    "qpart",  
    "expart", 


    "apd_hits", 
    "eapd",     
    "qapd",     

    "ixq", 
    "iyq", 
    "izq", 
    "etq", 
    "eiq", 

    "c1sc",       
    "c1errsc",    
    "c2sc",       
    "c2errsc",    
    "c1sumsc",    
    "c1sumerrsc", 
    "c2sumsc",    
    "c2sumerrsc", 

    #"csc",
    #"cerrsc",
    #"chi2_APD1",  
    #"chi2_APD2",  

    "xsc",        
    "ysc",        
    "zsc",        
    "tsc",        
    "rsc",        
    "esc",        
    "algsc",      

    "xcl",  
    "ycl",  
    "ucl",  
    "vcl",  
    "zcl",  
    "dtcl", 
    "tcl",  


    "ercl",   
    "eccl",   
    "epcl",   
    "eerrcl", 
    "ncscl",   
    "iu1cl",   
    "iu2cl",   
    "iu3cl",   
    "iu4cl",   
    "nvchcl",  
    "iv1cl",   
    "iv2cl",   
    "dhalfcl", 
    "evcl",    
    "ghcl",    
    "tdcl",    
    "fidcl",   


    "nusig",             
    "ncl",             
    "nsc",             
    "usig_ch",             
    "usig_e",              
    "usig_deltae",         
    "usig_t",              
    "usig_deltat",         
    "usig_baseline",       
    "usig_deltabaseline",  
    "usig_chi2",           
    "nsig",

    "compton_e",
    "compton_fom",
    "compton_ncl",
    "compton_phi",
    "compton_phi_err",
    "compton_x1",
    "compton_y1",
    "compton_z1",
    "compton_dx1",
    "compton_dy1",
    "compton_dz1",
    "compton_x2",
    "compton_y2",
    "compton_z2",
    "compton_dx2",
    "compton_dy2",
    "compton_dz2",
] 


not_yet_implemented = []
if __name__ == '__main__':
    for initial in list_of_keys: 
        final = mapping_dict[initial]
        match_it = re.match("(.*)\(%i\)(.*)", final) 
        if match_it: 
            print "  ed_new->%s(i)%s = ed_old->%s[i];" % (match_it.group(1), match_it.group(2), initial) 
        else:
            print "  ed_new->%s = ed_old->%s;" % (final, initial)