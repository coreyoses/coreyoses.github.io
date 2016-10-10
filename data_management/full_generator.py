#!/usr/bin/env python

import json
import sys

standard_label_prefix="coses:art"
_VIEWS_={}
_HTML_=1
_VIEWS_[_HTML_]="html"
_LATEX_=2
_VIEWS_[_LATEX_]="latex"

_VIEWS_INVERTED_={ v:k for k,v in _VIEWS_.items() }

_ORDINALS_={}
_ORDINALS_[1]="Primary"
_ORDINALS_[2]="Secondary"
_ORDINALS_[3]="Tertiary"
_ORDINALS_[4]="Quaternary"
_ORDINALS_[5]="Quinary"
_ORDINALS_[6]="Senary"
_ORDINALS_[7]="Septenary"
_ORDINALS_[8]="Octonary"
_ORDINALS_[9]="Nonary"
_ORDINALS_[10]="Denary"
_ORDINALS_[11]="11-nary"
_ORDINALS_[12]="Duodenary"

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
            view=_VIEWS_[_view]
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
            if view==_LATEX_:
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

class data_file:
    """
    """
    def __init__(self,File_Path=""):
        self.file_path=""
        self.data={}

        self.file_path=File_Path
        data_file.__grabData(self)

    def __grabData(self):
        try:
            with open(self.file_path) as fin:
                self.data=json.load(fin)
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

def getCountFromLabel(label,prefix=standard_label_prefix):
    try:
        return int(label.replace(prefix,""))
    except:
        generateError("Unknown label style, cannot extract count from "+str(label))

def getDuplicates(some_list):
    seen=set()
    duplicates=[]

    for key in some_list:
        if key in seen:
            duplicates.append(key)
        seen.add(key)

    return duplicates

def getCountSkipped(some_count_list):
    minimum=min(some_count_list)
    maximum=max(some_count_list)
    missing=[]

    for i in range(minimum,maximum):
        if i not in some_count_list:
            missing.append(i)

    return missing

def loadAndValidatePublications():
    ############################################################################################################
    def validateLabels(pub_data):
        publications=pub_data["publications"]
        #check that there are no duplicates in labels
        duplicates=getDuplicates(publications.data.keys())
        if duplicates:
            generateError("Duplicate publication labels: "+",".join(map(str,duplicates)))
        #check that full range exists in counts
        counts=[ getCountFromLabel(label) for label in publications.data.keys() ]
        missing=getCountSkipped(counts)
        if missing:
            generateError("Publication label count range not complete, missing: "+",".join(map(str,missing)))
        return True
    ############################################################################################################
    def validateAuthors(pub_data):
        publications=pub_data["publications"]
        author_list=pub_data["authors"].data.keys()
        institution_list=pub_data["institutions"].data.keys()
        for pub in publications.data.keys():
            authors_mapList=[pub,"authors"]
            #check that there are no duplicates in authors
            publications_authors=publications.getNodeData(authors_mapList).keys()
            duplicates=getDuplicates(publications_authors)
            if duplicates:
                generateError("Duplicate authors in "+str(pub)+": "+",".join(map(str,duplicates)))
            #validate authors and institutions
            orders=[]
            for author in publications_authors:
                if author not in author_list:
                    generateError("Author in "+str(pub)+" not found in author list: "+str(author))
                author_specific_mapList=authors_mapList+[author]
                publications_institutions=publications.getNodeData(author_specific_mapList+["institution"])
                for institution in publications_institutions:
                    if institution not in institution_list:
                        generateError("Institution of author "+str(author)+" in "+str(pub)+" not found in institution list: "+str(institution))
                orders.append(publications.getNodeData(author_specific_mapList+["order"]))
            #validate orders (duplicates and range)
            duplicates=getDuplicates(orders)
            if duplicates:
                generateError("Duplicate orders in "+str(pub)+": "+",".join(map(str,duplicates)))
            missing=getCountSkipped(orders)
            if missing:
                generateError("Order count range in "+str(pub)+" not complete, missing: "+",".join(map(str,missing)))
        return True
    ############################################################################################################
    def validateJournals(pub_data):
        publications=pub_data["publications"]
        journal_list=pub_data["journals"].data.keys()
        for pub in publications.data.keys():
            #check that journal is found
            journal_mapList=[pub,"journal"]
            journal=publications.getNodeData(journal_mapList)
            #journal can be empty
            if journal and journal not in journal_list:
                generateError("Journal in "+str(pub)+" not found in journal list: "+str(journal))
        return True
    ############################################################################################################
    def fullValidator(pub_data):
        print "Validating publication labels"
        validateLabels(pub_data)
        print "Validating publication authors"
        validateAuthors(pub_data)
        print "Validating publication journals"
        validateJournals(pub_data)

        print "Publications are all validated!"
        return True
    ############################################################################################################

    publications=data_file(File_Path="data/publications.json")
    journals=data_file(File_Path="data/journals.json")
    authors=data_file(File_Path="data/people.json")
    institutions=data_file(File_Path="data/institutions.json")

    pub_data={}
    pub_data["publications"]=publications
    pub_data["journals"]=journals
    pub_data["authors"]=authors
    pub_data["institutions"]=institutions
    
    fullValidator(pub_data)

    return pub_data


if __name__ == "__main__":
    
    pub_data=loadAndValidatePublications()
    #print publications.data
    #publications.writeData(Destination="here")
