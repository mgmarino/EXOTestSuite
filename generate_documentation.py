import ROOT
import re
import datetime



list_type = """<ul style="list-style-type:none;">"""
base_url = "http://dl.dropbox.com/u/979314/htmldoc/"
def generate_doc_for_object(obj, previous = ""):
    the_class = obj.IsA()
    list_of_everything = dir(obj)
    
    

    data_list = [(member, the_class.GetDataMember(member)) for member 
                  in list_of_everything if the_class.GetDataMember(member)]
    output = previous + '*'*10 + ' ' + the_class.GetName()
    print """<li><a href="%s%s.html">%s</a></li>""" % (base_url, the_class.GetName(), previous + the_class.GetName())
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
        #print "%s%s%-40s  %-15s  %-10s %-70s" % (previous, "   ", mem, data_mem.GetTypeName(), old_value, new_value)
    if len(to_be_created)==0 and len(get_members)==0: return
    print list_type 
    for amem in to_be_created: generate_doc_for_object(amem(), previous + "   ")
    for amem in get_members: generate_doc_for_object(amem, previous + "   ")
    print "</ul>"

if __name__ == '__main__':

    ROOT.gSystem.Load("libEXOUtilities")
    ed = ROOT.EXOEventData()
    print """
<html>
<body>
<p>EXOEventData tree-structure, auto-generated on (UTC) %s</p>
%s
    """ % (str(datetime.datetime.utcnow()), list_type)
    generate_doc_for_object(ed)
    generate_doc_for_object(ed.GetWaveformData(), "   ")
print """
</ul>
</body>
</html>
"""

