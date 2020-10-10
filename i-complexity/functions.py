#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import re

import os

def alphabetizer(string):
    
    #alphabetizes elements within a string
    
    st_lst = string.split(';')
    st_lst = sorted(st_lst)
    alph = ';'.join(st_lst)
    
    return alph

def dim_ord(string, dim1 = False, dim2 = False, dim3 = False):
    
    '''
    PURPOSE
    -------
    - Orders features by dimension
    - Can theoretically be applied to a single string by simply calling the function dim_ord('V;V.MSDR;SG')
    - If applying to an entire column, must be done so using the .apply() method
    - A maximum of three (optional) dimensions can be inputted.
        - If a dimension is specified, features within that dimension will be at the beginning of the new string. 
        - All features not within that dimension will follow, but will still be ordered alphabetically by dimension.
    - if alphabetizer was previously run, then dimension features will also be in alphabetical order
    
    PARAMETERS
    ----------
    string | A string containing features seperated by a semicolon.
    
    dim1   | (Optional) A string denoting a dimension as worded in the Unimorph Schema User Guide Appendix 1.
                        If dim2 and dim3 are specified, dim1 will appear first.
    
    dim2   | (Optional) A string denoting a dimension as worded in the Unimorph Schema User Guide Appendix 1.
                        If dim1 is specified, dim1 will appear first, followed by dim2.
                        Will raise error if dim1 is False (dim1 must exist for dim2 to be used).
    
    dim3   | (Optional) A string denoting a dimension as worded in the Unimorph Schema User Guide Appendix 1.
                        If dim1 and dim3 are specified, dim1 will appear first, followed by dim2, and lastly dim3.
                        Will raise error if dim1 and dim2 are False (dim1 and dim2 must exist for dim3 to be used).
    
    RETURNS
    ---------
    A string with features ordered by dimension, or an alternate order specified by the user.
    '''
    
    #mappings from dimensions to features
    mappings = {
                'Aktionsart' : ['accmp', 'ach', 'acty', 'atel', 'dur', 'dyn', 'pct', 'semel', 'stat', 'tel'],

                'Animacy' : ['anim', 'hum', 'inan', 'nhum'],

                'Argument' : ['argac3s'],

                'Aspect' : ['hab', 'ipfv', 'iter', 'pfv', 'prf', 'prog', 'prosp'],

                'Case' : ['abl', 'abs', 'acc', 'all', 'ante', 'apprx', 'apud', 'at', 'avr', 
                          'ben', 'byway', 'circ', 'com', 'compv', 'dat', 'eqtv', 'erg', 'ess', 
                          'frml', 'gen', 'in', 'ins', 'inter', 'nom', 'noms', 'on', 'onhr', 
                          'onvr', 'post', 'priv', 'prol', 'propr', 'prox', 'prp', 'prt', 'rel',
                          'rem', 'sub', 'term', 'trans', 'vers', 'voc'],

                'Comparison' : ['ab' 'cmpr' 'eqt' 'rl' 'sprl'],

                'Definiteness' : ['f', 'indf', 'nspec', 'spec'],

                'Deixis' : ['abv', 'bel', 'even', 'med', 'noref', 'nvis', 
                            'phor', 'prox', 'ref1', 'ref2', 'remt', 'vis'],

                'Evidentiality' : ['assum', 'aud', 'drct', 'fh', 'hrsy', 'infer', 'nfh', 'nvsen', 'quot', 'rprt', 'sen'],

                'Finiteness' : ['fin', 'nfin'],

                'Gender' : ['bantu1-23', 'fem', 'masc', 'nakh1-8', 'neut'],

                'Information Structure' : ['foc', 'top'],

                'Interrogativity' : ['decl', 'int'],

                'Language-Specific Features' : ['lgspec1', 'lgspec2'],

                'Mood' : ['adm', 'aunprp', 'auprp', 'cond', 'deb', 'ded', 
                          'imp', 'ind', 'inten', 'irr', 'lkly', 'oblig', 
                          'opt', 'perm', 'pot', 'purp', 'real', 'sbjv', 'sim'],

                'Number' : ['du', 'gpauc', 'grpl', 'invn', 'pauc', 'pl', 'sg', 'tri'],

                'Part of Speech' : ['adj', 'adp', 'adv', 'art', 'aux', 'clf', 'comp', 'conj', 
                                    'det', 'intj', 'n', 'num', 'part', 'pro', 'propn', 'v', 
                                    'v.cvb', 'v.msdr', 'v.ptcp'],

                'Person' : ['0', '1', '2', '3', '4','excl', 'incl', 'obv', 'prx'],

                'Polarity' : ['pos', 'neg'],

                'Politeness' : ['avoid', 'col', 'elev', 'foreg', 'form', 'high', 'humb', 'infm', 'lit', 
                                'low', 'pol', 'stelev', 'stsupr'],

                'Possession' : ['aln', 'naln', 'pss1d', 'pss1de', 'pss1di', 'pss1p', 'pss1pe', 
                               'pss1pi', 'pss1s', 'pss2d', 'pss2df', 'pss2dm', 'pss2p', 'pss2pf', 
                               'pss2pm', 'pss2s', 'pss2sf', 'pss2sform', 'pss2sinfm', 'pss2sm', 'pss3d', 
                               'pss3df', 'pss3dm', 'pss3p', 'pss3pf', 'pss3pm', 'pss3s', 'pss3sf', 'pss3sm',  'pssd'],

                'Switch-Reference' : ['cn_r_mn', 'ds', 'dsadv', 'log', 'or', 'seqma', 'simma', 'ss', 'ssadv'],

                'Tense' : ['1day', 'fut', 'hod', 'immed', 'prs', 'pst', 'rct', 'rmt'],

                'Valency' : ['appl', 'caus', 'ditr', 'imprs', 'intr', 'recp', 'refl', 'tr'],

                'Voice' : ['acfoc', 'act', 'agfoc', 'antip', 'bfoc', 'cfoc', 'dir', 'ifoc', 'inv', 'lfoc', 
                           'mid', 'pass', 'pfoc']}
    
    #list containing all dimension names
    dimlst = list(mappings.keys())
    
    #splitting strings into a list to access individual features
    lst = string.split(';')
    
    #empty lists and dictionary to store ordered features
    d1 = []
    d2 = []
    d3 = []
    rest_d ={}
    
    #if three dimensions are specified
    if dim1 and dim2 and dim3:
        
        #iterating through each feature in the lst
        for feat in lst:
            
            #finding the dimension each feature belongs to
            #if it belongs to one of the specified dimensions, then add it to the corresponding list
            if feat.lower() in mappings[dim1]:
                d1.append(feat)
                
            elif feat.lower() in mappings[dim2]:
                d2.append(feat)
                
            elif feat.lower() in mappings[dim3]:
                d3.append(feat)
            
            #if feature belongs to a non-specified dimension, then it will come after
            else:
    
                for dim in dimlst:
                    if feat.lower() in mappings[dim]:
                    
                        #each feature mapped to its corresponding dimension
                        rest_d[feat] = dim
        
        #sorting the keys by their values, thereby getting each feature (key) in order by dimension (value)
        rest_d = {k: v for k, v in sorted(rest_d.items(), key=lambda item: item[1])}
        
        #converting the dictionary keys (features) into a list
        rest_lst = list(rest_d.keys())
        
        #combining all of the lists into one list containing features in the desired order
        #if a given word did not contain a particular feature, this still works
        #will just be added as an empty list, which does not show up in the finalized list
        ordered = sorted(d1) + sorted(d2) + sorted(d3) + rest_lst
        
        #joining the list into a string seperated by a semi-colon
        joined = ';'.join(ordered) 
        
        #return the joined string
        return joined
    
    #same as previous, but if only dim1 and dim2 were specified
    elif dim1 and dim2 and dim3 == False:
    
        for feat in lst:
            if feat.lower() in mappings[dim1]:
                d1.append(feat)
                
            elif feat.lower() in mappings[dim2]:
                d2.append(feat)
                
            else:
                 for dim in dimlst:
                    if feat.lower() in mappings[dim]:
                        rest_d[feat] = dim

        rest_d = {k: v for k, v in sorted(rest_d.items(), key=lambda item: item[1])}

        rest_lst = list(rest_d.keys())
        
        
        ordered = sorted(d1) + sorted(d2) + rest_lst
        
        joined = ';'.join(ordered) 
        
        return joined    
    
    #same as previous, but if only dim1 was specified
    elif dim1 and dim2 == False and dim3 == False:

        for feat in lst:
            if feat.lower() in mappings[dim1]:
                d1.append(feat)

            else:
                for dim in dimlst:
                    if feat.lower() in mappings[dim]:
                        rest_d[feat] = dim

        rest_d = {k: v for k, v in sorted(rest_d.items(), key=lambda item: item[1])}

        rest_lst = list(rest_d.keys())
        

        ordered = sorted(d1) + rest_lst

        joined = ';'.join(ordered) 

        return joined    
    
    #same as previous, but with no dimensions specified
    else:
        for feat in lst:
            for dim in dimlst:
                if feat.lower() in mappings[dim]:
                    rest_d[feat] = dim

        rest_d = {k: v for k, v in sorted(rest_d.items(), key=lambda item: item[1])}

        rest_lst = list(rest_d.keys())
        
        joined = ';'.join(rest_lst)
        
        return joined
    
