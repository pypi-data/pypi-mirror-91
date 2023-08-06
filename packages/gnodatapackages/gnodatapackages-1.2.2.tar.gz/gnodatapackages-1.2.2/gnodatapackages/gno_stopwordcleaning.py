#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re 
import string
import os
import sys

from os.path import join


# In[18]:


# choose the stopwordslist
# when found, will be replaced with ""

def Remove_stopwords(Master_pd, stopwordlist, *argv):  
     # ACTION NEEDED:  for project_folder : one of the below should wok. __file__ doesnt work on local 
    dir_path = os.path.dirname(os.path.realpath(__file__))  
#     dir_path = os.path.abspath(os.path.dirname(sys.argv[1])) #when this is set to 0 on local, it shows the anaconda paths

    filepath = os.path.join(dir_path, stopwordlist)
    file = open(filepath, "r", encoding = "utf8", errors = 'backslashreplace')
    StopWords = pd.read_csv(file, sep = ",", usecols = ["tosearch", "toreplace"], 
                              skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()

    for arg in argv: 
        Master_pd[arg] = Master_pd[arg].str.upper()
        Master_pd[arg].replace(to_replace = StopWords["tosearch"].str.upper().tolist(), 
                               value = "", inplace=True, regex=True)
        Master_pd[arg] = [c.replace('  ', ' ').strip(string.whitespace) for c in Master_pd[arg]] #the strip only works for bef and aft not extra spaces in the middle

    return Master_pd


# In[22]:


# from gno data package, to remove all the stopwords 

#  this is for one PD and 1 or more columns to review and clean/replace.
# because this is just to clean up company name, am assuming there wont be many columns - for loop
# this is different from remove_stopwords because there is a to_replace_with 

def Replace_CoStopwords(Master_pd, *argv):  
    # ACTION NEEDED:  for project_folder : one of the below should wok. __file__ doesnt work on local 
    # project_folder = os.path.dirname(os.path.realpath(__file__))  
#     dir_path = os.path.abspath(os.path.dirname(sys.argv[1])) #when this is set to 0 on local, it shows the anaconda paths
    dir_path = os.path.dirname(os.path.realpath(__file__))

    filepath = os.path.join(dir_path, "coname_stopwordsWescape_gno.csv")
    file = open(filepath, "r", encoding = "utf8", errors = 'backslashreplace')
    CoStopWords = pd.read_csv(file, sep = ",", usecols = ["tosearch", "toreplace"], 
                              skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()

    value_to_replace = CoStopWords["tosearch"].str.upper().tolist()
    replace_value_with_this = CoStopWords["toreplace"].str.upper().tolist()

    for arg in argv: 
        Master_pd[arg] = Master_pd[arg].str.upper()
        Master_pd[arg].replace(to_replace = value_to_replace, 
                               value = replace_value_with_this, inplace=True, regex=True)
        Master_pd[arg] = [c.replace('  ', ' ').strip(string.whitespace) for c in Master_pd[arg]] #the strip only works for bef and aft not extra spaces in the middle
  
    return Master_pd
