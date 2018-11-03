# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:19:17 2017

@author: dgj918
"""
import logging as log
import numpy as np
from sklearn import decomposition
from sklearn.externals import joblib

class nonNegMatrix():
    
    def __init__(self, maxIterations, init_strategy, randomSeed):
        
        self.maxIterations = maxIterations
        self.init = init_strategy
        self.randomSeed = randomSeed
        self.W = None
        self.H = None
        
    def apply(self, matrix, k):
        self.W = None
        self.H = None
        model = decomposition.NMF(init=self.init, n_components = k, max_iter = self.maxIterations, random_state = self.randomSeed)
        self.W = model.fit_transform(matrix)
        self.H = model.components_


    def rankTerms(self, topicIndex, top):
        topIndicies = np.argsort(self.H[topicIndex, : ])[::-1]
        if top < 1 or top > len(topIndicies):
            return topIndicies
        return topIndicies[0:top]
    
    def generatePartition(self):
        if self.W is None:
            raise ValueError("No Results")
        return np.argmax(self.W, axis=1)
    

def generateDoctRank(W):
    
    doctRankings = []
    topics = W.shape[1]
    for topicIndex in range(topics):
        W = np.arra(W[:, topicIndex])
        topIndicies = np.argsort(W)[::-1]
        doctRankings.append(topIndicies)
    
    return doctRankings


        
        