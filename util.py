# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 21:00:48 2017

@author: dgj918
"""

import logging as log
import cPickle as pickle


def saveCorpusData(windowName, outPath, doctTermMatrix, CMDs, sessions):    
    
    doctTermMatrixOutPath = "%s%s_CORPUS.pkl" % (outPath, windowName)
    
    pickle.dump((doctTermMatrix, CMDs, sessions), file(doctTermMatrixOutPath, 'wb'))
    

def loadCorpusData(inPath):
    
    (doctTermMatrix, CMDs, sessions) = pickle.load(file(inPath, 'r'))
    
    return (doctTermMatrix, CMDs, sessions)


def saveDtmResults(outPath, sessions, CMDs, termRankings, partition, W, H, topicLabels = None):
    if topicLabels is None:
        topicLables = []
        for i in range(len(termRankings)):
            topicLables.append("Topic %s" % (i+1))
    pickle.dump((sessions, CMDs, termRankings, partition, W, H, topicLabels), file(outPath, 'wb'))
        
        
def loadDtmResults(inPath):
    
    (sessions, CMDs, termRankings, partition, W, H, topicLabels) = pickle.load(file(inPath, 'rb'))
    return (sessions, CMDs, termRankings, partition, W, H, topicLabels)

def saveModel(model, outPath):
    pickle.dump((model), file(outPath, 'wb'))
        
        
def loadModel(inPath):
    (model) = pickle.load(file(inPath, 'rb'))
    return (model)