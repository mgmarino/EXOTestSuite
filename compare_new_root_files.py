import sys
import re
import ROOT
import math
import ctypes


obj_list = [ "fCompton", "fEventHeader", "fMonteCarloData" ]
ignore = ['fBuildID', 'GetNumAPDHits', 'fCompressionID']
#ignore = ['fBuildID', 'GetNumAPDSignals', 'fCompressionID']

def compare(old, new, attr):
    if old != new:
        print '*'*60
        print attr
        print old, new
        print '*'*60

def compare_object(old, new):
    for anattr in dir(new): 
        if anattr in ignore: continue
        if anattr in obj_list:
            compare_object(getattr(old, anattr), getattr(new, anattr))
        elif re.match("f.*", anattr): 
            compare(getattr(old, anattr), getattr(new, anattr), anattr)
        elif re.match("Get.*", anattr):
            if re.match("GetNew.*", anattr): continue
            elif re.match("GetNum.*", anattr): 
                compare(getattr(old, anattr)(), getattr(new, anattr)(), anattr)
            elif re.match("Get.*Array.*", anattr): 
                old_arr, new_arr = (getattr(old, anattr)(), getattr(new, anattr)())
                if old_arr.GetEntriesFast() != new_arr.GetEntriesFast():
                    continue
                    print anattr
                for old_obj, new_obj in zip(old_arr, new_arr):
                    compare_object(old_obj, new_obj)

def compare_trees(old_tree, new_tree):
    for i in range(old_tree.GetEntries()):
        print "Entry: ", i
        old_tree.GetEntry(i)
        new_tree.GetEntry(i)
        old_event = old_tree.EventBranch
        new_event = new_tree.EventBranch
        compare_object( old_event, new_event)
           

if __name__ == '__main__':
    ROOT.gSystem.Load("libEXOUtilities")
    print "First try..."
    compare_trees(ROOT.TFile.Open(sys.argv[1]).Get("tree"), ROOT.TFile.Open(sys.argv[2]).Get("tree")) 
