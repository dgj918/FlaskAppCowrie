# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 19:22:30 2017

@author: dgj918
"""
from prettytable import PrettyTable
import numpy as np


def genDocRankings(W):
    
    doctRankings = []
    topics = W.shape[1]
    for topicIndex in range(topics):
        w = np.array(W[:, topicIndex])
        topIndicies = np.argsort(w)[::-1]
        doctRankings.append(topIndicies)
    return doctRankings


def termRankSize(termRankings):
    
    m = 0
    
    for ranking in termRankings:
        if m == 0:
            m = len(ranking)
        else:
            m = min(len(ranking), m)
            
    return m

def truncTermRankings(rankings, numRankings):
    if numRankings < 1:
        return rankings
    truncRank = []
    for rank in rankings:
        truncRank.append(rank[0:min(len(rank), numRankings)])
    return truncRank

def formatTermRanks(termRanks, numRankings, labels):
    header = ["Rank"]
    if labels is None:
        for i in range(len(termRanks)):
            header.append("Window%02d" % (i+1))
    else:
        for label in labels:
            header.append(label)
    tab = PrettyTable(header)
    tab.align["Rank"] = "r"
    for label in header[1:]:
        tab.align[label] = "l"
    for pos in range(numRankings):
        row = [str(pos+1)]
        for ranking in termRanks:
            if len(ranking) <= pos:
                row.append("")
            else:
                row.append(ranking[pos])
        tab.add_row(row)
    return tab

def formatTermRanksLong(termRanks, labels, numRankings):

    if labels is None:
        print "None"
        labels = []
        for i in range(len(termRanks)):
            labels.append("Window%02d" % (i+1))
    maxLabelLen = 0
    for label in labels:
        maxLabelLen = max(maxLabelLen, len(label))
    maxLabelLen += 1
    
    s = ""
    for i, label in enumerate(labels):
        s += label.ljust(maxLabelLen)
        s += ": "
        sterms = ""
        for term in termRanks[i][0:numRankings]:
            if len(sterms) > 0:
                sterms += ", "
            sterms += term
        s += sterms + "\n"
    return s
    
    