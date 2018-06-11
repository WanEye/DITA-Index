# DITA-Index

This utility adds tags `<indexterm>` to DITA files. You need the following files.
1. DITA files
2. indexterm.txt in the working directory

To generate the index in the DITA output, the DITAMAP file must contain the <indexlist> tag.

To run the utility, you need Python. 

## Contents

* `DITAtest` folder with sample DITA project
* `indexterm.txt` sample input file with sample index terms
* `indextermGenerator.jpg` Jackson diagram of the program structure
* `Index_m_all.py` Python code

## Output
Log file that contains information about the routines that the program ran and the indexterms that the program added.

## Generating the index

### Before you begin
1. Verify that your DITAMAP file contains the `<indexterm>` tag.
2. Verify that Python is installed and works from the DITAMAP directory.

To verify:
  
  1. Open a command line. For Windows: start cmd. For Linux: Ctrl + Alt + t. For Mac: Terminal.
  2. Navigate to the directory where your DITAMAP sits.
  3. Type `python --version`. 
 #### Result 
 If you see `Python <version>`, Python works properly.
  
### Procedure
1. Navigate to the directory where your DITAMAP file sits.
2. Copy `indexterm.txt` to the directory where your DITAMAP file sits.
3. Copy `Index_m_all.py` to the directory where your DITAMAP file sits. 
4. Type `python Index_m_all.py`.

#### Result
* The DITA files contains tags `<indexterm>`.
* The DITA output comprises a document with index. 



