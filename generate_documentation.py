import ROOT
import re


def generate_doc_for_object(obj, previous = ""):
    the_class = obj.IsA()
    list_of_everything = dir(obj)
    
    

    data_list = [(member, the_class.GetDataMember(member)) for member 
                  in list_of_everything if the_class.GetDataMember(member)]
    print previous, the_class.GetName() 
    for mem, data_mem in data_list:
        # clean up title
        print previous, "   ", mem, data_mem.GetTypeName(), data_mem.GetTitle()

if __name__ == '__main__':

    ROOT.gSystem.Load("libEXOUtilities")
    ed = ROOT.EXOEventData()
    generate_doc_for_object(ed)
    generate_doc_for_object(ed.GetWaveformData(), "   ")

