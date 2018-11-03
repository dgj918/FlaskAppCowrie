# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:41:26 2017

@author: dgj918
"""

import gensim


class modelSimilar():
    
    def __init__(self, model):
        self.model = model

        
    def similar(self, rankI, rankJ):
        
        sim = 0.0
        pairs = 0
        
        for termI in rankI:
            for termJ in rankJ:
                try:
                    sim += self.model.similarity(termI, termJ)
                    pairs += 1
                except:
                    pass 
        if pairs == 0:
            return 0.0

        return sim / pairs
    

class withinTopicMeasure:
    
    def __init__(self, metric):
        
        self.metric = metric

        
    def evaluateRanking(self, termRanking):
        return self.metric.similar(termRanking, termRanking)
    
    def evalRankings(self, termRankings):
        scores = []
        overall = 0.0
        for topicIndex in range(len(termRankings)):
            score = self.evaluateRanking(termRankings[topicIndex])
            scores.append(score)
            overall += score
        overall /= len(termRankings)

        return overall