import ROOT
import re


boundary_limit = 100

def generate_doc_for_object(obj, previous = ""):
    the_class = obj.IsA()
    list_of_everything = dir(obj)
    
    

    data_list = [(member, the_class.GetDataMember(member)) for member 
                  in list_of_everything if the_class.GetDataMember(member)]
    output = previous + '*'*10 + ' ' + the_class.GetName()
    print output + '*'*(boundary_limit - len(output)) 
    get_members = [getattr(obj, aname)() for aname in list_of_everything
                  if re.match("GetNew.*", aname)]
    to_be_created = []
    for mem, data_mem in data_list:
        # clean up title
        if re.match("EXO.*", data_mem.GetTypeName()):
            to_be_created.append(getattr(ROOT, data_mem.GetTypeName()))
            continue
        title = data_mem.GetTitle()
        title = re.sub('\s{3,}', ' ', title)
        temp = title.split(':')
        old_value = ''
        new_value = temp[0]
        if len(temp) > 1:
            old_value = temp[0]
            new_value = temp[1]
        print "%s%s%-40s  %-15s  %-10s %-70s" % (previous, "   ", mem, data_mem.GetTypeName(), old_value, new_value)
    for amem in to_be_created: generate_doc_for_object(amem(), previous + "   ")
    for amem in get_members: generate_doc_for_object(amem, previous + "   ")
    print previous + '*'*(boundary_limit - len(previous))

if __name__ == '__main__':

    ROOT.gSystem.Load("libEXOUtilities")
    ed = ROOT.EXOEventData()
    generate_doc_for_object(ed)
    generate_doc_for_object(ed.GetWaveformData(), "   ")

