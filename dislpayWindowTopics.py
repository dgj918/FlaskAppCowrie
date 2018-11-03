# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 20:47:23 2017

@author: dgj918
"""
import util
import glob
import rank

class displayTopics:
    
    def __init__(self, columnSize, filePath, top):
        
        self.columnSize = columnSize
        self.filePath = filePath
        self.top = top   
        
    def printTopics(self):
        
        for files in glob.glob('%s*_DTM.pkl' % self.filePath):
            (sessions, CMDs, termRank, partition, W, H, labels) = util.loadDtmResults( files )
            print "Loaded model with %d topics from %s" % (len(termRank), files)
            print "Top %d commands for %d topics: " % (self.top, len(termRank))
            
            m = rank.termRankSize(termRank)
            
            rank.formatTermRanksLong(termRank, labels, min(self.top, m))
            
            current = 0
            while current < len(termRank):
                currentEnd = min(current + self.ColumnSize, len(termRank))
                currentRank = termRank[current:currentEnd]
                currentLabels = labels[current:currentEnd]
                rank.formatTermRank(currentRank, currentLabels, min(self.top, m))
                current += self.columnSize
                