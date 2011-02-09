import sys
import os.path
import pyexo
import ROOT
import traceback

class EXOParseToNewEXOEventData(pyexo.EXOAnalysisModule):
    """
    An example of how one might subclass an EXOAnalysisModule in python
    You absolutely don't have to use anything you won't need, and
    of course you can add additional functions as necessary.
    This class is defined here, but normally you would define the class
    in a separate module (i.e. a separate .py file) and import it. 
    """
    """
      Not yet implemented
    
      i_charge_cluster
      // Reconstructed scintillation signals
    
      double        csc[MAXSC*MAXNAPD]   //[nphe]
      double        cerrsc[MAXSC*MAXNAPD]   //[nphe]
    
      double        chi2_APD_gang[MAXNAPD]   //[napd]
      double        thsc     
      double        sssc     
      double        ssc     
      double        esc     
      // Compton-Cone Reconstructed info
    
      int           compton_ncl
      double        compton_x1
      double        compton_y1
      double        compton_z1
      double        compton_dx1
      double        compton_dy1
      double        compton_dz1
      double        compton_x2
      double        compton_y2
      double        compton_z2
      double        compton_dx2
      double        compton_dy2
      double        compton_dz2
      double        compton_phi
      double        compton_phi_err
      double        compton_e
      double        compton_fom
     
    """


    # class variable 
    output_filename = "temp.root"
    def set_name_of_output_file(self, name): self.output_filename = name 

    def BeginOfRun(self, ED):
        something = 0
        self.event_num = 0
        try:
            something = self.MyRun( ED )
        except:
            print "*"*60
            traceback.print_exc()
            print "*"*60
            sys.exit(1)
        return something

    def MyRun(self, ED):
        print "Beginning Run"
        self.afile = ROOT.TFile( self.output_filename, "recreate" )
        self.afile.SetCompressionLevel( 4 )
        self.tree  = ROOT.TTree( "EXOEventDataTree", "Event Data For EXO" ) 
        self.tree.SetMaxVirtualSize(200*1000*1000)
        #self.tree.BranchRef()

        #self.awffile = ROOT.TFile( self.output_filename[:-5] + 'waveforms.root', "recreate" )
        #self.awffile.SetCompressionLevel( 4 )
        #self.wftree  = ROOT.TTree( "EXOWaveformDataTree", "Waveform Data for EXO" ) 
        #self.wftree.BranchRef()

        self.new_eventdata = ROOT.EXOEventData()
        self.new_waveform_data = ROOT.EXOWaveformData()

        self.tree.Branch("EventBranch", self.new_eventdata )
        self.new_eventdata.SetTree( self.tree )
        self.tree.Branch("WaveformBranch", self.new_waveform_data )

        self.new_info = ROOT.EXOFileInfo("EXOTreeFileData", "EXOTreeFileData")
        #self.new_info.GetWaveformFile().AddUrl( self.awffile.GetName() )
        self.new_info.GetEventDataFile().AddUrl( self.afile.GetName() )

        self.tree.GetUserInfo().Add( self.new_info )
        #self.wftree.GetUserInfo().Add( self.new_info )
        print "Initialization done"
        return 0


    def BeginOfEvent(self, ED):
        something = 0
        try:
            something = self.MyEvent( ED )
        except:
            print "*"*60
            traceback.print_exc()
            print "*"*60
            sys.exit(2)
        return something
    def MyEvent(self, ED):
        self.event_num += 1
        self.new_eventdata.Clear()        
        self.new_waveform_data.Clear()        

        self.new_waveform_data.SetEventData( self.new_eventdata )
        self.new_eventdata.SetWaveformData( self.new_waveform_data )

        header = self.new_eventdata.fEventHeader
        header.fHeaderString = ED.header
        header.fSVNRevision = ED.svn_rev
        header.fBuildID = ED.build_id
        header.fRunNumber = ED.nr
        header.fEventNumber = ED.ne
        header.fCompressionID = ED.compressionid
        header.fFrameID = ED.frameid
        header.fFrameRevision = ED.framerev
        header.fCardCount = ED.cc
        header.fTriggerCount = ED.trigcount
        header.fTriggerSeconds = ED.trigsec
        header.fTriggerMicroSeconds = ED.trigsub
        header.fTriggerDrift = ED.trigdrift
        header.fSumTriggerThreshold = ED.sn
        header.fSumTriggerRequest = ED.sr
        header.fSumTriggerValue = ED.trigsum
        header.fIndividualTriggerThreshold = ED._in
        header.fIndividualTriggerRequest = ED.ir
        header.fMaxValueChannel = ED.indsum
        header.fOfflineTriggerChannel = ED.trigchan
        header.fTriggerOffset = ED.trigoff
        header.fFrameIsEmpty = ED.ebit
        header.fTriggerSource = ED.src
        header.fSampleCount = ED.samplecount

        header.fGeant4EventNumber = ED.g4ne
        header.fGeant4SubEventNumber = ED.subne
        header.fIsMonteCarloEvent = ED.is_mc
        header.fTaggedAsMuon =      ED.muontag
        header.fMuonDriftVelocity = ED.muon_driftvelocity
        header.fMuonPurity =      ED.muon_purity
        header.fMuonPurityError = ED.muon_purity_err
        header.fMonteCarloFiducialFlag = ED.mcfid

        mc_data = self.new_eventdata.fMonteCarloData

        for idpart, epart, qpart, apart, expart in zip( ED.get_idpart_as_ndarray(),
                                                        ED.get_epart_as_ndarray(), 
                                                        ED.get_qpart_as_ndarray(), 
                                                        ED.get_apart_as_ndarray(), 
                                                        ED.get_expart_as_ndarray() 
                                                        ):
            part_info = mc_data.GetNewParticleInformation()
            part_info.fParticleID = idpart 
            part_info.fParticleAtomicNumber = apart   
            part_info.fParticleKineticEnergykeV = epart
            part_info.fParticleCharge = qpart 
            part_info.fParticleExcitedStatekeV = expart  

        mc_data.fBetaDecayQValue      = ED.qbeta                           
        mc_data.fPrimaryEventX        = ED.x0                                                                     
        mc_data.fPrimaryEventY        = ED.y0                                                                     
        mc_data.fPrimaryEventZ        = ED.z0                                                                     
        mc_data.fTotalPhotons         = ED.totalph                                                               
        mc_data.fTotalHitsArrayOne    = ED.hitsp1                                                                  
        mc_data.fTotalHitsArrayTwo    = ED.hitsp2                           	     	     	     	
        mc_data.fTotalEnergyInSalt                        = ED.esalt
        mc_data.fTotalEnergyInLead                        = ED.eshield
        mc_data.fTotalEnergyInOuterCryostat               = ED.eoutcry
        mc_data.fTotalEnergyInInnerCryostat               = ED.eincry
        mc_data.fTotalEnergyInHFE                         = ED.ehfe
        mc_data.fTotalEnergyInTPC                         = ED.evessel
        mc_data.fTotalEnergyInLiquidXe                    = ED.elxet
        mc_data.fTotalIonizationEnergyInLiquidXe          = ED.elxei
        mc_data.fTotalEnergyOptPhotonsInCathode           = ED.ecathode_photons
        mc_data.fTotalEnergyOptPhotonsInBothAnodes        = ED.eanodes_photons
        mc_data.fTotalEnergyOptPhotonsInBothWireSupports  = ED.ewire_supports_photons
        mc_data.fTotalEnergyOptPhotonsInCathodeRing       = ED.ecathode_ring_photons
        mc_data.fTotalEnergyOptPhotonsInTeflonReflector   = ED.ereflector_photons
        mc_data.fTotalEnergyOptPhotonsInBothAPDFrames     = ED.eapd_frames_photons
        mc_data.fTotalEnergyOptPhotonsInLiquidXe          = ED.elxe_photons
        mc_data.fTotalEnergyOptPhotonsInLiquidXeVessel    = ED.evessel_photons
        mc_data.fTotalEnergyOptPhotonsInRemovedAPDs       = ED.eremoved_apds_photons
        mc_data.fTotalEnergyOptPhotonsInFieldShapingRings = ED.efield_rings_photons


        for ixq, iyq, izq, etq, eiq in zip( ED.get_ixq_as_ndarray(),
                                            ED.get_iyq_as_ndarray(), 
                                            ED.get_izq_as_ndarray(), 
                                            ED.get_etq_as_ndarray(), 
                                            ED.get_eiq_as_ndarray() ): 
            pixelated_charge = mc_data.GetNewPixelatedChargeDeposit()
            pixelated_charge.fX                        = ixq  
            pixelated_charge.fY                        = iyq  
            pixelated_charge.fZ                        = izq  
            pixelated_charge.fTotalEnergykeV           = etq               
            pixelated_charge.fTotalIonizationEnergykeV = eiq                         

      

        for apd_hits, eapd, qapd in zip( ED.get_apd_hits_as_ndarray(),
                                         ED.get_eapd_as_ndarray(), 
                                         ED.get_qapd_as_ndarray()) :
            apd = mc_data.GetNewAPDInfo()
            apd.fAPDHits   = apd_hits
            apd.fAPDEnergy = eapd
            apd.fAPDCharge = qapd


        reference_for_charge_cluster = {}

        list_of_uwire = []
        for usig_ch, usig_e, usig_deltae, usig_t, usig_deltat, \
            usig_baseline, usig_deltabaseline, usig_chi2, \
            usig_ichargecluster in zip( ED.get_usig_ch_as_ndarray(),
                                        ED.get_usig_e_as_ndarray(),
                                        ED.get_usig_deltae_as_ndarray(),
                                        ED.get_usig_t_as_ndarray(),
                                        ED.get_usig_deltat_as_ndarray(),
                                        ED.get_usig_baseline_as_ndarray(),
                                        ED.get_usig_deltabaseline_as_ndarray(),
                                        ED.get_usig_chi2_as_ndarray(),
                                        ED.get_usig_ichargecluster_as_ndarray() ):
             new_uwire_info = self.new_eventdata.GetNewReconstructedUWireSignal()
             new_uwire_info.fChannel 	   = usig_ch	    
             new_uwire_info.fEnergy 	   = usig_e		    	
             new_uwire_info.fEnergyError   = usig_deltae	    	
             new_uwire_info.fTime 	   = usig_t		    	
             new_uwire_info.fTimeError 	   = usig_deltat	    
             new_uwire_info.fBaseline 	   = usig_baseline	    
             new_uwire_info.fBaselineError = usig_deltabaseline 
             new_uwire_info.fChiSquare     = usig_chi2 
             reference_for_charge_cluster[ usig_ichargecluster ] =  new_uwire_info
             list_of_uwire.append( new_uwire_info )
 
       # The usig_ichargecluster is a number, we need to convert to a reference 

        reference_for_scintillation_cluster = {}
        i = 0
        for ercl, eccl, epcl, eerrcl, xcl, ycl, ucl, vcl, zcl, tcl, dtcl, \
            isccl, ncscl, iu1clcs, iu1cl, iu2clcs, iu2cl, iu3clcs, iu3cl, \
            iu4clcs, iu4cl, nvchcl, iv1cl, iv2cl, dhalfcl, evcl, ghcl, \
            tdcl, fidcl in zip( ED.get_ercl_as_ndarray(),
                                ED.get_eccl_as_ndarray(), 
                                ED.get_epcl_as_ndarray(), 
                                ED.get_eerrcl_as_ndarray(), 
                                ED.get_xcl_as_ndarray(), 
                                ED.get_ycl_as_ndarray(), 
                                ED.get_ucl_as_ndarray(), 
                                ED.get_vcl_as_ndarray(), 
                                ED.get_zcl_as_ndarray(), 
                                ED.get_tcl_as_ndarray(), 
                                ED.get_dtcl_as_ndarray(), 
                                ED.get_isccl_as_ndarray(), 
                                ED.get_ncscl_as_ndarray(), 
                                ED.get_iu1clcs_as_ndarray(), 
                                ED.get_iu1cl_as_ndarray(), 
                                ED.get_iu2clcs_as_ndarray(), 
                                ED.get_iu2cl_as_ndarray(), 
                                ED.get_iu3clcs_as_ndarray(), 
                                ED.get_iu3cl_as_ndarray(), 
                                ED.get_iu4clcs_as_ndarray(), 
                                ED.get_iu4cl_as_ndarray(), 
                                ED.get_nvchcl_as_ndarray(), 
                                ED.get_iv1cl_as_ndarray(), 
                                ED.get_iv2cl_as_ndarray(), 
                                ED.get_dhalfcl_as_ndarray(), 
                                ED.get_evcl_as_ndarray(), 
                                ED.get_ghcl_as_ndarray(), 
                                ED.get_tdcl_as_ndarray(), 
                                ED.get_fidcl_as_ndarray() ):
                 new_charge_cluster = self.new_eventdata.GetNewReconstructedChargeCluster()
        
                 new_charge_cluster.fRawEnergy                 = ercl       
                 new_charge_cluster.fCorrectedEnergy           = eccl       
                 new_charge_cluster.fPurityCorrectedEnergy     = epcl       
                 new_charge_cluster.fCorrectedEnergyError      = eerrcl       
                 new_charge_cluster.fX                         = xcl          
                 new_charge_cluster.fY                         = ycl          
                 new_charge_cluster.fZ                         = zcl          
                 new_charge_cluster.fU                         = ucl          
                 new_charge_cluster.fV                         = vcl          
                 new_charge_cluster.fCollectionTime            = tcl      
                 new_charge_cluster.fDriftTime                 = dtcl      
                 new_charge_cluster.fNumberOfCollectionSignals = ncscl     
        
                 reference_for_scintillation_cluster[ isccl ] = new_charge_cluster
                 # setting the pointer
                 if i in reference_for_charge_cluster.keys(): 
                     reference_for_charge_cluster[i].SetChargeCluster( new_charge_cluster )
                 i += 1
                 
                 new_charge_cluster.fChannelNumberOfFirstSignal   = iu1cl     
                 new_charge_cluster.fChannelNumberOfSecondSignal  = iu2cl     
                 new_charge_cluster.fChannelNumberOfThirdSignal   = iu3cl    
                 new_charge_cluster.fChannelNumberOfFourthSignal  = iu4cl    
                 if iu1clcs >= 0 and iu1clcs <  len( list_of_uwire ):
                     new_charge_cluster.SetUSignalOfFirstSignal( list_of_uwire[iu1clcs] )
                 if iu2clcs >= 0 and iu2clcs <  len( list_of_uwire ):
                     new_charge_cluster.SetUSignalOfSecondSignal( list_of_uwire[iu2clcs] )   
                 if iu3clcs >= 0 and iu3clcs <  len( list_of_uwire ):
                     new_charge_cluster.SetUSignalOfThirdSignal( list_of_uwire[iu3clcs] )
                 if iu4clcs >= 0 and iu4clcs <  len( list_of_uwire ):
                     new_charge_cluster.SetUSignalOfFourthSignal( list_of_uwire[iu4clcs]  )  
                 new_charge_cluster.fNumberOfVChannels = nvchcl 
                 new_charge_cluster.fVChannelNumberOne = iv1cl   
                 new_charge_cluster.fVChannelNumberTwo = iv2cl   
                 new_charge_cluster.fDetectorHalf      = dhalfcl
                 new_charge_cluster.fEnergyInVChannels = evcl     
        
                 new_charge_cluster.fIsGhost           = ghcl 
                 new_charge_cluster.fIs3DCluster       = tdcl     
                 new_charge_cluster.fIsFiducial        = fidcl  


        i = 0
        for c1sc, c1errsc, c2sc, c2errsc, algsc, \
            c1sumsc, c1sumerrsc, c2sumsc, c2sumerrsc, \
            xsc, ysc, zsc, tsc, rsc, thsc, sssc, ssc, esc  in zip(
              ED.get_c1sc_as_ndarray(),   
              ED.get_c1errsc_as_ndarray(),   
              ED.get_c2sc_as_ndarray(),   
              ED.get_c2errsc_as_ndarray(),   
              ED.get_algsc_as_ndarray(),   
              ED.get_c1sumsc_as_ndarray(),   
              ED.get_c1sumerrsc_as_ndarray(),   
              ED.get_c2sumsc_as_ndarray(),   
              ED.get_c2sumerrsc_as_ndarray(),   
              ED.get_xsc_as_ndarray(),   
              ED.get_ysc_as_ndarray(),   
              ED.get_zsc_as_ndarray(),   
              ED.get_tsc_as_ndarray(),   
              ED.get_rsc_as_ndarray(),   
              ED.get_thsc_as_ndarray(),   
              ED.get_sssc_as_ndarray(),   
              ED.get_ssc_as_ndarray(),   
              ED.get_esc_as_ndarray() ):  

            new_scintillation_cluster = self.new_eventdata.GetNewReconstructedScintillationCluster()     
            new_scintillation_cluster.fCountsOnAPDPlaneOne     = c1sc    
            new_scintillation_cluster.fCountsOnAPDPlaneOneError= c1errsc 
            new_scintillation_cluster.fCountsOnAPDPlaneTwo     = c2sc    
            new_scintillation_cluster.fCountsOnAPDPlaneTwoError= c2errsc 
            new_scintillation_cluster.fAlgorithmUsed           = algsc   
            new_scintillation_cluster.fChiSquaredAPDOne = ED.chi2_APD1
            new_scintillation_cluster.fChiSquaredAPDTwo = ED.chi2_APD2
            new_scintillation_cluster.fCountsSumOnAPDPlaneOne     = c1sumsc    
            new_scintillation_cluster.fCountsSumOnAPDPlaneOneError= c1sumerrsc 
            new_scintillation_cluster.fCountsSumOnAPDPlaneTwo     = c2sumsc    
            new_scintillation_cluster.fCountsSumOnAPDPlaneTwoError= c2sumerrsc 
            new_scintillation_cluster.fX         = xsc
            new_scintillation_cluster.fY         = ysc
            new_scintillation_cluster.fZ         = zsc
            new_scintillation_cluster.fTime      = tsc
            new_scintillation_cluster.fRadius    = rsc
            # setting the pointer
            if i in reference_for_scintillation_cluster.keys(): 
                reference_for_scintillation_cluster[i].SetScintillationCluster( new_scintillation_cluster )
            i += 1

        self.new_eventdata.fIsFiducialEvent = ED.fidev                                                                           
        self.new_eventdata.fNumberOfSites   = ED.nsite                                  
        self.new_eventdata.fIsbb0nCandidate = ED.bb0n                                                                            
        self.new_eventdata.fIsbb2nCandidate = ED.bb2n                                                                            
        self.new_eventdata.fIsAlphaCandidate = ED.alpha                                         
        self.new_eventdata.fTotalRawReconstructedEnergy                     = ED.errec 
        self.new_eventdata.fTotalGridEfficiencyCorrectedReconstructedEnergy = ED.ecrec              
        self.new_eventdata.fTotalPurityCorrectedEnergy = ED.eprec              
        self.new_eventdata.fDepth                                           = ED.depth    
        self.new_eventdata.fCorrectedEnergySum                              = ED.ecsum 
                      
        anarray              = ED.get_data_as_ndarray()
        num_per_event        = ED.nele/ED.nsig
        work_with            = anarray.reshape(-1, num_per_event)
        for chan, waveform in zip( ED.get_chan_as_ndarray(), work_with ):
            new_waveform = self.new_waveform_data.GetNewWaveform()
            new_waveform.fChannel = chan
            new_waveform.SetData( waveform, len(waveform) )
            new_waveform.Compress()


        self.tree.Fill()
        #self.wftree.Fill()
        #if self.event_num > 10000: return -1
        return 0

    def ShutDown(self):
        print "  Finishing Up writing to:", self.output_filename
        self.afile = self.tree.GetCurrentFile()
        self.afile.cd()
        self.tree.Write("", ROOT.TObject.kOverwrite)

        
        #self.awffile.cd()
        #self.wftree.Write("", ROOT.TObject.kOverwrite)

        self.afile.Close()
        #self.awffile.Close()
        return 0


