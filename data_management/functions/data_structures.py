#!/usr/bin/env python

from settings import *

data_directory="data"
JSONS=[ json for json in os.listdir(data_directory) if ".json"==json[-5:] ]
data_obj={}
for json in JSONS:
    obj_name=json[:-5]
    obj_path=os.path.join(data_directory,json)
    data_obj[obj_name]=Data_Obj(obj_path)

"""
objective_obj=data_file("data/objective.json")
edu_obj=data_file("data/education.json")
proj_obj=data_file("data/projects.json")
presentations_obj=data_file("data/presentations.json")
people_obj=data_file("data/people.json")
inst_obj=data_file("data/institutions.json")
teach_obj=data_file("data/teaching.json")
press_obj=data_file("data/press.json")
work_obj=data_file("data/work_skills.json")
activities_obj=data_file("data/activities.json")
honors_obj=data_file("data/honors.json")
pubs_obj=data_file("data/publications.json")
journals_obj=data_file("data/journals.json")
"""
