'''
Created on 19 sep. 2018

@author: WanEye
'''
import errno
import os
import sys
import shutil
import re

# globals
# g_content content DITA file
#
#
# Generic functions
def copy(src, dest):
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the source is not a folder
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print(src + ' Folder not copied. Error: %s' % e)
            
    return

def stripFile(fileContent):
    # remove all new lines
    # to format and indent again, use Oxygen Tools > Format and Indent files ... 
    fileContent = fileContent.replace('\n', " ")
        # replace multi spaces with single spaces
    while ("  " in fileContent):
        fileContent = fileContent.replace("  ", " ")
    
    return (fileContent)

# Structural functions
def R10AgetDITAfiles():
#     Determine the current directory.
#     Get all .dita files with full path in the current directory and subdirectories.
#     Put all these .dita files in list g_fileList    
    
    routine = 'R10A: '
    R99writeLog(routine)
    #
    global g_current_Dir
    global g_filesList
    g_filesList = []
    
    g_current_Dir = os.getcwd()
    print "directory in process: " + g_current_Dir
    
    for dirpath, dirnames, filenames in os.walk(g_current_Dir):
        for filename in [f for f in filenames if f.endswith(".dita")]:
            DITAfile = os.path.join(g_current_Dir, dirpath, filename)
            g_filesList.append(DITAfile)
        
        for filename in [f for f in filenames if f.endswith(".xml")]:
            DITAfile = os.path.join(g_current_Dir, dirpath, filename)
            g_filesList.append(DITAfile)
    
            
    R99writeLog("The program found the following files: ")
    for filesFromList in g_filesList:
        R99writeLog(filesFromList)
    
    return


def R10BgetIndexterms():
#     Open and read the file where you store the term that you want to put into the index.
#     Put these terms into a list.
#     Close the terms file.

    routine = 'R10B: ' 
    R99writeLog(routine)
    #
    global g_indexTerms
    g_indexTerms = []
    R99writeLog(routine)
    indextermFile = g_current_Dir + "/indexterms.txt"
    try: 
        INDEXTERMS = open(indextermFile)
        g_indexTerms = INDEXTERMS.readlines()
        
    except IOError:
        print ("ERROR: " + routine + "opening or read file " + indextermFile)
        sys.exit()
        
    INDEXTERMS.close()
    
    # Remove newlines
    for index in range(len(g_indexTerms)):
        g_indexTerms[index] = g_indexTerms[index].rstrip('\n')
        
    return 


def R10Cbackup(): 
    routine = 'R10C: '
    R99writeLog(routine)
    #
    # Make a backup of all .dita files because the program changes the files.
    #
    backup_Dir = g_current_Dir + '/DITAbackup/'
    
    if os.path.exists(backup_Dir):
        errorR10C = """
        <indexterm> already present.
        User actions:
        Verify DITA code for <indexterm>
        If you want to generate the tags again, delete """
        print errorR10C
        print "        " + backup_Dir 
        print "        Then, run this program again."
        
        sys.exit()
    
    copy(g_current_Dir, backup_Dir)
    return


def R10DinitDITAMAP():
    # Find all bookmap DITAMAP files
    # Determine location of <indexlist>: before <reltable> or before </bookmap>
    # Write the <indexlist> tag in each DITAMAP file
    #
    routine = 'R10D: '
    R99writeLog(routine)
    
    maplist = []
    backmatter = '''
    <!-- Begin: add index_m_all.py R10D -->
    <backmatter>
        <booklists>
          <indexlist/>
        </booklists>
    <!-- End -->
    </backmatter>
    '''
    for dirpath, dirnames, filenames in os.walk(g_current_Dir):
        for filename in [f for f in filenames if f.endswith(".ditamap")]:
            DITAMAPfile = os.path.join(g_current_Dir, dirpath, filename)
            maplist.append(DITAMAPfile)
    for MAPfile in maplist:
        DITAMAP = open(MAPfile, "r")
        content = DITAMAP.read()
        DITAMAP.close()
        
        if ("<backmatter" not in content):
            if '<reltable' in content:
                content = content.replace('<reltable' , backmatter + '<reltable' , 1)
            else:    
                content = content.replace('</bookmap>', backmatter + '</bookmap>', 1)
            
        if ("<booklists>" not in content):
            booklists = '''<!-- Begin: add index_m_all.py R10D -->
        <booklists>
            <indexlist/>
        </booklists>
    <!-- End -->
    </backmatter>
            '''
            content = content.replace('</backmatter>', booklists)
        
        if ("<indexlist" not in content):
            indexlist = '''<!-- Begin: add index_m_all.py routine -->
                <indexlist/>
        </booklists>
            <!-- End -->
            '''
            content = content.replace("</booklists>", indexlist)
        
        DITAMAP = open(MAPfile, "w")
        DITAMAP.write(content)                
    return           

          
