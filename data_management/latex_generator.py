#!/usr/bin/env python

#flows from definitions, basic_functions, settings, data_structures
import sys
sys.path.insert(0,"functions")
from data_structures import *

_DOT_DELIMITER_="\\ \\ $\\cdotp$\\ \\ "
_DEFAULT_INDENTATION_="2.5cm"
_DOI_PREFIX_="http://dx.doi.org/"
#HIGHLIGHT_COLOR="NavyBlue"

def keepStringTogether(in_string):
    return "".join(["\\mbox{",in_string,"}"])

def getLatexHyperlink(link,display=""):
    if not display:
        display=link
    return "\\href{"+link+"}{"+display+"}"

def getPhoneNumber(numbers):
    #should have 4 parts
    return " ".join(["+"+str(numbers[0]),"("+str(numbers[1])+")",str(numbers[2]),str(numbers[3])])

def createBullets(_list):
    output=[]
    output.append("\\begin{itemize}[leftmargin=*]")
    for l in _list:
        output.append(" ".join(["\\item",l]))
    output.append("\\end{itemize}")
    return " ".join(output)

def fixStringLatex(string):
    letters=list(string)
    max_count=len(letters)
    output=[]

    problem_characters=["&","%","$","#","_","{","}","~","^"]
    solution_character="\\"
    
    for i,l in enumerate(letters):
        for p in problem_characters:
            if l==p:
                #determine if fix is already there
                if i and letters[i]==solution_character:
                    break
                output.append(solution_character)
        if l=="~" or l=="^":
            output.append("{}")
        #only okay if it serves as an escape
        if l==solution_character:
            if not (i<(max_count-1) and letters[i+1] in problem_characters):
                generateError("Issue fixing string for latex: "+string)
        output.append(l)
    return "".join(output)