def pov(array):
    
    '''
    PURPOSE
    -------
    Creates a list denoting if a particular word is tagged as being for both first and second person use.
    
    PARAMETERS
    ----------
    array | An array (or dataframe column) of features. Features should be strings.
    
    RETURNS
    --------
    A list containing booleans denoting if a given array value contains a tag for both first and second person.
    '''
    
    #empty list to store booleans
    pov_lst = []
    
    #iterating through each string in the array
    for string in array:
        
        #cleaning the string
        new = re.sub('(.*[a-z]\d+.*)|(.*d+\[a-z].*)', '', string)
        
        #if a match is found for both 1st person and second person, append true
        if any(x in new for x in ['1;', ';1;', ';1']) and any(y in new for y in ['2;', ';2;', ';2']):
            pov_lst.append(True)
            
        else:
            pov_lst.append(False)
        
            
    #return the populated list
    return pov_lst

def dim_pop(df, column = 'feature'):
    
    '''
    PURPOSE
    -------
    - Populates a dataframe with columns corresponding to dimensions
    - If a given string of features contains a particular dimension: column will denote "true"
    - Otherwise, column will denote "False"
    
    PARAMETERS
    ----------
    df     | Pandas.DataFrame | Dataframe to be populated with dimension columns
    
    column |        Str       | (Optional). Name of the pandas dataframe column to be searched for features.
                                'feature' by default.
    
    RETURNS
    -------
    A dataframe containing columns that correspond to dimensions.
    '''
    
    #A dictionary that will denote if a given row contains a particular dimension
    #empty lists will be populated in upcoming loops
    res = {dimlst[i]: [] for i in range(len(dimlst))}
    
    # A list to contain the dimensions contained within each word
    word_dims = []

    #iterating through each row in the feature column
    for string in df[column]:
        #Initializing a list to contain all the dimensions found within that word
        inner = []

        #splitting the string into a list for iteration
        split_str = string.split(';')

        #goes through each feature
        #maps each feature to its corresponding dimension
        #appends the dimension to the empty list named inner
        for feat in split_str:
            [inner.append(a) for a, b in mappings.items() if feat.lower() in b]

        #appends each inner list to the word_dims list
        #word dims is now a lists of lists, where each inner list contains each words dimensions
        word_dims.append(inner)
    
    #iterating through each inner list in word_dims
    for val in word_dims:

        #iterating through each dimension
        for dim in dimlst:

            #if the dimension can be found within the rows list of dimensions
            #append True to the corresponding key in the res dictionary
            if dim in val:
                res[dim].append(True)
            #else, append False to the corresponding Key
            else:
                res[dim].append(False)

            #handles cases where a word has multiple features of the same dimensions
            #as soon as the dimension is found, it will move on to the next dimension
            #will not double count
            
    #populating dataframe columns with their corresponding dimension booleans
    for dim in dimlst:
        df[dim] = res[dim]
    return df