def run_analysis(list_of_input_files, output_file):
    """ 
    This is an example analysis script that one might write.
    It essentially replaces EXOAnalysis.cc, the idea here for
    this example is to be as simple as possible.  In particular,
    registration of modules is streamlined. 
    """
   
    # Loop over the input files"
    for input_file in list_of_input_files:
        #############################################
        # The analysis manager handles all the basic 
        # instantiations that must happen for initialization.        
        # In general for quick, one-off analyses, the
        # internals will not be important.
        analysis_mgr = pyexo.PyEXOOfflineManager()

        # mgr is an EXOAnalysisManager instance
        mgr = analysis_mgr.get_analysis_mgr()
        #############################################
        
        #############################################
        # Now instantiate our modules:
        #
        # First a compiled module distributed by
        # EXOAnalysis:
        # Then a module we defined above:
        wf_analysis = EXOParseToNewEXOEventData(mgr)
        #############################################


        #############################################
        # Now we register the modules.  Note, that
        # the order of registration is important
        # as the modules will be called in this
        # order in the analysis loop.
        # The name given is just a nickname, 
        mgr.UseModule("input")
        analysis_mgr.register_module(wf_analysis, "example")
        mgr.ShowRegisteredModules()
        #############################################
 
        #############################################
        # Setting the base file name from the input
        # (presumably ROOt) file:
        wf_analysis.set_name_of_output_file(output_file)
        #############################################

        print "Reading from file: ", input_file
        print "  Outputting to: ", output_file
        #############################################

        #############################################
        # Setting the input filename
        # Since we selected the EXOTreeInputModule above,
        # this should be a ROOT file
        analysis_mgr.set_filename(input_file)
        #############################################


        #############################################
        # Go, actually do the analysis
        analysis_mgr.run_analysis()
        print "Done..."
        #############################################

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "Usage: [output_file] [files_to_parse]"
        sys.exit(1)
    ROOT.gROOT.SetBatch()
    ROOT.gApplication.ExecuteFile("LoadEXClasses.C");
    run_analysis(sys.argv[2:], sys.argv[1])
