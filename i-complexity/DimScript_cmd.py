#!/usr/bin/env python
# coding: utf-8

# In[4]:


# This adds the directory above to our Python path
# This is so that we can add import our custom python module code into this script
import sys
sys.path.append('../')

### imports
import pandas as pd
import numpy as np
import re
import os

### importing our functions
from functions import alphabetizer, dim_ord, pov, dim_pop, master 


# In[ ]:


if __name__ == '__main__':
    
    # Map command line arguments to function arguments.
    master(*sys.argv[1:])