def master(filename, directory, save_dir, dim1 = False, dim2 = False, dim3 = False):
    
    '''
    PURPOSE
    -------
    Takes in a file, and applies all ordering functions and creates columns denoting dimension 
    and 1st/2nd person co-occurence.
    
    PARAMETERS
    ----------
    filename  | str | a .txt file from unimorph in the form 'eng.txt'. 
    
    directory | str | A directory for which to LOOK FOR the file in the form 
                      'C:\---\--\folder_name' or '\folder', depending on your working directory.
    
    save_dir  | str | A directory for which to SAVE the output csv file to in the form
                      'C:\---\--\folder_name' or '\folder', depending on your working directory.
    
    RETURNS
    -------
    A csv file containing an ordered feature column, and columns denoting dimensions and 
    1st/2nd persion dimension co-occurence
    '''
    
    
    name = filename.replace('.txt', '')
    
    df = pd.read_csv(directory + '\\' + filename, delimiter="\t", names = ['word', 'form', 'feature'])
    
    df['feature'] = df['feature'].apply(alphabetizer)
    
    
    if dim1 and dim2 and dim3:
        df['feature'] = df['feature'].apply(dim_ord, dim1, dim2, dim3)
        
    elif dim1 and dim2 and dim3 == False:
        df['feature'] = df['feature'].apply(dim_ord, dim1, dim2)
        
    elif dim1 and dim2 == False and dim3 == False:
        df['feature'] = df['feature'].apply(dim_ord, dim1)
        
    else:
        df['feature'] = df['feature'].apply(dim_ord)
    
    
    df['pov'] = pov(df['feature'])
    
    df = dim_pop(df, 'feature')
    
    return df.to_csv(save_dir + '\mod_'+ name + '.csv', index = False)
    
    

