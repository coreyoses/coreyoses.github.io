#!/usr/bin/env python

from basic_functions import *

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

    publications=data_file(File_Path="../data/publications.json")
    journals=data_file(File_Path="../data/journals.json")
    authors=data_file(File_Path="../data/people.json")
    institutions=data_file(File_Path="../data/institutions.json")

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
