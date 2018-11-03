# -*- coding: utf-8 -*-
"""
Created on Wed Nov 08 18:43:21 2017

@author: dgj918
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import scipy.sparse as sp



def readData(fileLocation):
    # Column names include: compCS, dst_ip, dst_port, eventid, isError(boolean), message, password, sensor, system, timestamp, username
    cowrieLog = pd.read_json(fileLocation, orient = 'columns', lines = True, encoding = 'utf-8')
    return cowrieLog

def filterCleanData(cowrieLogRaw):
    # Copies just session and input columns
    cowrieLogFiltered = cowrieLogRaw[['session','input']].copy()
    
    # Drops NAs
    cowrieLogFiltered = cowrieLogFiltered.dropna(subset=['input'], how='any')
    
    # Groups the sessions together and seperates each command by a comma
    cowrieLogFiltered = cowrieLogFiltered.groupby(['session'])['input'].apply(lambda x: ' '.join(x)).reset_index()
    
    return cowrieLogFiltered

def intEncode(cowrieCMDinputs):
    # integer encode the commands in each session into a sparse matrix
    intEncode = CountVectorizer(max_df = 1, max_features = 5000, tokenizer=lambda x: x.split(', '))
    cowrieCMDsparse = intEncode.fit_transform(cowrieCMDinputs['input'].values)
    return cowrieCMDsparse

def checkSparseInput(matrix):
    sparseCheck = sp.issparse(matrix)
    if sparseCheck:
        return matrix
    else:
        print "input must be a sparse matrix."