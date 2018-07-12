import os
import sys
from shutil import copyfile
import re
from numpy.lib._iotools import LineSplitter


def R10AgetDITAfiles():
    """
    Determine the current directory.
    Get all .dita files with full path in the current directory and subdirectories.
    Put all these .dita files in list global_fileList    
    """
    routine = 'R10A: '
    R99writeLog(routine)
    #
    global global_current_Dir
    global global_filesList
    global_filesList = []
    
    global_current_Dir = os.getcwd()
    print "directory in process: " + global_current_Dir
    
    for dirpath, dirnames, filenames in os.walk(global_current_Dir):
        for filename in [f for f in filenames if f.endswith(".dita")]:
            DITAfile = os.path.join(global_current_Dir, dirpath, filename)
            global_filesList.append(DITAfile)
    return


def R10BgetIndexterms():
    
    """
    Open and read the file where you store the term that you want to put into the index.
    Put these terms into a list.
    Close the terms file.
    """
    routine = 'R10B: ' 
    #
    global global_indexTerms
    global_indexTerms = []
    R99writeLog(routine)
    print routine
    indextermFile = global_current_Dir + "/Indexterms.txt"
    try: 
        INDEXTERMS = open(indextermFile)
        global_indexTerms = INDEXTERMS.readlines()
        
    except IOError:
        print ("ERROR: " + routine + "opening or read file " + indextermFile)
        sys.exit()
        
    INDEXTERMS.close()
    
    return 


def R10CbackupDITAfiles():
    """
    Make a backup of all .dita files because the program cbanges the files.
    """
    routine = 'R10C: '
    R99writeLog(routine)
    #
    backup_Dir = global_current_Dir + '/DITAbackup/'
    
    if os.path.exists(backup_Dir):
        print "Tags <indexterm> already present."
        print "User actions:"
        print "Verify DITA code for tags <indexterm>"
        print "If you want to generate <indexterm> tags, delete " + backup_Dir 
        print "Run this program again"
        sys.exit()
    else:    
        try:
            os.makedirs(backup_Dir)
        except IOError:
            Mess = "FATAL ERROR: Cannot make directory " + routine + global_current_Dir + backup_Dir
            print Mess
            R99writeLog(Mess)
            sys.exit()
        
    for dirpath, dirnames, filenames in os.walk(global_current_Dir):
        for filename in [f for f in filenames if f.endswith(".dita")]:
            DITAfile = os.path.join(global_current_Dir, dirpath, filename)
            backup_File = backup_Dir + filename
            if not os.path.isfile(backup_File):
                try:
                    copyfile(DITAfile, backup_File)
                except IOError:
                    print("ERROR: Cannot copy " + routine + backup_File)
                    sys.exit()
    return


def R10DProcDITAMAP():
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
    for dirpath, dirnames, filenames in os.walk(global_current_Dir):
        for filename in [f for f in filenames if f.endswith(".ditamap")]:
            DITAMAPfile = os.path.join(global_current_Dir, dirpath, filename)
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
    
    routine = "R10EgetAllowedTags"
    global global_allowedTags
    global_allowedTags = []
    TAGS = open("containedBy.txt", "r")
    global_allowedTags = TAGS.readlines()
    R99writeLog(routine)
    return
          

def R10initPrg():
    """
    Gathers all information and puts the information into an array.
     Back up the .dita files.
    """
    global LOGFILE
    routine = 'R10: '
   
    LOGFILE = open('logFile.txt', 'w')
    R99writeLog('ROUTINES: MESSAGE: ADD INDEXTERM:')
    R99writeLog(routine)
    
    R10AgetDITAfiles()
    R10BgetIndexterms()
    #   R10CbackupDITAfiles()
    R10DProcDITAMAP()
    R10EgetAllowedTags()
    return


def R20initDITAfile(DITAfile):
    routine = 'R20: ' 
    
        #
    global global_content
    DITAfileRel = os.path.relpath(DITAfile)
    try:
        DITA = open(DITAfile, "r")
        global_content = DITA.read()
    except IOError:
        Mess = "FATAL READ ERROR Cannot open " + routine + DITAfileRel
        R99writeLog(Mess)
        sys.exit()
    DITA.close()
    
    # If the file contains a conref, warn the user

    if "conref" in global_content:
        mess = routine + "MANUAL ACTION REQUIRED " + DITAfileRel + " contains conref"
        R99writeLog(mess)
    
    return


def R29finDITAfile(global_content, DITAfile):
    routine = "R29 "
    #
    DITAfileRel = os.path.relpath(DITAfile)
   
    try:
        DITA = open(DITAfile, "w")
             
    except IOError:
        print("WRITE ERROR: Cannot open " + routine + DITAfile)
        sys.exit()
    
    DITA.write(global_content)
    DITA.close()
    R99writeLog(routine + DITAfileRel)
    return


def R30procTerm(DITAfile, term, tag, cont):
    """
    Open the .dita file and puts the content into a string.
    Add the index terms between indexterm tags.
    Overwrite the original file.
    Close the file.
    """
    routine = 'R30: ' 
    #
    global global_content
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
    regex = tag + ".*?" + endtag
   
    
    DITAlines = re.findall(regex, cont, re.DOTALL | re.IGNORECASE)

    for txtline in DITAlines:
        if term + ' '  in txtline or term + '<' in txtline:
            if '<indexterm>' + term not in txtline:
                txtlineNew = tag + '<indexterm>' + term + '</indexterm>'
                global_content = cont.replace(tag, txtlineNew, 1)
                print "FOUND: " + tag + term + endtag + "  " + txtline + "NEW: \n" + txtlineNew 
            
    return

   
def R19finPrg():   
    """
    Notify the user that the program is ready.
    """
    routine = 'R19: ' 
    R99writeLog(routine)
    LOGFILE.close()
    #
    print ("added indexterms in DITA files in" + global_current_Dir)
    print "The End"
    return


def R99writeLog(Msg):
    with open("logfile.txt", "a") as LOGFILE:
        LOGFILE.write(Msg + "\n")
    # print Msg
    return


##### MAIN #####
def R00Main():
    #  
    global global_content
    global_content = ""
    R10initPrg()
    for DITAfile in global_filesList:
        R20initDITAfile(DITAfile)      
        for term in global_indexTerms:
            for tag in global_allowedTags:         
                R30procTerm(DITAfile, term, tag, global_content)
        R29finDITAfile(global_content, DITAfile)
    R19finPrg()
    return
  
    
R00Main()
