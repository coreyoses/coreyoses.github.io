#!/usr/bin/env python

standard_label_prefix="coses:art"
VIEWS={}
MODE_HTML=1
VIEWS[MODE_HTML]="html"
MODE_LATEX=2
VIEWS[MODE_LATEX]="latex"

VIEWS_INVERTED={ v:k for k,v in VIEWS.items() }

ORDINALS={}
ORDINALS[1]="Primary"
ORDINALS[2]="Secondary"
ORDINALS[3]="Tertiary"
ORDINALS[4]="Quaternary"
ORDINALS[5]="Quinary"
ORDINALS[6]="Senary"
ORDINALS[7]="Septenary"
ORDINALS[8]="Octonary"
ORDINALS[9]="Nonary"
ORDINALS[10]="Denary"
ORDINALS[11]="11-nary"
ORDINALS[12]="Duodenary"

order_count_sections=0

SECTIONS_ORDERED=[]
SECTION_PERSONAL_INFO=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_OBJECTIVE=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_EDUCATION=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_RESEARCH=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_TEACHING=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_WORK_SKILLS=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_ACTIVITIES=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_PRESS=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_AWARDS=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1
SECTION_PUBLICATIONS=order_count_sections; SECTIONS_ORDERED.append(order_count_sections); order_count_sections+=1

SECTION_HEADERS={}
SECTION_HEADERS[SECTION_PERSONAL_INFO]="Personal Information"
SECTION_HEADERS[SECTION_OBJECTIVE]="Objective"
SECTION_HEADERS[SECTION_EDUCATION]="Education"
SECTION_HEADERS[SECTION_RESEARCH]="Research"
SECTION_HEADERS[SECTION_TEACHING]="Teaching Experience"
SECTION_HEADERS[SECTION_PRESS]="Press and News Releases"
SECTION_HEADERS[SECTION_WORK_SKILLS]="Work Experience and Skills"
SECTION_HEADERS[SECTION_ACTIVITIES]="Activities and Outreach"
SECTION_HEADERS[SECTION_PUBLICATIONS]="Publications"
SECTION_HEADERS[SECTION_AWARDS]="Honors and Awards"
   
