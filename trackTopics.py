# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 22:47:08 2017

@author: dgj918
"""

import util 
import rank
import glob
import os, os.path
from prettytable import PrettyTable


class trackTop:
    
	def __init__(self, dynamicInPath, windInPath, top):

		self.windPath = windInPath
		self.dyResults = util.loadDtmResults(dynamicInPath)
		self.assignedWindowMap = {}
		self.top = top
        
        
	def dyTopicWindows(self):
		self.dyTopics = len(self.dyResults[2]) 
		self.dyTermRankings = rank.truncTermRankings(self.dyResults[2], self.top)        
		self.dyPartition = self.dyResults[3]



		for index, windowTopicLabel in enumerate(self.dyResults[0]):
			self.assignedWindowMap[windowTopicLabel] = self.dyPartition[index]

		allTrackedTopics = []

		for i in range(self.dyTopics):
			allTrackedTopics.append([])

		windowNum = 0

		for files in glob.glob('%s*_DTM.pkl' % self.windPath):

			windowNum += 1
			print "Reading window topics for window %d from %s ..." % ( windowNum, files )
			windowResults = util.loadDtmResults(files)
			windowTopics = len(windowResults[2])
			print "windTopics", windowTopics
			windowTermRankings = rank.truncTermRankings(windowResults[2], self.top)
			print "Loaded model with %d window topics from %s" % (windowTopics, files)

			for index, windowTopicLabel in enumerate(windowResults[6]):
				dyTopicIndex = self.assignedWindowMap[windowTopicLabel]
				ranking = windowTermRankings[index]
				allTrackedTopics[dyTopicIndex].append((windowNum,ranking)) #windowNum
			tables = []
			for i in range(self.dyTopics):
				dyTopicLabel = self.dyResults[6][i]
				print "Dynmaic Topic: %s " % dyTopicLabel
				header = ["Rank", "Overall"]
				
				for t in allTrackedTopics[i]:
					field = "Window %d" % t[0]
					suffix = 1
					while field in header:
						suffix += 1
						field = "Window %d(%d)" % (t[0], suffix)
					header.append(field)
				tab = PrettyTable(header)
				tab.align["Rank"] = "r"
				
				for label in header[1:]:
					tab.align[label] = "l"
					
				
				for pos in range(self.top):
					row = [str(pos+1)]
					row.append(self.dyTermRankings[i][pos])
					
					for t in allTrackedTopics[i]:
						if len(t[1]) <= pos:
							row.append("")
						else:
							row.append(t[1][pos])
					tab.add_row(row)
				print tab
				tab = tab.get_html_string()
				tables.append(tab)
			return tables