def getResumeContent():
    
    def getHeader():
        header=[]
        header.append("\\documentclass[11pt]{article}")
        header.append("")
        header.append("%http://www.tug.org/mactex/fonts/LaTeX_Preamble-Font_Choices.html")
        header.append("% Euler for math | Palatino for rm | Helvetica for ss | Courier for tt")
        header.append("\\renewcommand{\\rmdefault}{ppl} % rm")
        header.append("\\linespread{1.05}        % Palatino needs more leading")
        header.append("\\usepackage[scaled]{helvet} % ss")
        header.append("\\usepackage{courier} % tt")
        header.append("\\usepackage{euler} % math")
        header.append("\\usepackage{soul}")
        header.append("%\\usepackage{eulervm} % a better implementation of the euler package (not in gwTeX)")
        header.append("\\normalfont")
        header.append("\\usepackage[T1]{fontenc}")
        header.append("")
        header.append("\\usepackage[top=0.5in,left=0.5in,right=0.5in,bottom=1in]{geometry}")
        header.append("\\usepackage[dvipsnames]{xcolor}")
        header.append("\\usepackage{array}")
        header.append("\\usepackage{hyperref}")
        header.append("\\usepackage{enumitem}")
        header.append("\\hypersetup{colorlinks,breaklinks,urlcolor=Maroon,linkcolor=Maroon}")
        header.append("\\hyphenpenalty=10000    %avoid hyphenation")
        return header

    def getSectionHeader(header,indent=_DEFAULT_INDENTATION_,color="black",large=False):
        output=[]
        output.append("\\hspace{")
        output.append(indent)
        output.append("}\\textcolor{")
        output.append(color)
        output.append("}{")
        if large:
            output.append("\\LARGE")
        output.append("\\textsc{\\so{")
        output.append(header)
        output.append("}}}")
        return "".join(output)

    def getYearHeader(year,indent=_DEFAULT_INDENTATION_):
        output=[]
        output.append("\\hspace{")
        output.append(indent)
        output.append("}")
        output.append("{\\Large")
        output.append(str(year))
        output.append("}")
        return "".join(output)

    def getEntry(margin="",date="",title="",description="",large_title=False):
        output=[]
        output.append("\\begin{center}")
        output.append("\\begin{tabular}{>{\\centering\\arraybackslash}m{0.75in}m{0.25in}c}")
        if margin:
            output.append("".join(["\\raggedleft{\\textit{\\small{",margin,"}}}"]))
        output.append(" & & ")
        output.append("\\begin{tabular}{@{}p{0.85in}p{0.05in}p{4.1in}@{}}")
        if large_title:
            output.append("".join(["\\multicolumn{3}{@{}p{5.3in}@{}}{",title,"} \\\\"]))
        else:
            if date:
                output.append("".join(["\\textit{\\small{",date,"}}"]))
            output.append(" & &")
            output.append(" ".join([title,"\\\\"]))
        if description:
            #output.append("".join(["\\multicolumn{3}{@{}p{5.1in}@{}}{\\vspace{-0.1in}\\footnotesize{",description,"}}"]))
            output.append("".join(["\\multicolumn{3}{@{}p{5.3in}@{}}{\\vspace{-0.1in}\\footnotesize{",description,"}}"]))
        output.append("\\end{tabular} \\\\")
        output.append("\\end{tabular}")
        output.append("\\end{center}")
        
        return "\n".join(output)

    def getPersonalInfo():
        content=[]
        content.append(getSectionHeader(" ".join([ data_obj["personal_info"].getNodeData(name,MODE_LATEX).upper() for name in ["first_name","last_name"] if data_obj["personal_info"].getNodeData(name,MODE_LATEX) ]),color="Maroon",large=True))
        content.append("")
        content.append("\\vspace{0.15cm}")
        content.append("")
        titles=data_obj["personal_info"].getNodeData("titles")
        for title in titles:
            content.append("\\hspace{2.5cm}\\textit{"+getViewSpecificNode(title["title"],MODE_LATEX)+\
                           ",} "+getViewSpecificNode(title["location"],MODE_LATEX))
        content.append("")
        content.append("\\vspace{0.5cm}")
        content.append("")
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_PERSONAL_INFO]))
        content.append("")
        content.append("\\vspace{-0.2cm}")
        content.append("")
        entry_date="email"
        entry_title=getLatexHyperlink("mailto:"+data_obj["personal_info"].getNodeData("email",MODE_LATEX),data_obj["personal_info"].getNodeData("email",MODE_LATEX))
        content.append(getEntry(date=entry_date,title=entry_title))
        content.append("")
        content.append("\\vspace{-0.75cm}")
        content.append("")
        entry_date="website"
        entry_title=getLatexHyperlink(data_obj["personal_info"].getNodeData("homepage",MODE_LATEX))
        content.append(getEntry(date=entry_date,title=entry_title))
        content.append("")
        content.append("\\vspace{-0.75cm}")
        content.append("")
        entry_date="phone"
        entry_title=""
        #add flag for mobile
        if True:
            entry_title+="(M) "
            mobile_phone=data_obj["personal_info"].getNodeData("mobile_phone")
            entry_title+=getPhoneNumber(mobile_phone)
            entry_title+=_DOT_DELIMITER_
        entry_title+="(W) "
        work_phone=data_obj["personal_info"].getNodeData("work_phone")
        entry_title+=getPhoneNumber(work_phone)
        content.append(getEntry(date=entry_date,title=entry_title))
        
        return content

    def getObjective():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_OBJECTIVE]))
        content.append("")
        content.append("\\vspace{-0.75cm}")
        content.append("")
        
        #make flag for type of resume
        if True:
            variant="educational"
        objective=data_obj["objective"].getNodeData(variant)
        content.append(getEntry(description=objective))

        return content
    
    def getAdvisors(advisors,title="Advisor",show_title=True):
        outstring=""
        if show_title:
            if len(advisors)==1:
                outstring+="\\textbf{"+title+"}: "#+uniqueEndingJoin(advisors,", "," \\& ")
            else:
                outstring+="\\textbf{"+title+"s}: "#+uniqueEndingJoin(advisors,", "," \\& ")
        outstring+=uniqueEndingJoin(advisors,", "," \\& ")
        return outstring

    def getEducation():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_EDUCATION]))
        content.append("")
        
        schools=sorted(data_obj["education"].data.keys(),key=lambda school: data_obj["education"].getNodeData([school,'order']),reverse=True)
        for school in schools:
            entry_margin=data_obj["education"].getNodeData([school,"degree"],MODE_LATEX)
            entry_date=data_obj["education"].getNodeData([school,"duration"],MODE_LATEX)
            entry_title=data_obj["education"].getNodeData([school,"name"],MODE_LATEX)
            entry_description=""
            join_w_dots=[]
            gpa=data_obj["education"].getNodeData([school,"gpa"],MODE_LATEX)
            if gpa:
                join_w_dots.append(keepStringTogether("GPA: "+gpa))
            honors=[ getViewSpecificNode(honor,MODE_LATEX) for honor in data_obj["education"].getNodeData([school,"honors"]) if honor ]
            if honors:
                for honor in honors:
                    join_w_dots.append(keepStringTogether("\\textit{"+honor+"}"))
            college=data_obj["education"].getNodeData([school,"school"],MODE_LATEX)
            #add flag
            if False and college:
                join_w_dots.append(keepStringTogether("School: "+college))
            department=data_obj["education"].getNodeData([school,"department"],MODE_LATEX)
            if department:
                join_w_dots.append(keepStringTogether("Department: "+department))
            entry_description+=_DOT_DELIMITER_.join(join_w_dots)
            entry_description+="\\newline "
            theses=[ data_obj["projects"].getNodeData([thesis,"title"],MODE_LATEX) for thesis in data_obj["education"].getNodeData([school,"theses"]) if thesis ]
            if theses:
                if len(theses)>1:
                    for i,thesis in enumerate(theses):
                        entry_description+=ORDINALS[i]+" Thesis: \\textit{"+thesis+"}"
                        entry_description+="\\newline "
                else:
                    entry_description+="Thesis: \\textit{"+theses[0]+"}"
                    entry_description+="\\newline "
            #no description, do in research section
            advisors=[ " ".join( [ data_obj["people"].getNodeData([advisor,name],MODE_LATEX) for name in ["first_name","middle_name","last_name"] if data_obj["people"].getNodeData([advisor,name],MODE_LATEX) ] ) for advisor in data_obj["education"].getNodeData([school,"advisors"]) if advisor ]
            if advisors:
                entry_description+=getAdvisors(advisors)
            #content.append(getDescription(data_obj["education"].getNodeData([school,"degree"],MODE_LATEX),misc))
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getResearchExperience():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_RESEARCH]))
        content.append("")
        
        experiences=sorted(data_obj["projects"].data.keys(),key=lambda experience: data_obj["projects"].getNodeData([experience,'order']),reverse=True)
        for experience in experiences:
            entry_margin=data_obj["institutions"].getNodeData([data_obj["projects"].getNodeData([experience,"institution"]),"name"],MODE_LATEX)
            entry_date=data_obj["projects"].getNodeData([experience,"duration"],MODE_LATEX)
            entry_title=data_obj["projects"].getNodeData([experience,"title"],MODE_LATEX)
            entry_description=""
            descriptions=[ getViewSpecificNode(description,MODE_LATEX) for description in data_obj["projects"].getNodeData([experience,"description"],MODE_LATEX) if description ]
            presentation_nodes=[ data_obj["presentations"].data[presentation] for presentation in data_obj["projects"].getNodeData([experience,"presentations"],MODE_LATEX) if presentation ]
            presentations=[]
            for node in presentation_nodes:
                presentations+=getPresentationItems(node,MODE_LATEX)
            highlights=[ getViewSpecificNode(highlight,MODE_LATEX) for highlight in data_obj["projects"].getNodeData([experience,"highlights"],MODE_LATEX) if highlight ]
            advisors=[ " ".join( [ data_obj["people"].getNodeData([advisor,name],MODE_LATEX) for name in ["first_name","middle_name","last_name"] if data_obj["people"].getNodeData([advisor,name],MODE_LATEX) ] ) for advisor in data_obj["projects"].getNodeData([experience,"advisors"]) if advisor ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
            if presentations:
                entry_description+=createBullets(presentations)+" "
            if highlights:
                entry_description+=createBullets(highlights)+" "
            if advisors:
                if description and not (presentations or highlights):
                    entry_description+="\\newline "
                entry_description+=getAdvisors(advisors)
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")
        
        return content

    def getTeachingExperience():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_TEACHING]))
        content.append("")

        experiences=sorted(data_obj["teaching"].data.keys(),key=lambda experience: data_obj["teaching"].getNodeData([experience,'order']),reverse=True)
        for experience in experiences:
            entry_margin=data_obj["teaching"].getNodeData([experience,"title"],MODE_LATEX)#
            entry_date=data_obj["teaching"].getNodeData([experience,"duration"],MODE_LATEX)
            entry_title=", ".join([data_obj["teaching"].getNodeData([experience,"course"],MODE_LATEX),data_obj["institutions"].getNodeData([data_obj["teaching"].getNodeData([experience,"institution"]),"name"],MODE_LATEX)])
            entry_description=""
            descriptions=[ getViewSpecificNode(description,MODE_LATEX) for description in data_obj["teaching"].getNodeData([experience,"description"],MODE_LATEX) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
            highlights=[ getViewSpecificNode(highlight,MODE_LATEX) for highlight in data_obj["teaching"].getNodeData([experience,"highlights"],MODE_LATEX) if highlight ]
            if highlights:
                entry_description+=createBullets(highlights)+" "
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")
        
        #need to add -vspace
        #content.append()

        return content

    def getPress():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_PRESS]))
        content.append("")

        releases=sorted(data_obj["press"].data.keys(),key=lambda release: data_obj["press"].getNodeData([release,'order']),reverse=True)
        for release in releases:
            entry_margin=data_obj["press"].getNodeData([release,"organization"],MODE_LATEX)
            entry_date=data_obj["press"].getNodeData([release,"date"],MODE_LATEX)
            entry_title="\\textit{``"+data_obj["press"].getNodeData([release,"title"],MODE_LATEX)+"''}"
            entry_description=""
            descriptions=[ getViewSpecificNode(description,MODE_LATEX) for description in data_obj["press"].getNodeData([release,"description"],MODE_LATEX) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
                entry_description+="\\newline "
            url=data_obj["press"].getNodeData([release,"url"],MODE_LATEX)
            if url:
                entry_description+=getLatexHyperlink(fixStringLatex(url))
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getWorkExperienceAndSkills():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_WORK_SKILLS]))
        content.append("")

        experiences=sorted(data_obj["work_skills"].data.keys(),key=lambda experience: data_obj["work_skills"].getNodeData([experience,'order']),reverse=True)
        for experience in experiences:
            entry_margin=data_obj["work_skills"].getNodeData([experience,"title"],MODE_LATEX)
            entry_date=data_obj["work_skills"].getNodeData([experience,"duration"],MODE_LATEX)
            entry_title=data_obj["work_skills"].getNodeData([experience,"organization"],MODE_LATEX)
            #if not entry_title:
            #    entry_title=entry_margin
            #    entry_margin=""
            entry_description=""
            descriptions=[ getViewSpecificNode(description,MODE_LATEX) for description in data_obj["work_skills"].getNodeData([experience,"description"],MODE_LATEX) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
            highlights=[ getViewSpecificNode(highlight,MODE_LATEX) for highlight in data_obj["work_skills"].getNodeData([experience,"highlights"],MODE_LATEX) if highlight ]
            if highlights:
                entry_description+=createBullets(highlights)+" "
            supervisors=[ " ".join( [ data_obj["people"].getNodeData([supervisor,name],MODE_LATEX) for name in ["first_name","middle_name","last_name"] if data_obj["people"].getNodeData([supervisor,name],MODE_LATEX) ] ) for supervisor in data_obj["work_skills"].getNodeData([experience,"supervisors"]) if supervisor ]
            if supervisors:
                if description and not highlights:
                    entry_description+="\\newline "
                entry_description+=getAdvisors(supervisors,title="Supervisor")
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content
    
    #COME BACK AND FILL IN CONFERENCES FROM PAST, LIKE KC, MUN, FBLA, ETC.
    def getActivities():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_ACTIVITIES]))
        content.append("")

        activities=sorted(data_obj["activities"].data.keys(),key=lambda activity: data_obj["activities"].getNodeData([activity,'order']),reverse=True)
        for activity in activities:
            entry_margin=""
            positions=[ getViewSpecificNode(position,MODE_LATEX) for position in data_obj["activities"].getNodeData([activity,"positions"],MODE_LATEX) if position ]
            if positions:
                entry_margin=positions[0]
                #too long, just fix here 
                if "New York District" in entry_margin and "Distinguished Past Governor" in entry_margin:
                    entry_margin="\\textcolor{NavyBlue}{Distinguished Past Governor}"
            entry_date=data_obj["activities"].getNodeData([activity,"duration"],MODE_LATEX)
            entry_title=data_obj["activities"].getNodeData([activity,"title"],MODE_LATEX)
            entry_description=""
            descriptions=[ getViewSpecificNode(description,MODE_LATEX) for description in data_obj["activities"].getNodeData([activity,"description"],MODE_LATEX) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
                #entry_description+="\\newline "
            highlights=[ getViewSpecificNode(highlight,MODE_LATEX) for highlight in data_obj["activities"].getNodeData([activity,"highlights"],MODE_LATEX) if highlight ]
            if highlights:
                entry_description+=createBullets(highlights)+" "
            if len(positions)>1:
                if description and not highlights:
                    entry_description+="\\newline "
                entry_description+=getAdvisors(positions,title="Position")
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getAwards():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_AWARDS]))
        content.append("")

        honors=sorted(data_obj["honors"].data.keys(),key=lambda honor: data_obj["honors"].getNodeData([honor,'order']),reverse=True)
        for honor in honors:
            entry_margin=data_obj["honors"].getNodeData([honor,"type"],MODE_LATEX)
            entry_date=data_obj["honors"].getNodeData([honor,"date"],MODE_LATEX)
            entry_title=data_obj["honors"].getNodeData([honor,"title"],MODE_LATEX)
            organization=data_obj["honors"].getNodeData([honor,"organization"],MODE_LATEX)
            if organization:
                entry_title=", ".join([entry_title,organization])
            entry_description=""
            descriptions=[ getViewSpecificNode(description,MODE_LATEX) for description in data_obj["honors"].getNodeData([honor,"description"],MODE_LATEX) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
                #entry_description+="\\newline "
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getPublications():
        content=[]
        content.append(getSectionHeader(SECTION_HEADERS[SECTION_PUBLICATIONS]))
        content.append("")

        current_year=0

        pubs=sorted(data_obj["publications"].data.keys(),key=lambda pub: getCountFromLabel(pub),reverse=True)
        for pub in pubs:
            #figure out date stuff first
            date=data_obj["publications"].getNodeData([pub,"year"],MODE_LATEX)
            if date!=current_year:
                content.append("")
                if not current_year:
                    content.append("\\vspace{0.5cm}")
                content.append(getYearHeader(date))
                content.append("")
                current_year=date
            status=data_obj["publications"].getNodeData([pub,"status"],MODE_LATEX)
            entry_title="\\textit{"+data_obj["publications"].getNodeData([pub,"title"],MODE_LATEX)+"}"
            entry_description=""
            _authors=[ " ".join( [ data_obj["people"].getNodeData([author,name],MODE_LATEX) for name in ["first_name","middle_name","last_name"] if data_obj["people"].getNodeData([author,name],MODE_LATEX) ] ) for author in sorted(data_obj["publications"].getNodeData([pub,"authors"]).keys(),key=lambda a: data_obj["publications"].getNodeData([pub,"authors",a,"order"])) if author ]
            authors=[]
            for a in _authors:
                if a=="Corey Oses":
                    a="\\textcolor{NavyBlue}{Corey Oses}"
                authors.append(a)
            if status=="published" or status=="press":
                entry_margin=data_obj["journals"].getNodeData([data_obj["publications"].getNodeData([pub,"journal"]),"name"],MODE_LATEX)
                entry_title+=" \\newline "
                #entry_title+="\\small{"+getAdvisors(authors,title="Author",show_title=False)+"} \\newline "
                entry_title+=getFormattedPublication(\
                        data_obj["journals"].getNodeData([data_obj["publications"].getNodeData([pub,"journal"]),"abbreviation"],MODE_LATEX),\
                        data_obj["publications"].getNodeData([pub,"volume"],MODE_LATEX),\
                        data_obj["publications"].getNodeData([pub,"number"],MODE_LATEX),\
                        data_obj["publications"].getNodeData([pub,"pages"],MODE_LATEX),\
                        data_obj["publications"].getNodeData([pub,"year"],MODE_LATEX),\
                        MODE_LATEX,\
                        pub_status=status)+" "#+" \\newline "+\
            elif status=="submitted":
                entry_margin="Submitted"
            else:
                entry_margin="In Preparation"
            entry_date=""#str(data_obj["publications"].getNodeData([pub,"year"],MODE_LATEX))
            if authors:
                entry_description+=getAdvisors(authors,title="Author")+" \\newline "
            show_abstract=data_obj["publications"].getNodeData([pub,"show_abstract"],MODE_LATEX)
            abstract=data_obj["publications"].getNodeData([pub,"abstract"],MODE_LATEX)
            if True or show_abstract:
                entry_description+="\\textbf{Abstract}: "+abstract+" \\newline "
            #highlights=[ getViewSpecificNode(highlight,MODE_LATEX) for highlight in data_obj["publications"].getNodeData([experience,"highlights"],MODE_LATEX) if highlight ]
            #if highlights:
            #    entry_description+=createBullets(highlights)+" "
            if status=="published":
                doi=data_obj["publications"].getNodeData([pub,"doi"],MODE_LATEX)
                if not doi:
                    generateError("No doi found for "+data_obj["publications"].getNodeData([pub,"title"],MODE_LATEX))
                entry_description+="\\textbf{DOI}: "+getLatexHyperlink(_DOI_PREFIX_+doi,display=fixStringLatex(doi))
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description,large_title=True))
            content.append("")

        return content

    spacing=0

    section_generator={}
    section_generator[SECTION_PERSONAL_INFO]=getPersonalInfo
    section_generator[SECTION_OBJECTIVE]=getObjective
    section_generator[SECTION_EDUCATION]=getEducation
    section_generator[SECTION_RESEARCH]=getResearchExperience
    section_generator[SECTION_TEACHING]=getTeachingExperience
    section_generator[SECTION_PRESS]=getPress
    section_generator[SECTION_WORK_SKILLS]=getWorkExperienceAndSkills
    section_generator[SECTION_ACTIVITIES]=getActivities
    section_generator[SECTION_PUBLICATIONS]=getPublications
    section_generator[SECTION_AWARDS]=getAwards
    

    content=[]
    content+=getHeader()
    content.append("")
    content.append("\\begin{document}")
    for i,section in enumerate(SECTIONS_ORDERED):
        if not SECTION_SHOW[section]:
            continue
        content+=section_generator[section]()
        if section==SECTION_OBJECTIVE:
            content.append("")
            content.append("\\vspace{"+str(spacing)+"em}")
        if i<(len(SECTIONS_ORDERED)-1):
            content.append("")

    content.append("\\end{document}")
    return content


