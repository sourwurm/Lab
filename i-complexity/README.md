# I-Complexity

Scripts, notebooks, and transformed data pertaining to the i-complexity project.

- Dimension_Clean - Notebook showcasing how the functions work
- DimBook - Notebook that provides an easy way to apply these functions outside of the command line. Contains functionality for applying to both single files or entires folders.
- DimScript_cmd - Script that runs the function from the command line.
- functions - Contains functions for importing into DimBook and DimScript_cmd.

Things to keep in mind:

- Make sure functions.py is in the same folder as the notebooks. OR install the functions.py file to your python distribution.

master function
---------------
- REQUIRES 3 parameters
	1. A filename ('eng.txt')
	2. A directory to look for the file 'C:\\---\Downloads\---\folder' or '\folder', depending on
	   your working directory (where your current instance of python is running).
	3. A directory to SAVE the file in. Similar to 2, but ideally it's a different folder in order
	   to keep the old file and the new file seperate and organized.

- OPTIONAL PARAMETERS
	1. dim1 
	2. dim2 
	3. dim3
		*Let's you specify dimensions to order the features by. Dimensions that aren't specified
		 will be ordered normally (alphabetically).
		* ex: dim1 = 'Person' -> All features pertaining to the 'Person' dimension will appear first in the 'features' column. Every feature that is NOT in the 'Person' dimensions will be ordered alphabetically, and appear after all of the 'Person' features.
		* if using dim2 and dim3 too: dim1 appears first, followed by dim2, and then dim3. Un-specified dimensions will follow afterwards, again in alphabetical order (by dimension).


All functions can be run independently through imports in a notebook, or through the commandline.
Instructions on how to make a call with the commandline while including arguments are here:

https://www.stefaanlippens.net/simple-cli-argument-handling-in-python/

So for example, 

$ python DimScript.py 'eng.txt' '\Downloads' '\Documents' 'Part of Speech' 'Person' 'Number'

If there's any syntax error, the command line should let you know.

If you ever wanna do a bunch of files in a batch, I've included a code block at the end of the Dimension Clean and DimBook 
notebooksthat let you specify directories to look for unimorph files in,
and where to save them to as well.


	
