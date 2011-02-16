import ROOT
import re
import datetime
"""
<style type="text/css">
div{ color: gray; }
div.hidden {
  display:none;
}
</style>
<script type="text/javascript">
 function unhide(divID) {
 var item = document.getElementsByName(divID);
 for ( var i = 0; i < item.length; i++ )
   {
     var anitem = item[i];
     if (anitem.style.display != "inline") {
       anitem.style.display = "inline";
     } else {      
       anitem.style.display = "none";
     }
   }
 }
 </script>

<a href="javascript:unhide('hidden');">Show</a>
"""
def generate_doc_for_object(obj, previous = "", atitle=""):
    the_class = obj.IsA()
    list_of_everything = dir(obj)
    data_list = [(member, the_class.GetDataMember(member)) for member 
                  in list_of_everything if the_class.GetDataMember(member)]
    output = the_class.GetName()
    if len(atitle): output += """ (<font color="gray">%s</font>)""" % atitle
    print """<tr><th colspan="4" align="left">  %s</th></tr>""" % (output) 
    get_members = [(getattr(obj, aname)(), aname.replace('New','') +"(#)", aname.replace('New', 'Num')+"s()") for aname in list_of_everything
                  if re.match("GetNew.*", aname)]
    to_be_created = []
    for mem, data_mem in data_list:
        # clean up title
        if re.match("EXO.*", data_mem.GetTypeName()):
            to_be_created.append((getattr(ROOT, data_mem.GetTypeName()), mem))
            continue
        title = data_mem.GetTitle()
        title = re.sub('\s{3,}', ' ', title)
        temp = title.split(':')
        old_value = ' '
        new_value = temp[0]
        if len(temp) > 1:
            old_value = temp[0]
            new_value = temp[1]
        print """<tr><td><font color="gray">%s</font>%s  </td><td>%s </td><td> %s </td><td> %s</td></tr>""" % \
          (previous, mem, data_mem.GetTypeName(), old_value, ' ' + new_value.lstrip())

    for amem,mem in to_be_created: generate_doc_for_object(amem(), previous + mem + ".")
    for amem,mem,title_add in get_members: generate_doc_for_object(amem, previous + mem + "->", previous + title_add)

if __name__ == '__main__':

    ROOT.gSystem.Load("libEXOUtilities")
    ed = ROOT.EXOEventData()
    print """
<html>
<body>
<table border="1" cellpadding="5" cellpadding="0">
<caption>EXOEventData description, auto-generated on (UTC) %s</caption> 
<tr><th>Name</th><th>Type</th><th>Old Name</th><th>Description</th></tr>
    """ % (str(datetime.datetime.utcnow()))
    generate_doc_for_object(ed)
    generate_doc_for_object(ed.GetWaveformData(), "GetWaveformData()->")
    print """
</table>
</body>
</html>
    """
