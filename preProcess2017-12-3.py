# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 07:37:38 2017

@author: dgj918
"""
import pandas as pd
import numpy as np
import datetime
import math

from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
from pandas import compat 

from developCorpus import *
from LDAtestv2 import *
import util

import mysql.connector
from mysql.connector import errorcode

import cPickle as pickle



class preProcessDataDTM:
    
    def __init__(self, totalDays, numWindows, outPath):
        
        self.totalDays = totalDays
        self.numWindows = numWindows
        self.outPath = outPath

    def readData(self):
        # Column names include: compCS, dst_ip, dst_port, eventid, isError(boolean), message, password, sensor, system, timestamp, username
        cowrieLog = pd.read_json(self.fileLocation, orient = 'columns', lines = True, encoding = 'utf-8')
        return cowrieLog
    
    def readWindow(self):
        windowSize = math.ceil(self.totalDays / self.numWindows)
        now = datetime.datetime.now()
        start = now.strftime("%Y-%m-%d")
        
        for window in range(self.numWindows):
            end = datetime.datetime.strptime(start, '%Y-%m-%d') - datetime.timedelta(days=windowSize)
            end = end.strftime('%Y-%m-%d')
            
            try:
                cnx = mysql.connector.connect(user='cowrieRemote', password='asj2381!@38089f!@$#438ash',
                              host='165.227.97.111',
                              database='cowrie')
                windowName = '%s - %s' % (end, start)
                cowrieCMDinputs = pd.read_sql_query('SELECT * FROM input WHERE timestamp BETWEEN \'%s\' AND \'%s\'' % (end, start), con=cnx)
                modelPath = self.word2VecPrep(windowName, cowrieCMDinputs)
                self.preProcessDTM(windowName, cowrieCMDinputs)
            except mysql.connector.Error as err:
              if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
              elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
              else:
                print(err)
            else:
              cnx.close()
                       
            start = datetime.datetime.strptime(end, '%Y-%m-%d') - datetime.timedelta(days=1)
            start = start.strftime('%Y-%m-%d')

        return modelPath

    def preProcessDTM(self, windowName, cowrieCMDinputs): 
        cowrieCMDinputs = cowrieCMDinputs.groupby(['session'])['input'].apply(lambda x: ','.join(x)).reset_index()
        sessions = list(cowrieCMDinputs['session'])
        cowrieCMDinputs = list(cowrieCMDinputs['input'])
        


        # integer encode the commands in each session into a sparse matrix
        intEncode = TfidfVectorizer(max_features = 10000, tokenizer=lambda x: x.split(','))
        cowrieCMDsparse = intEncode.fit_transform(cowrieCMDinputs)
                
        numDocs = len(sessions)

        vocab = []
        v = intEncode.vocabulary_
        
        print "----------------------------------------------------------------"
        print windowName
        print "Number of Sessions: ", numDocs
        print "Number of commands in corpus: ", len(v)
        print "----------------------------------------------------------------"
        for i in range(len(v)):
            vocab.append("")
        for voc in v.keys():
            vocab[v[voc]] = voc
        

        util.saveCorpusData(windowName, self.outPath, cowrieCMDsparse, vocab, sessions)
    
    def word2VecPrep(self, windowName, cowrieCMDinputs):
        cowrieCMDinputs = cowrieCMDinputs.groupby(['session'])['input'].apply(lambda x: ','.join(x)).reset_index()
        cowrieCMDinputs = cowrieCMDinputs.values.tolist()
        sessionTokens = []
        sessions = []
        for session, CMDs in cowrieCMDinputs:
            sessionTokens.append([cmd for cmd in CMDs.split(',')])
            sessions.append(session)
          
        model = gensim.models.Word2Vec(sessionTokens)
        modelName = "%s_CORPUS.pkl_model.bin" % windowName
        modelOutPath = self.outPath + modelName
        util.saveModel(model, modelOutPath)

        return modelOutPath


   
class preProcessDataLDA:
    
    def __init__(self, totalDays, LDAoutPath):
        
        self.totalDays = totalDays
        self.LDAoutPath = LDAoutPath
   
    def readDB(self):

        now = datetime.datetime.now()
        start = now.strftime("%Y-%m-%d")
        
        end = datetime.datetime.strptime(start, '%Y-%m-%d') - datetime.timedelta(days=self.totalDays)
        end = end.strftime('%Y-%m-%d')
        
        try:
            cnx = mysql.connector.connect(user='cowrieRemote', password='asj2381!@38089f!@$#438ash',
                          host='165.227.97.111',
                          database='cowrie')
            windowName = '%s - %s' % (end, start)
            cowrieCMDinputs = pd.read_sql_query('SELECT * FROM input WHERE timestamp BETWEEN \'%s\' AND \'%s\'' % (end, start), con=cnx)

        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        else:
          cnx.close()
        
        return windowName, cowrieCMDinputs

            
    def word2VecPrepLDA(self, windowName, cowrieCMDinputs):
        cowrieCMDinputs = cowrieCMDinputs.groupby(['session'])['input'].apply(lambda x: ','.join(x)).reset_index()
        cowrieCMDinputs = cowrieCMDinputs.values.tolist()

        sessionTokens = []
        sessions = []
        for session, CMDs in cowrieCMDinputs:
            sessionTokens.append([cmd for cmd in CMDs.split(',')])
            sessions.append(session)
          
        model = gensim.models.Word2Vec(sessionTokens)
        modelName = "%s_CORPUS.pkl_model.bin" % windowName
        modelOutPath = self.LDAoutPath + modelName
        util.saveModel(model, modelOutPath)
        print modelOutPath
        return modelOutPath

    def filterCleanDataLDA(self, cowrieLog):
        
        # Copies just session and input columns
        cowrieLogFiltered = cowrieLog[['session','input']].copy()
        
        # Drops NAs
        cowrieLogFiltered = cowrieLogFiltered.dropna(subset=['input'], how='any')
            
        return cowrieLogFiltered

    def preProcessLDA(self, cowrieLogFiltered):
    
        # Groups the sessions together and seperates each command by a comma
        cowrieLogFiltered = cowrieLogFiltered.groupby(['session'])['input'].apply(lambda x: ','.join(x)).reset_index()
        splitColumn = lambda x: pd.Series([i for i in reversed(x.split(','))])
      
        cowrieLogFiltered = cowrieLogFiltered.set_index('session')['input'].apply(splitColumn).reset_index()
        cowrieLogFiltered = cowrieLogFiltered.set_index('session')
        
        cowrieLogFiltered = cowrieLogFiltered.T
        cowrieLogFiltered = cowrieLogFiltered.fillna(0, axis = 0, inplace = False)
        
        cowFilter = cowrieLogFiltered.to_dict('list')
        valList = 0
        cowFilter = {key:[elem for elem in value if elem != valList] for key,value in cowFilter.iteritems()}         
        print cowFilter
        return cowFilter






