#!/usr/bin/env python

import os
import errno
import subprocess
import json
import sys

from definitions import *

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def issue_command(command):
    p=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return p.communicate()

#http://stackoverflow.com/questions/14902299/json-loads-allows-duplicate-keys-in-a-dictionary-overwriting-the-first-value
def dict_raise_on_duplicates(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    for k, v in ordered_pairs:
        if k in d:
           raise ValueError("Duplicate key: %r" % (k,))
        else:
           d[k] = v
    return d

def uniqueEndingJoin(_list,delim1,delim2):
    if len(_list)==1:
        return _list[0]
    else:
        return delim2.join([delim1.join(_list[:-1]),_list[-1]])

def generateError(_message):
    message="".join(["ERROR - ",_message])
    sys.exit(message)

def getViewSpecificNode(node,_view):
    if isinstance(node, dict):
        try:
            view=VIEWS[_view]
        except:
            generateError("View not found: "+str(_view))
        try:
            return node[view]
        except:
            generateError("Node does not contain desired view ("+str(_view)+"): "+str(node))
    else:
        return node

def getPresentationItems(node,view):
    def getPresentationItem(title,view,organization,show_date,date):
        if title:
            output_string=", ".join([getViewSpecificNode(title,view),getViewSpecificNode(organization,view)])
        else:
            output_string=" ".join(["Presented at",getViewSpecificNode(organization,view)])
        if show_date:
            if view==MODE_LATEX:
                output_string=" --- ".join([output_string,getViewSpecificNode(date,view)])
        return output_string+"."

    #precedence:  results, title, "Presentated at"
    try:
        results=[ r for r in node["results"] if r ]
    except:
        generateError("Presentation node does not contain ''results'': "+str(node))
    try:
        title=node["title"]
    except:
        generateError("Presentation node does not contain ''title'': "+str(node))
    try:
        organization=node["organization"]
    except:
        generateError("Presentation node does not contain ''organization'': "+str(node))
    try:
        show_date=node["show_date"]
    except:
        generateError("Presentation node does not contain ''show_date'': "+str(node))
    try:
        date=node["date"]
    except:
        generateError("Presentation node does not contain ''date'': "+str(node))
    output=[]
    if results:
        for r in results:
            output.append(getPresentationItem(r,view,organization,show_date,date))
    else:
        output.append(getPresentationItem(title,view,organization,show_date,date))

    return output

class Data_Obj:
    """
    """
    def __init__(self,File_Path=""):
        self.file_path=""
        self.data={}

        self.file_path=File_Path
        Data_Obj.__grabData(self)

    def __grabData(self):
        try:
            with open(self.file_path) as fin:
                self.data=json.load(fin,object_pairs_hook=dict_raise_on_duplicates)
        except:
            generateError("Unable to open "+str(self.file_path))

    def getNodeData(self,mapList,View=None):
        if isinstance(mapList,list):
            try:
                node=reduce(lambda d, k: d[k], mapList, self.data)
            except:
                generateError("MapList ("+str(mapList)+") failed in node: "+str(self.file_path))
        else:
            try:
                node=self.data[mapList]
            except:
                generateError("Key ("+str(mapList)+") failed in node: "+str(self.file_path))
        view=View
        if view:
            node=getViewSpecificNode(node,view)
        return node

    def writeData(self,Destination=""):
        destination=Destination
        if not destination:
            destination=self.file_path
        try:
            with open(destination,"w") as fout:
                json.dump(self.data,fout,sort_keys=True,indent=4,separators=(',', ': '))
        except:
            generateError("Unable to write to "+str(destination))

def getCountFromLabel(label,prefix=journal_label_prefix):
    try:
        return int(label.replace(prefix,""))
    except:
        generateError("Unknown label style, cannot extract count from "+str(label))

def getFormattedPublication(abbrev_journal,volume,number,pages,year,view,pub_status="published"):
    if not (pub_status=="published" or pub_status=="press"):
        generateError("Unknown publication status: "+pub_status)
    if not abbrev_journal:
        generateError("No journal provided.")
    if pub_status=="published":
        if not volume:
            generateError("No volume provided.")
        #number not necessary
        if not pages:
            generateError("No pages provided.")
    if not year:
        generateError("No year provided.")
    if view==MODE_LATEX:
        outstring=abbrev_journal+" "
        if pub_status=="published":
            outstring+="\\textbf{"+volume+"}"
            if number:
                outstring+="("+number+")"
            outstring+=", "+pages+" "
        else:
            outstring+="\\textbf{in press} "
        outstring+="("+str(year)+")"
        return outstring

def joinLists(_list,d_list):
    out_list=[]
    for i,l in enumerate(_list):
        out_list.append(l)
        if i<(len(_list)-1):
            out_list+=d_list
    return out_list
