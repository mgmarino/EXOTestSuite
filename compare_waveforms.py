import sys
import re
import ROOT
import math
import ctypes
import pdb


ignored = [
   "chan",
   "nsample",
   "nele",
   "data",
   "nqele",
   "qdata",
   "nsig",
   ]
def compare(old, new, old_branch, new_branch, entry):
    if old != new and not (math.isnan(old) and math.isnan(new)):
        print '*'*60
        print old_branch, new_branch, entry
        print "old", old, "new", new
        print '*'*60

def compare_trees(old_tree, new_tree):
    for i in range(old_tree.GetEntries()):
    #for i in range(4):
        old_tree.GetEntry(i)
        new_tree.GetEntry(i)
        if old_tree.ncl >= 99 or\
           old_tree.nusig >= 999 or\
           old_tree.nsc >= 99 or\
           old_tree.napd >= 99: continue 
        wf_data = new_tree.EventBranch.GetWaveformData()
        nsamp = old_tree.nsample 
        for chan in old_tree.chan: 
            wf = wf_data.GetWaveformAtChannel(chan) 
            if not wf: 
                print "Error", chan
                continue
            
           

if __name__ == '__main__':
    ROOT.gSystem.Load("libEXOUtilities")
    first_file = ROOT.TFile.Open(sys.argv[1])
    second_file = ROOT.TFile.Open(sys.argv[2])
    compare_trees(first_file.Get("tree"), second_file.Get("tree")) 
