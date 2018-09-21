# DITA-Index

This utility adds tags `<indexterm>` to DITA files. You define the terms that you want to include into the index in file `indexterm.txt`.

You need the following files.
1. DITA files
2. indexterm.txt in the working directory
3. containedBy.txt in the working directory

To run the utility, you need Python. 

## Contents

* `DITAtest` folder with sample DITA project
* `indexterms.txt` sample input file with sample index terms
* `containedBy.txt` list of tags that can contain the `<indexterm>` tag according to DITA rules
* `indextermGenerator.jpg` Jackson diagram of the program structure
* `Index_m_all.py` Python code

## Output
Log file that contains information about the routines that the program ran and the indexterms that the program added.

## Generating the index

### Before you begin
1. Verify that Python is installed and works from the DITAMAP directory.

To verify:
  
  1. Open a command line. For Windows: start `cmd`. For Linux: `Ctrl + Alt + t`. For Mac: Terminal.
  2. Navigate to the directory where your DITAMAP sits.
  3. Type `python --version`. 
 #### Result 
 If you see `Python <version>`, Python works properly.
  
### Procedure
1. Navigate to the directory where your DITAMAP file sits.
2. Copy `containedBy.txt` to the directory where your DITAMAP file sits.
3. Copy `Index_m_all.py` to the directory where your DITAMAP file sits. 
4. Create a file `indexterms.txt` in the directory where your DITAMAP file sits. 
5. Write the terms that you want to include in the index in `indexterms.txt`.
4. Type `python Index_m_all.py`.

#### Result
* The DITAMAP file contains the `<indexlist>` tag.
* The DITA files contains tags `<indexterm>`.
* The DITA output comprises a document with index. 



