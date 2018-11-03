# -*- coding: utf-8 -*-
"""
Created on Thu Nov 09 13:01:44 2017

@author: 212547746
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 07 09:21:09 2017

@author: 212547746
"""
from numpy import argsort, cumsum, log, ones, random, searchsorted, sum, zeros
import sys
from plotData import *


class LDA(object):
    
    def __init__(self, cowrieData, topics, iterations):
        
        self.cowrieData = cowrieData
        self.sessions = sessions = len(cowrieData)
        self.CMDs = CMDs = sum(len(cmd) for cmd in cowrieData)
        self.uniqueCMD = uniqueCMD = len(cowrieData.alphabet)
        
        self.topics = topics # user input
        self.iterations = iterations
        
        self.alpha = .5 * ones(topics)
        self.alphaSum = .5 * topics
        
        self.beta = 0.01 * ones(uniqueCMD)
        self.betaSum = 0.01 * uniqueCMD
        
        self.numWordsTopic = zeros((uniqueCMD, topics), dtype = int)
        self.numTopicDoc = zeros((topics, sessions), dtype = int)
        
        self.numTopics = zeros((topics), dtype = int)
        
        self.CMDsPerSess = CMDsPerSess = []
        
        for session in cowrieData:
            CMDsPerSess.append(zeros(len(session), dtype=int))
        
        
    def colGibSamp(self):
        
        alpha = self.alpha
        alphaSum = self.alphaSum
        
        beta = self.beta
        betaSum = self.betaSum
        
        numWordsTopic = self.numWordsTopic
        numTopicDoc = self.numTopicDoc
        
        numTopics = self.numTopics
        
        logProb = 0.0
        
        numWordsTopic.fill(0)
        numTopicDoc.fill(0)
        numTopics.fill(0)
        
        for doc, (docs, CMDsPerSess) in enumerate(zip(self.cowrieData, self.CMDsPerSess)):
            for C, (CMD, topic) in enumerate(zip(docs.cmds, CMDsPerSess)):
                logProb += log((numTopicDoc[topic, doc] + alpha[topic]) / (C + alphaSum) *
                               (numWordsTopic[CMD, topic] + beta[CMD]) / (numTopics[topic] + betaSum))
    
                numWordsTopic[CMD, topic] += 1
                numTopicDoc[topic, doc] += 1
                numTopics[topic] += 1
        print logProb
        return logProb
            
    
    def inf(self):
        
        self.topicSample(init = True)
        
        cg = self.colGibSamp()
        
        plt = plotData('Iteration', 'Log Probability')
        plt.updatePlot(0,cg)

        print '\nIteration %s: %s' % (0,cg)
        self.printResults()

        for s in xrange (1, self.iterations+1):
            
            sys.stdout.write('.')
            
            if s % 10 == 0:
                
                cg = self.colGibSamp()
                print "cg ", cg
                plt.updatePlot(s,cg)
                
                print '\nIteration %s: %s' % (0,cg)
                self.printResults()
                
            self.topicSample()
            
    def topicSample(self, init=True):
        
        alpha = self.alpha
        
        beta = self.beta
        betaSum = self.betaSum
        
        numWordsTopic = self.numWordsTopic
 
        numTopicDoc = self.numTopicDoc

        numTopics = self.numTopics

        
        for doc, (docs, CMDsPerS) in enumerate(zip(self.cowrieData, self.CMDsPerSess)):
            for C, (CMD, topic) in enumerate(zip(docs.cmds, CMDsPerS)):
                if not init:  
                    numWordsTopic[CMD, topic] -= 1
                    
                    numTopics[topic] -= 1
                    
                    numTopicDoc[topic, doc] -= 1
                    
                distribution = (numWordsTopic[CMD, :] + beta[CMD]) / (numTopics + betaSum) * (numTopicDoc[:, doc] + alpha)

                sumDist = cumsum(distribution)
              
                rand = random.random() * sumDist[-1]
               
                topic = searchsorted(sumDist, rand)
                
                
                numWordsTopic[CMD, topic] += 1
 
                numTopicDoc[topic, doc] += 1

                numTopics[topic] += 1

                
                CMDsPerS[C] = topic

                
    def printResults(self, numTopics = 5, numCommands = 10):
        
        beta = self.beta
        numWordsTopic = self.numWordsTopic
        alphabet = self.cowrieData.alphabet
        #[:numCommands]
                      
        for t in xrange(self.topics):
            sortedTypes = map(alphabet.lookup, argsort(numWordsTopic[:, t] + beta))
            print "##########################\nTopic %s: \n\n %s\n" % (t+1, '\n '.join(sortedTypes[-numTopics:][::-1]))
        
        for topic in self.numWordsTopic:
            a = numWordsTopic[:,topic]
            print "a ", a

    
    
