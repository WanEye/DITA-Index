import os
import sys
from shutil import copyfile


def R10AgetDITAfiles():
    """
    Determine the current directory.
    Get all .dita files with full path in the current directory and subdirectories.
    Put all these .dita files in list global_fileList    
    """
    routine = 'R10A'
    #
    global global_current_Dir
    global global_filesList
    global_filesList = []
    
    global_current_Dir=os.getcwd()
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
    routine='R10B '
    #
    global global_terms
    
    indextermFile = global_current_Dir + "/indexterms.txt"
    try: 
        indexterms = open(indextermFile)
        terms = indexterms.read()
    except IOError:
        print ("ERROR: " + routine + "opening or read file " + indextermFile)
        sys.exit()
        
    global_terms=terms.splitlines()
  
    indexterms.close()
    
    return


def R10CbackupDITAfiles():
    """
    Make a backup of all .dita files because the program cbanges the files.
    """
    routine = 'R10C '
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
            print ("ERROR: Cannot make directory " + routine + global_current_Dir + backup_Dir)
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


def R10initPrg():
    """
    Gathers all information and puts the information into an array.
     Back up the .dita files.
    """
    routine = 'R10 '
    # 
    R10AgetDITAfiles()
    R10BgetIndexterms()
    R10CbackupDITAfiles()
    
    return


def R30procTerm(DITAfile, term):
    """
    Open the .dita file and puts the content into a string.
    Add the index terms between indexterm tags.
    Overwrite the original file.
    Close the file.
    """
    
    routine = 'R30 '
    #
    replaceStr = term + '<indexterm>' + term + '</indexterm>'
    
    try:
        DITA = open(DITAfile, "r+")
        cont = DITA.read()
    except IOError:
        print("ERROR: Cannot open " + routine + DITAfile)
        sys.exit()
         
    replacedContent = cont.replace(term, replaceStr)
    
    if replacedContent != cont:
        DITA.seek(0)
        DITA.write(replacedContent)
    DITA.close()
    
    return

   
def R19finPrg():   
    """
    Notify the user that the program is ready.
    """
    routine = 'R19 ' 
    #
    print ("added indexterms in DITA files in" + global_current_Dir)   
    return


##### MAIN #####
def R00Main():
    routine = 'R00 '
    #  
    R10initPrg()
    for DITAfile in global_filesList:
        for term in global_terms:
            R30procTerm(DITAfile, term)
    R19finPrg()
    
    return
  
    
R00Main()