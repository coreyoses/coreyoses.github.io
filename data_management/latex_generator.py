#!/usr/bin/env python

from basic_functions import *
from full_generator import generateError
from full_generator import getViewSpecificNode
from full_generator import data_file
from full_generator import _LATEX_
from full_generator import _ORDINALS_
from full_generator import uniqueEndingJoin
from full_generator import getPresentationItems

_DOT_DELIMITER_="\\ \\ $\\cdotp$\\ \\ "
_DEFAULT_INDENTATION_="2.5cm"
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
    obj=data_file("data/objective.json")
    edu_obj=data_file("data/education.json")
    proj_obj=data_file("data/projects.json")
    presentations_obj=data_file("data/presentations.json")
    people_obj=data_file("data/people.json")
    inst_obj=data_file("data/institutions.json")
    teach_obj=data_file("data/teaching.json")
    press_obj=data_file("data/press.json")
    work_obj=data_file("data/work_skills.json")
    
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
        header.append("\\usepackage[margin=0.5in]{geometry}")
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

    def getEntry(margin="",date="",title="",description=""):
        output=[]
        output.append("\\begin{center}")
        output.append("\\begin{tabular}{>{\\centering\\arraybackslash}m{0.75in}m{0.25in}c}")
        if margin:
            output.append("".join(["\\raggedleft{\\textit{\\small{",margin,"}}}"]))
        output.append(" & & ")
        output.append("\\begin{tabular}{@{}p{0.85in}p{0.05in}p{4.1in}@{}}")
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
        pinfo=data_file("data/personal_info.json")
        content=[]
        content.append(getSectionHeader(" ".join([ pinfo.getNodeData(name,_LATEX_).upper() for name in ["first_name","last_name"] if pinfo.getNodeData(name,_LATEX_) ]),color="Maroon",large=True))
        content.append("")
        content.append("\\vspace{0.15cm}")
        content.append("")
        titles=pinfo.getNodeData("titles")
        for title in titles:
            content.append("\\hspace{2.5cm}\\textit{"+getViewSpecificNode(title["title"],_LATEX_)+\
                           ",} "+getViewSpecificNode(title["location"],_LATEX_))
        content.append("")
        content.append("\\vspace{0.5cm}")
        content.append("")
        content.append(getSectionHeader("Personal Information"))
        content.append("")
        content.append("\\vspace{-0.2cm}")
        content.append("")
        entry_date="email"
        entry_title=getLatexHyperlink("mailto:"+pinfo.getNodeData("email",_LATEX_),pinfo.getNodeData("email",_LATEX_))
        content.append(getEntry(date=entry_date,title=entry_title))
        content.append("")
        content.append("\\vspace{-0.75cm}")
        content.append("")
        entry_date="website"
        entry_title=getLatexHyperlink(pinfo.getNodeData("homepage",_LATEX_))
        content.append(getEntry(date=entry_date,title=entry_title))
        content.append("")
        content.append("\\vspace{-0.75cm}")
        content.append("")
        entry_date="phone"
        entry_title=""
        #add flag for mobile
        if True:
            entry_title+="(M) "
            mobile_phone=pinfo.getNodeData("mobile_phone")
            entry_title+=getPhoneNumber(mobile_phone)
            entry_title+=_DOT_DELIMITER_
        entry_title+="(W) "
        work_phone=pinfo.getNodeData("work_phone")
        entry_title+=getPhoneNumber(work_phone)
        content.append(getEntry(date=entry_date,title=entry_title))
        
        return content

    def getObjective():
        content=[]
        content.append(getSectionHeader("Objective"))
        content.append("")
        content.append("\\vspace{-0.75cm}")
        
        #make flag for type of resume
        if True:
            variant="educational"
        objective=obj.getNodeData(variant)
        content.append(getEntry(description=objective))

        return content
    
    def getAdvisors(advisors,title="Advisor"):
        if len(advisors)==1:
            return title+": "+uniqueEndingJoin(advisors,", "," \\& ")
        else:
            return title+"s: "+uniqueEndingJoin(advisors,", "," \\& ")

    def getEducation():
        content=[]
        content.append(getSectionHeader("Education"))
        content.append("")
        
        schools=sorted(edu_obj.data.keys(),key=lambda school: edu_obj.data[school]['order'],reverse=True)
        for school in schools:
            entry_margin=edu_obj.getNodeData([school,"degree"],_LATEX_)
            entry_date=edu_obj.getNodeData([school,"duration"],_LATEX_)
            entry_title=edu_obj.getNodeData([school,"name"],_LATEX_)
            entry_description=""
            join_w_dots=[]
            gpa=edu_obj.getNodeData([school,"gpa"],_LATEX_)
            if gpa:
                join_w_dots.append(keepStringTogether("GPA: "+gpa))
            honors=[ getViewSpecificNode(honor,_LATEX_) for honor in edu_obj.getNodeData([school,"honors"]) if honor ]
            if honors:
                for honor in honors:
                    join_w_dots.append(keepStringTogether("\\textit{"+honor+"}"))
            college=edu_obj.getNodeData([school,"school"],_LATEX_)
            #add flag
            if False and college:
                join_w_dots.append(keepStringTogether("School: "+college))
            department=edu_obj.getNodeData([school,"department"],_LATEX_)
            if department:
                join_w_dots.append(keepStringTogether("Department: "+department))
            entry_description+=_DOT_DELIMITER_.join(join_w_dots)
            entry_description+="\\newline "
            theses=[ proj_obj.getNodeData([thesis,"title"],_LATEX_) for thesis in edu_obj.getNodeData([school,"theses"]) if thesis ]
            if theses:
                if len(theses)>1:
                    for i,thesis in enumerate(theses):
                        entry_description+=_ORDINALS_[i]+" Thesis: \\textit{"+thesis+"}"
                        entry_description+="\\newline "
                else:
                    entry_description+="Thesis: \\textit{"+theses[0]+"}"
                    entry_description+="\\newline "
            #no description, do in research section
            advisors=[ " ".join( [ people_obj.getNodeData([advisor,name],_LATEX_) for name in ["first_name","middle_name","last_name"] if people_obj.getNodeData([advisor,name],_LATEX_) ] ) for advisor in edu_obj.getNodeData([school,"advisors"]) if advisor ]
            if advisors:
                entry_description+=getAdvisors(advisors)
            #content.append(getDescription(edu_obj.getNodeData([school,"degree"],_LATEX_),misc))
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getResearchExperience():
        content=[]
        content.append(getSectionHeader("Research"))
        content.append("")
        
        experiences=sorted(proj_obj.data.keys(),key=lambda experience: proj_obj.data[experience]['order'],reverse=True)
        for experience in experiences:
            entry_margin=inst_obj.getNodeData([proj_obj.getNodeData([experience,"institution"]),"name"],_LATEX_)
            entry_date=proj_obj.getNodeData([experience,"duration"],_LATEX_)
            entry_title=proj_obj.getNodeData([experience,"title"],_LATEX_)
            entry_description=""
            descriptions=[ getViewSpecificNode(description,_LATEX_) for description in proj_obj.getNodeData([experience,"description"],_LATEX_) if description ]
            presentation_nodes=[ presentations_obj.data[presentation] for presentation in proj_obj.getNodeData([experience,"presentations"],_LATEX_) if presentation ]
            presentations=[]
            for node in presentation_nodes:
                presentations+=getPresentationItems(node,_LATEX_)
            highlights=[ getViewSpecificNode(highlight,_LATEX_) for highlight in proj_obj.getNodeData([experience,"highlights"],_LATEX_) if highlight ]
            advisors=[ " ".join( [ people_obj.getNodeData([advisor,name],_LATEX_) for name in ["first_name","middle_name","last_name"] if people_obj.getNodeData([advisor,name],_LATEX_) ] ) for advisor in proj_obj.getNodeData([experience,"advisors"]) if advisor ]
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
        content.append(getSectionHeader("Teaching Experience"))
        content.append("")

        experiences=sorted(teach_obj.data.keys(),key=lambda experience: teach_obj.data[experience]['order'],reverse=True)
        for experience in experiences:
            entry_margin=teach_obj.getNodeData([experience,"title"],_LATEX_)#
            entry_date=teach_obj.getNodeData([experience,"duration"],_LATEX_)
            entry_title=", ".join([teach_obj.getNodeData([experience,"course"],_LATEX_),inst_obj.getNodeData([teach_obj.getNodeData([experience,"institution"]),"name"],_LATEX_)])
            entry_description=""
            descriptions=[ getViewSpecificNode(description,_LATEX_) for description in teach_obj.getNodeData([experience,"description"],_LATEX_) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
            highlights=[ getViewSpecificNode(highlight,_LATEX_) for highlight in teach_obj.getNodeData([experience,"highlights"],_LATEX_) if highlight ]
            if highlights:
                entry_description+=createBullets(highlights)+" "
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")
        
        #need to add -vspace
        #content.append()

        return content

    def getPress():
        content=[]
        content.append(getSectionHeader("Press and News Releases"))
        content.append("")

        releases=sorted(press_obj.data.keys(),key=lambda release: press_obj.data[release]['order'],reverse=True)
        for release in releases:
            entry_margin=press_obj.getNodeData([release,"organization"],_LATEX_)
            entry_date=press_obj.getNodeData([release,"date"],_LATEX_)
            entry_title="\\textit{``"+press_obj.getNodeData([release,"title"],_LATEX_)+"''}"
            entry_description=""
            descriptions=[ getViewSpecificNode(description,_LATEX_) for description in press_obj.getNodeData([release,"description"],_LATEX_) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
            url=press_obj.getNodeData([release,"url"],_LATEX_)
            if url:
                entry_description+=getLatexHyperlink(fixStringLatex(url))
                #entry_description+="\\newline "
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getWorkExperienceAndSkills():
        content=[]
        content.append(getSectionHeader("Work Experience and Skills"))
        content.append("")

        experiences=sorted(work_obj.data.keys(),key=lambda experience: work_obj.data[experience]['order'],reverse=True)
        for experience in experiences:
            entry_margin=work_obj.getNodeData([experience,"title"],_LATEX_)
            entry_date=work_obj.getNodeData([experience,"duration"],_LATEX_)
            entry_title=work_obj.getNodeData([experience,"organization"],_LATEX_)
            #if not entry_title:
            #    entry_title=entry_margin
            #    entry_margin=""
            entry_description=""
            descriptions=[ getViewSpecificNode(description,_LATEX_) for description in work_obj.getNodeData([experience,"description"],_LATEX_) if description ]
            if descriptions:
                entry_description+=_DOT_DELIMITER_.join(descriptions)
            highlights=[ getViewSpecificNode(highlight,_LATEX_) for highlight in work_obj.getNodeData([experience,"highlights"],_LATEX_) if highlight ]
            if highlights:
                entry_description+=createBullets(highlights)+" "
            supervisors=[ " ".join( [ people_obj.getNodeData([supervisor,name],_LATEX_) for name in ["first_name","middle_name","last_name"] if people_obj.getNodeData([supervisor,name],_LATEX_) ] ) for supervisor in work_obj.getNodeData([experience,"supervisors"]) if supervisor ]
            if supervisors:
                if description and not highlights:
                    entry_description+="\\newline "
                entry_description+=getAdvisors(supervisors,title="Supervisor")
            content.append(getEntry(margin=entry_margin,date=entry_date,title=entry_title,description=entry_description))
            content.append("")

        return content

    def getAwards():
        content=[]
        content.append(getSectionHeader("Education"))
        content.append(getTitle("2011-2012","The University of California, Berkeley"))
        misc=""
        misc+="GPA: 8.0\\ \\ $\\cdotp$\\ \\ \\textit{First Class Honours}\\ \\ $\\cdotp$\\ \\ "
        misc+="School: Business and Administration\\newline Thesis: \\textit{Money Is The Root Of All Evil -- Or Is It?}\\newline "
        misc+="Description: This thesis explored the idea that money has been the cause of untold anguish and suffering in the world. "
        misc+="I found that it has, in fact, not.\\newline "
        misc+="Advisors: Prof.~James \\textsc{Smith} \\& Assoc. Prof.~Jane \\textsc{Smith}"
        content.append(getDescription("Masters of Commerce",misc))

        return content

    def getActivities():
        #qualify as professional, outreach, extra curricular
        content=[]
        content.append(getSectionHeader("Education"))
        content.append(getTitle("2011-2012","The University of California, Berkeley"))
        misc=""
        misc+="GPA: 8.0\\ \\ $\\cdotp$\\ \\ \\textit{First Class Honours}\\ \\ $\\cdotp$\\ \\ "
        misc+="School: Business and Administration\\newline Thesis: \\textit{Money Is The Root Of All Evil -- Or Is It?}\\newline "
        misc+="Description: This thesis explored the idea that money has been the cause of untold anguish and suffering in the world. "
        misc+="I found that it has, in fact, not.\\newline "
        misc+="Advisors: Prof.~James \\textsc{Smith} \\& Assoc. Prof.~Jane \\textsc{Smith}"
        content.append(getDescription("Masters of Commerce",misc))

        return content

    def getPublications():

        content=[]
        content.append(getSectionHeader("Publications"))
        content.append(getTitle("January 2013","Publication Title"))
        misc=""
        misc+="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut nisl tellus, sodales non pulvinar in, adipiscing "
        misc+="sit amet purus. Suspendisse sed facilisis diam. Sed ornare sem nec justo adipiscing nec venenatis lectus "
        misc+="commodo. Mauris non neque ligula. Pellentesque sed quam eu felis iaculis iaculis ac a leo. Suspendisse neque neque, placerat "
        misc+="id adipiscing et, elementum eu sem.\\\\ Authors: John \\textsc{Smith}, ~James "
        misc+="\\textsc{Smith}"
        content.append(getDescription("Full Journal Name",misc))

        return content

    spacing=0

    content=[]
    content+=getHeader()
    content.append("")
    content.append("\\begin{document}")
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
    #content.append("\\vspace{"+str(spacing)+"em}")
    """
    content+=getPublications()
    content.append("\\vspace{"+str(spacing)+"em}")
    """

    content.append("")

    content.append("")
    #content.append("\\end{cv}")
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