if __name__ == "__main__":
    content=getResumeContent()
    destination="resume/full"
    mkdir_p(destination)
    destination+="/resume.tex"
    with open(destination,"w") as fout:
        fout.write("\n".join(content))

    """
    #content.append("\\thispagestyle{empty}")
    #begin{cv} in personalInfo, must be attached to name
    content+=getPersonalInfo()
    content.append("")
    #content.append("\\vspace{"+str(spacing+0.5)+"em}")
    if True:
        content.append("")
        content+=getObjective()
        content.append("")
        content.append("\\vspace{"+str(spacing)+"em}")
    content.append("")
    content+=getEducation()
    content.append("")
    #content.append("\\vspace{"+str(spacing)+"em}")
    content+=getResearchExperience()
    content.append("")
    content+=getTeachingExperience()
    content.append("")
    content+=getPress()
    content.append("")
    content+=getWorkExperienceAndSkills()
    content.append("")
    content+=getActivities()
    content.append("")
    content+=getAwards()
    content.append("")
    content+=getPublications()
    #content.append("\\vspace{"+str(spacing)+"em}")
    content+=getPublications()
    content.append("\\vspace{"+str(spacing)+"em}")

    content.append("")

    content.append("")
    #content.append("\\end{cv}")
    """


    """
    def getHeader():
        header=[]
        header.append("\\documentclass{scrartcl}")
        header.append("\\reversemarginpar")
        header.append("\\newcommand{\\MarginText}[1]{\\marginpar{\\raggedleft\\itshape\\small#1}}")
        header.append("\\usepackage[nochapters]{classicthesis}")
        header.append("\\usepackage[LabelsAligned]{currvita}")
        header.append("\\renewcommand{\\cvheadingfont}{\\LARGE\\color{Maroon}}")
        header.append("\\usepackage{hyperref}")
        header.append("\\hypersetup{colorlinks,breaklinks,urlcolor=Maroon,linkcolor=Maroon}")
        #header.append("\\newlength{\datebox}\\settowidth{\datebox}{Summer 2010--Spring 2011}")
        header.append("\\newlength{\datebox}\\settowidth{\datebox}{Spring 2011}")
        header.append("\\newcommand{\\NewEntry}[1]{\\hangindent=2em\\hangafter=0\\noindent\\raggedright{#1}\\par}")
        header.append("\\newcommand{\\Title}[3]{\\noindent\\hangindent=2em\\hangafter=0\\parbox{\\datebox}{\\small\\textit{#1}}\\hspace{1.5em} #2 #3")
        header.append("\\vspace{0.5em}}")
        header.append("\\newcommand{\\Description}[1]{\\hangindent=2em\\hangafter=0\\noindent\\raggedright\\footnotesize{#1}\\par\\normalsize\\vspace{1em}}")
        #header.append("\\newcommand{\\Description}[1]{\\hangindent=2em\\hangafter=0\\noindent\\raggedright\\footnotesize{#1}\par\\normalsize")
        return header

    def getNewEntry(entry):
        output="\\NewEntry{"
        output+=entry
        output+="}"
        return output

    #def getNewEntry(header,description,extra=""):
    def getTitle(header,description,extra=""):
        output="\\Title{"
        output+=header
        output+="}{"
        output+=description
        output+="}"
        #if extra:
        output+="{"
        output+=extra
        output+="}"
        return output

    def getDescription(header,description):
        output="\\Description{"
        if header:
            output+="\\MarginText{"+header+"}"
        output+=description+"}"
        return output

    def getSectionHeader(header,VSpacing="1em"):
        return "".join(["\\noindent\\spacedlowsmallcaps{",header,"}\\vspace{"+VSpacing+"}"])
    """