def R10EgetAllowedTags():   
    routine = "R10E"
    R99writeLog(routine)
    #
    global g_allowedTags
    g_allowedTags = []
    TAGS = open("containedBy.txt", "r")
    g_allowedTags = TAGS.readlines()
    R99writeLog(routine)
    # Remove newlines
    for index in range (len(g_allowedTags)):
        g_allowedTags[index] = g_allowedTags[index].rstrip('\n')    
    
    return
          

def R10initPrg():
    routine = "R10"
    R99writeLog(routine)
#     Gathers all information and puts the information into an array.
#     Back up the .dita files.
 
    global LOGFILE
    routine = 'R10: '
   
    LOGFILE = open('logFile.txt', 'w+')
    R99writeLog('ROUTINES: MESSAGE: ADD INDEXTERM:')
    R99writeLog(routine)
    
    R10AgetDITAfiles()
    R10BgetIndexterms()
    R10Cbackup()
    R10DinitDITAMAP()
    R10EgetAllowedTags()
    
    return


def R20initDITAfile(DITAfile):
    routine = 'R20: ' 
    R99writeLog(routine)
    #
    global g_content
    DITAfileRel = os.path.relpath(DITAfile)
    try:
        DITA = open(DITAfile, "r")
    except IOError:
        Mess = "FATAL READ ERROR Cannot open " + routine + DITAfileRel
        R99writeLog(Mess)
        sys.exit()
       
    g_content = DITA.read()
    DITA.close()
    
    g_content = stripFile(g_content)
            
    # If the file contains a conref, warn the user
    if "conref" in g_content:
        mess = routine + "WARNING: MANUAL ACTION REQUIRED " + DITAfileRel + " contains conref"
        R99writeLog(mess)
    
    return g_content


def R29finDITAfile(g_content, DITAfile):
    routine = "R29 "
    #
    DITAfileRel = os.path.relpath(DITAfile)
   
    try:
        DITA = open(DITAfile, "w")
             
    except IOError:
        print("WRITE ERROR: Cannot open " + routine + DITAfile)
        sys.exit()
    
    DITA.write(g_content)
    DITA.close()
    R99writeLog(routine + DITAfileRel)
    return


def R30procTerm(DITAfile, term, tag, cont):
    routine = 'R30 '
    R99writeLog(routine)
    #
#     Open the .dita file and puts the content into a string.
#     Add the index terms between indexterm tags.
#     Overwrite the original file.
#     Close the file.
    
    global g_content
    DITAfileRel = os.path.relpath(DITAfile)
    
    tag = tag.rstrip('\n')
    term = term.rstrip('\n')
           
    if '"' + term in cont:
        Warning1 = routine + "WARNING1 term contains quote in file " + DITAfileRel + " for term " + term
        print Warning1
        R99writeLog(Warning1)
        
    if "/" + term + "/" in cont:
        Warning2 = routine + "WARNING2 term contains slash in file " + DITAfileRel + " for term " + term
        print Warning2
        R99writeLog(Warning2)
        
    if term + "_" in cont:
        Warning3 = routine + "WARNING3 term contains underscore in file " + DITAfileRel + " for term " + term
        print Warning3
        R99writeLog(Warning3)    

    endtag = tag[:1] + "/" + tag[1:]
    
    cont = cont.replace(endtag, endtag + '\n')
    
    # find only the words that match the whole term (case-insensitve) 
    regex = "[\s|>]"+ term +"[\s|<]"+ ".*" + endtag
    indextag = '<indexterm>' + term  + '</indexterm>' + endtag
    
    DITAlines = re.findall(regex, cont, re.IGNORECASE)
    
    for txtline in DITAlines:  
        txtlineNew = txtline.replace(endtag, indextag)  
        cont = cont.replace(txtline, txtlineNew)
            
    g_content = cont
    g_content = stripFile(g_content)
        
    return 

   
def R19finPrg():   
    routine = 'R19 '
    R99writeLog(routine)
    
    #
    logContent = LOGFILE.read()
    if 'WARN' in logContent:
        print "PROGRAM ENDS WITH WARNINGS. SEE LOGFILE."
#   Notify the user that the program is ready.
    print ("added indexterms in DITA files in" + g_current_Dir)
    print "The End"
    
    LOGFILE.close()
    
    return


def R99writeLog(Msg):
    with open("logFile.txt", "a+") as LOGFILE:
        LOGFILE.write(Msg + "\n")
    
    return


##### MAIN #####
def R00Main():
    R10initPrg()
    for DITAfile in g_filesList:
        R20initDITAfile(DITAfile)      
        for term in g_indexTerms:
            if term in g_content or term.capitalize() in g_content:
                for tag in g_allowedTags:                   
                    if tag in g_content:
                        R30procTerm(DITAfile, term, tag, g_content)
        R29finDITAfile(g_content, DITAfile)
    R19finPrg()
    
    return
  
    
R00Main()
