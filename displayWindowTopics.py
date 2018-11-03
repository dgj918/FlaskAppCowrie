# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 20:47:23 2017

@author: dgj918
"""
import util
import glob
import rank
import prettytable

class displayTopics:
    
	def __init__(self, columnSize, filePath, top):
        
		self.columnSize = columnSize
		self.filePath = filePath
		self.top = top   
        
	def printTopics(self):
		tables = []
		for files in glob.glob('%s*_DTM.pkl' % self.filePath):
			(sessions, CMDs, termRankings, partition, W, H, labels) = util.loadDtmResults( files )
			print "-------------------------------------------------"
			print "Loaded model with %d topics from %s" % (len(termRankings), files)
			print "Top %d commands for %d topics: " % (self.top, len(termRankings))
            
			m = rank.termRankSize(termRankings)
			rank.formatTermRanksLong(termRankings, labels, min(self.top, m))
            
			current = 0
			while current < len(termRankings):
				currentEnd = min(current + self.columnSize, len(termRankings))
				currentRank = termRankings[current:currentEnd]
				currentLabels = labels[current:currentEnd]
				tab = rank.formatTermRanks(currentRank, min(self.top, m), currentLabels)
				current += self.columnSize
				#tab = tab.print_html()
				print tab
				tab = tab.get_html_string()
				tables.append(tab)
		return tables
