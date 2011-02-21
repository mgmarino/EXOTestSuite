import sys
import ROOT


def compare(old, new, attr):
    if old != new:
        print '*'*60
        print attr
        print old, new
        print '*'*60

def compare_trees(old_tree, new_tree):
    for i in range(old_tree.GetEntries()):
        print "Entry: ", i
        old_tree.GetEntry(i)
        new_tree.GetEntry(i)
        for branch in old_tree.GetListOfBranches():
            old_val = getattr(old_tree, branch.GetName())
            new_val = getattr(new_tree, branch.GetName())
            try:
                compare(len(old_val), len(new_val), branch.GetName()+ "len")
                for old, new in zip(old_val, new_val):
                    compare(old, new, branch.GetName())
 
            except TypeError:
                compare(old_val, new_val, branch.GetName())

           

if __name__ == '__main__':
    compare_trees(ROOT.TFile.Open(sys.argv[1]).Get("tree"), ROOT.TFile.Open(sys.argv[2]).Get("tree")) 
