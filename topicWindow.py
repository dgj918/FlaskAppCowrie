# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 10:32:52 2017

@author: dgj918
"""
import os, os.path, operator
import logging as log
import glob
import gensim

import nonNegativeMatrix, similarityMeasure, rank, util 



class topicWind():
    
    def __init__(self, topicMin, topicMax, maxIterations, filePath, labels, numRankings):
        
        self.topicMin = topicMin
        self.topicMax = topicMax
        self.maxIterations = maxIterations
        self.filePath = filePath
        self.labels = labels
        self.numRankings = numRankings
          
    def doctTermMatrix(self):      
        implementation = nonNegativeMatrix.nonNegMatrix(self.maxIterations, 'random', 0)
        selectedTopics = []

        for files in glob.glob('%s*_CORPUS.pkl' % self.filePath):
            encode2Int = files + '_model.bin'
            model = util.loadModel(encode2Int)
            #print "Loaded model from %s: " % encode2Int
            validMeasure = similarityMeasure.withinTopicMeasure(similarityMeasure.modelSimilar(model))
            windowName = os.path.splitext(os.path.basename(files))[0]
            (matrix, CMDs, sessions) = util.loadCorpusData(files)
            
            numSessions = len(sessions)
            topicMinAct = min(numSessions, self.topicMin)
            topicMaxAct = min(numSessions, self.topicMax)
            
            coherenceScore = {}
                
            for topic in range(topicMinAct, topicMaxAct +1):
                
                implementation.apply(matrix, self.topicMax)
                partition = implementation.generatePartition()
                topicLabels = []
                for i in range(topic):
                    
                    topicLabels.append("%s_Topic%02d" %(windowName, (i+1)))
                
                termRankings = []
                for topicIndex in range(topic):
                    
                    rankedTermIndicies = implementation.rankTerms(topicIndex, self.numRankings)
                    termRank = [CMDs[i] for i in rankedTermIndicies]
                    termRankings.append(termRank)
                    
                truncatedTermRankings = rank.truncTermRankings(termRankings, self.numRankings)
                coherenceScore[topic] = validMeasure.evalRankings(truncatedTermRankings)
                print "Model coherence (Topic=%d) = %.4f" % (topic,coherenceScore[topic])

                dirOut = self.filePath + "%s_" % (windowName)
                resultsOutPath = "%s_DTM.pkl" % dirOut
                print "saved to:", resultsOutPath
                util.saveDtmResults(resultsOutPath, sessions, CMDs, termRankings, partition, implementation.W, implementation.H, topicLabels)
            
            
            
            if len(coherenceScore) > 0:
                sx = sorted(coherenceScore.items(), key = operator.itemgetter(1))
                sx.reverse()
                topTopics =[p[0] for p in sx] [0:min(3, len(sx))]
                selectedTopics.append([files, topTopics[0]])
                print "Top recommendations for number of dynamic topics: %s" % ",".join(map(str, topTopics) )
