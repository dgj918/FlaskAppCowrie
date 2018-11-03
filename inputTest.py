# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 19:25:36 2017

@author: dgj918
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from developCorpus import *
from LDAtestv2 import *
from pandas import compat 



def readData(fileLocation):
    # Column names include: compCS, dst_ip, dst_port, eventid, isError(boolean), message, password, sensor, system, timestamp, username
    cowrieLog = pd.read_json(fileLocation, orient = 'columns', lines = True, encoding = 'utf-8')
    return cowrieLog

def filterCleanData(cowrieLog):
    # Copies just session and input columns
    cowrieLogFiltered = cowrieLog[['session','input']].copy()

    # Drops NAs
    cowrieLogFiltered = cowrieLogFiltered.dropna(subset=['input'], how='any')

    # Groups the sessions together and seperates each command by a comma
    cowrieLogFiltered = cowrieLogFiltered.groupby(['session'])['input'].apply(lambda x: ','.join(x)).reset_index()
    splitColumn = lambda x: pd.Series([i for i in reversed(x.split(','))])
  
    cowrieLogFiltered = cowrieLogFiltered.set_index('session')['input'].apply(splitColumn).reset_index()
    cowrieLogFiltered = cowrieLogFiltered.set_index('session')
    
    cowrieLogFiltered = cowrieLogFiltered.T
    cowrieLogFiltered = cowrieLogFiltered.fillna(0, axis = 0, inplace = False)
    return cowrieLogFiltered

def dfToDict(cowrieLogFiltered):

    cowFilter = cowrieLogFiltered.to_dict('list')
    valList = 0
    cowFilter = {key:[elem for elem in value if elem != valList] for key,value in cowFilter.iteritems()}         
    
    return cowFilter

def intEncode(self, cowrieCMDinputs):   
    # integer encode the commands in each session into a sparse matrix
    intEncode = CountVectorizer(max_features = 10000, tokenizer=lambda x: x.split(','))
    cowrieCMDsparse = intEncode.fit_transform(cowrieCMDinputs['input'].values)
    Cd = pd.DataFrame(cowrieCMDsparse.A, columns=intEncode.get_feature_names())
    return Cd

#fileLocation = 'C:/Users/212547746/Desktop/Personal/Project/cowrie2.json'
fileLocation = 'C:\Users\dgj918\C\Desktop\UofLClasses\Project\Honeypot\Data\cowrie3.json'

s1 = readData(fileLocation)
s2 = filterCleanData(s1)
s3 = dfToDict(s2)
corpus = Corpus()

for session, data in s3.iteritems(): 
    corpus.addDocument(session, data)

print "Documents: ", len(corpus)
print "CMDs: ", sum(len(doc) for doc in corpus)
print "unique types: ", len(corpus.alphabet)


#newLDA = LDA(corpus, 5, 100)
#newLDA.inf()


    
