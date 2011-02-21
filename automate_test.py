from subprocess import Popen, PIPE, STDOUT 
import os
path_to_exo = "/home/mgmarino/software/bin/EXOAnalysis"
path_to_old_exo = "/home/mgmarino/software/clean/bin/EXOAnalysis"
input_file = "/exo/scratch1/951_old_canon.root" 
#input_file = "/exo/scratch2/raw_data_test/951/run00000951-000.dat" 
test_script = "/home/mgmarino/tmp/EXOTestSuite/compare_root_files.py"
test_objs = {
    "EXOATeamComptonModule" : ("acompton", [  ]),
#    "EXOATeamELifeModule" : ("aelife", [  ]),
    "EXOATeamFilterModule" : ("afilter", [  ]),
    "EXOATeamMuonTagModule" : ("amutag", [  ]),
    "EXOAPDCentroid" : ("apd_centroid", [ "/apd_centroid/outfile @OUT@temp.root"]),
    "EXOATeamAPDReshaperModule" : ("apreshap", ["/apreshap/overwriteSignal",
                                                "/toutput/writeSignals",
                                                "maxevents 1000"]),
    "EXOATeamPurityCorrModule" : ("apurcorr", [  ]),
    "EXOATeamSoftwareTrigModule" : ("asofttrig", [  ]),
    "EXODriftVelocityModule" : ("dveloc", ["/driftvelocity/output_file @OUT@temp.root" ]),
#    "EXOEventDumpModule" : ("eventdump", [  ]),
#    "EXOLifetimeCalibModule" : ("lifecalib", [  ]),
    "EXOMuonTrackFinder" : ("muontrack", [  "/muontrack/nwirecounts 80",
                                            "/muontrack/minlightdt 0",
                                            "/muontrack/napdcounts 5000",
                                            "/muontrack/driftspeed 1.9"]),
    "EXOSumModule" : ("sum", [  ]),
    "EXOTriggerModule" : ("trig", ["/trig/overwrite"]),
    "EXODataTrimModule" : ("trim", [  ]),
    "EXOATeamUWireCorrModule" : ("ucor", [  ]),
}
#test_objs = {
#    "EXODriftVelocityModule" : "dveloc",
#}

def do_job(module_name="", extratext = []):

    test_dir = "test_" + module_name
    if os.path.exists(test_dir): return
    os.mkdir(test_dir)
    os.chdir(test_dir)
    output_text = """
use input %s toutput
/input/file %s
""" % (module_name, input_file)
    append = ""
    for text in extratext: 
        append += "%s\n" % text
    append += """
%maxevents 2
printmodulo 1000
show
begin
exit
"""

    jobs = []
    for tag, job in [("new" + module_name, path_to_exo), ("old" + module_name, path_to_old_exo)]: 
        final_text = """
%s
/toutput/file %s.root 
""" % (output_text, tag)
        final_text += append
        final_text = final_text.replace("@OUT@", tag)
        print final_text, job
        p = Popen(job, stdin=PIPE, stdout=PIPE, stderr=STDOUT) 
        p.stdin.write(final_text)
        print p.pid
        jobs.append((p, tag))

    for p, tag in jobs:
        comm = p.communicate()
        open("%s.out" % tag, "w").write(comm[0])
        if p.returncode != 0:
            print "error", p.pid
        
    print "Comparison********************" 
    p = Popen(['python', test_script, "old%s.root" % module_name, "new%s.root" % module_name], stdin=PIPE, stdout=PIPE, stderr=STDOUT) 
    open("compare_"+module_name, "w").write(p.communicate()[0])

if __name__=='__main__':
    for name, val in test_objs.items(): 
        mod, lis = val
        cwd = os.getcwd()
        print "Doing: ", name
        do_job(mod, lis)
        os.chdir(cwd)
