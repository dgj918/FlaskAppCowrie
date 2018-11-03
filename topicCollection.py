"""
Created on Sat Nov 18 11:17:27 2017

@author: dgj918
"""
import os, os.path, sys, random, operator
import logging as log
import numpy as np
import nonNegativeMatrix, similarityMeasure
import pandas as pd
import util
import glob
import sklearn.preprocessing
from optparse import OptionParser
import similarityMeasure
import rank
import nonNegativeMatrix
import cPickle as pickle


class topicCollect:
    
    def __init__ (self, topTerms = 10, threshold = 1e-6):
        
        self.topTerms = topTerms
        self.threshold = threshold
        self.topicIDs = []
        self.allWeights = []
        self.allCMDs = set()

    
    def addTopicModel(self, H, terms, windowTopicLabels):
        
        topic = H.shape[0]
        for topicIndex in range(topic):
            topicWeights = {}
            if self.topTerms > 0:
                topIndicies = np.argsort(H[topicIndex, :] )[::-1]
                for termIndex in topIndicies [0:self.topTerms]:
                    topicWeights[terms[termIndex]] = H[topicIndex, termIndex]
                    self.allCMDs.add(terms[termIndex])
            else:
                
                totalWeight = 0.0
                for termIndex in range(len(terms)):
                    totalWeight += H[topicIndex, termIndex]
                for termIndex in range(len(terms)):
                    w = H[topicIndex, termIndex] / totalWeight
                    if w >= self.threshold:
                        topicWeights[terms[termIndex]] = H[topicIndex, termIndex]
                        self.allCMDs.add(terms[termIndex])
            self.allWeights.append(topicWeights)
            self.topicIDs.append(windowTopicLabels[topicIndex])
            
    def createMatrix(self):
        
        allCMDs = list(self.allCMDs)
        m = np.zeros((len(self.allWeights), len(allCMDs)))
        termColMap = {}
        
        for term in allCMDs:
            termColMap[term] = len(termColMap)
        row =0
        
        for topicWeights in self.allWeights:
            for term in topicWeights.keys():
                m[row, termColMap[term]] = topicWeights[term]
            row += 1
        
        normalizer = sklearn.preprocessing.Normalizer(norm = 'l2', copy = True)
        normalizer.fit(m)
        m = normalizer.transform(m)
        return(m, allCMDs)
    
class dtmCollect:
    
    def __init__(self, filePath, maxIterations, topicMinAct, topicMaxAct, numRankings, modelPath):
        
        self.filePath = filePath
        self.maxIterations = maxIterations
        self.topicMinAct = topicMinAct
        self.topicMaxAct = topicMaxAct
        self.numRankings = numRankings
        self.modelPath = modelPath

        
    def dtmCollection(self):
        self.randomSeed = random.randint(1,100000)
        np.random.seed(self.randomSeed)
        
        collection = topicCollect()
        implementation = nonNegativeMatrix.nonNegMatrix(maxIterations = self.maxIterations, init_strategy = 'nndsvd', randomSeed = self.randomSeed)
        coherenceScore = {}
        
        for files in glob.glob('%s*_DTM.pkl' % self.filePath):
            model = util.loadModel(self.modelPath)
            print "Loaded model from %s: " % self.modelPath
            validMeasure = similarityMeasure.withinTopicMeasure(similarityMeasure.modelSimilar(model))
            
            windowName = os.path.splitext(os.path.basename(files))[0]
            
            (docIDs, CMDs, termRankings, partition, W, H, windowTopicLabels) = util.loadDtmResults(files)
            collection.addTopicModel(H,CMDs, windowTopicLabels)
            matrix, allCMDs = collection.createMatrix()
            

            for topic in range(self.topicMinAct, self.topicMaxAct +1):
                implementation.apply(matrix, self.topicMaxAct)
                partition = implementation.generatePartition()
                topicLabels = []
                
                for i in range(topic):
                    topicLabels.append("%s_Window%02d" %(windowName, (i+1)))
                              
                termRankings = []
                
                for topicIndex in range(topic):

                    rankedTermsIndicies = implementation.rankTerms(topicIndex, self.numRankings)
                    termRanking = [allCMDs[i] for i in rankedTermsIndicies]
                    termRankings.append(termRanking)
                
                    truncatedTermRankings = rank.truncTermRankings(termRankings, self.numRankings)
                    coherenceScore[topic] = validMeasure.evalRankings(truncatedTermRankings)
                    print "Model coherence (Topic=%d) = %.4f" % (topic,coherenceScore[topic])
                    
                resultsOutPath = self.filePath + "%02d_dynamicTopic.pkl" % topic
                util.saveDtmResults(resultsOutPath, collection.topicIDs, allCMDs, termRankings, partition, implementation.W, implementation.H, topicLabels)
                
                #rank.formatTermRanks(termRankings, labels = None, numRankings = self.numRankings ) 
            
            if len(coherenceScore) > 0:
                sx = sorted(coherenceScore.items(), key=operator.itemgetter(1))
                sx.reverse()
                topTopic = [p[0] for p in sx] [0:min(3,len(sx))]
                print "Top recommendations for number of dynamic topics: %s" % ",".join(map(str, topTopic))
