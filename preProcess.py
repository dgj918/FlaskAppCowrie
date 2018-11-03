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
    
    def __init__(self, startDate, endDate, numWindows, outPath):
        
		date_format = "%Y-%m-%d"
		self.startDate = startDate
		self.endDate = endDate
		self.delta = self.endDate - self.startDate
		self.totalDays = self.delta.days
		self.numWindows = numWindows
		self.outPath = outPath
   
    def readWindow(self):
		windowSize = math.ceil(self.totalDays / self.numWindows)
		int(windowSize)
		start = self.startDate
		#start = start.strftime('%Y-%m-%d')
		end = self.startDate  + datetime.timedelta(days=windowSize)
		
		for window in range(self.numWindows):
			try:
				cnx = mysql.connector.connect(user='cowrieRemote', password='asj2381!@38089f!@$#438ash',
                              host='localhost',
                              database='cowrie')
				windowName = '%s - %s' % (start, end)
				cowrieCMDinputs = pd.read_sql_query('SELECT * FROM input WHERE timestamp BETWEEN \'%s\' AND \'%s\'' % (start, end), con=cnx)
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
			
			start = end 
			end = end + datetime.timedelta(days = windowSize)


		return modelPath

    def preProcessDTM(self, windowName, cowrieCMDinputs): 
        cowrieCMDinputs = cowrieCMDinputs.groupby(['session'])['input'].apply(lambda x: ','.join(x)).reset_index()
        sessions = list(cowrieCMDinputs['session'])
        cowrieCMDinputs = list(cowrieCMDinputs['input'])
        stopWordList = ['sh', 'sh ', 'enable', 'shell', 'system', 'enable ', ':', ': ', 'wget', 'wget ', 'tftp', 'tfpt ', 'uname -a']

        # integer encode the commands in each session into a sparse matrix
        intEncode = TfidfVectorizer(stop_words = stopWordList, max_features = 10000, tokenizer=lambda x: x.split(','))
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
        
        stopWordList = ['sh', 'sh ', 'enable', 'shell', 'system', 'enable ', ':', ': ', 'wget', 'wget ', 'tftp', 'tfpt ', 'uname -a']
        cmdTokens = [[cmd for cmd in cmds if cmd not in stopWordList] for cmds in sessionTokens]
        
        model = gensim.models.Word2Vec(cmdTokens)
        modelName = "%s_CORPUS.pkl_model.bin" % windowName
        modelOutPath = self.outPath + modelName
        util.saveModel(model, modelOutPath)

        return modelOutPath


   
class preProcessDataLDA:
    
    def __init__(self, startDate, endDate, LDAoutPath):
		self.startDate = startDate
		self.endDate = endDate
		self.LDAoutPath = LDAoutPath
   
    def readDB(self):

		start = self.startDate
		end = self.endDate
		
		try:
			cnx = mysql.connector.connect(user='cowrieRemote', password='asj2381!@38089f!@$#438ash', host='localhost', database='cowrie')
			windowName = '%s - %s' % (start, end)
			cowrieCMDinputs = pd.read_sql_query('SELECT * FROM input WHERE timestamp BETWEEN \'%s\' AND \'%s\'' % (start, end), con=cnx)

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
        stopWordList = ['sh', 'sh ', 'enable', 'shell', 'system', 'enable ', ':', ': ', 'wget', 'wget ', 'tftp', 'tfpt ', 'uname -a']

        for session, CMDs in cowrieCMDinputs:
            sessionTokens.append([cmd for cmd in CMDs.split(',')])
            sessions.append(session)
        
        cmdTokens = [[cmd for cmd in cmds if cmd not in stopWordList] for cmds in sessionTokens]  
        
        model = gensim.models.Word2Vec(cmdTokens)
        modelName = "%s_CORPUS.pkl_model.bin" % windowName
        modelOutPath = self.LDAoutPath + modelName
        util.saveModel(model, modelOutPath)
 
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
        stopWordList = ['sh', 'sh ', 'enable', 'shell', 'system', 'enable ', ':', ': ', 'wget', 'wget ', 'tftp', 'tfpt ', 'uname -a']
        cowFilter = {key:[elem for elem in value if elem not in stopWordList] for key,value in cowFilter.iteritems()} 
        

        return cowFilter






