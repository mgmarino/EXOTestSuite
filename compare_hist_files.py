import sys
import ROOT
import numpy


def compare_hist(old_hist, new_hist):
    if old_hist.GetEntries() == 0 and new_hist.GetEntries() == 0: return
    old = numpy.ndarray((old_hist.GetBufferSize(),), buffer=old_hist.GetBuffer(), dtype=float)
    new = numpy.ndarray((new_hist.GetBufferSize(),), buffer=new_hist.GetBuffer(), dtype=float)

    if (old - new).sum() != 0: 
        print "Error", old_hist.GetName()
def compare_files(old_file, new_file):
    i = 0
    total = len(old_file.GetListOfKeys())
    for old_key, new_key in zip(old_file.GetListOfKeys(), new_file.GetListOfKeys() ): 
        print i, total
        compare_hist( old_file.Get(old_key.GetName()), new_file.Get(new_key.GetName()))
        i += 1

if __name__ == '__main__':
    compare_files(ROOT.TFile.Open(sys.argv[1]), ROOT.TFile.Open(sys.argv[2])) 
