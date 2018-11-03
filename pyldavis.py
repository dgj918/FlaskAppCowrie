# -*- coding: utf-8 -*-
"""
Created on Wed Dec 06 22:42:51 2017

@author: dgj918
"""

import numpy as np
import pyLDAvis
import cPickle as pickle
import gensim

modelinPath1 = 'C:\Users\dgj918\C\Desktop\\flask\data\LDAvis\\2017-10-06 - 2017-11-05_CORPUS.pkl_model.bin'
(model) = pickle.load(file(modelinPath1, 'rb'))

freq = model.wv.vocab

modelinPath2 = 'C:\Users\dgj918\C\Desktop\\flask\data\LDAvis\\2017-11-06 - 2017-12-06_CORPUS.pkl_model.bin'
(model2) = pickle.load(file(modelinPath2, 'rb'))

pInPath1 = 'C:\Users\dgj918\C\Desktop\\flask\data\LDAvis\\2017-10-06 - 2017-11-05_CORPUS__DTM.pkl'
(sessions, CMDs, termRankings, partition, W, H, topicLabels) = pickle.load(file(pInPath1, 'rb'))

pInPath2 = 'C:\Users\dgj918\C\Desktop\\flask\data\LDAvis\\2017-11-06 - 2017-12-06_CORPUS__DTM.pkl'
(sessions2, CMDs2, termRankings2, partition2, W2, H2, topicLabels2) = pickle.load(file(pInPath2, 'rb'))
		

movies_vis_data = pyLDAvis.prepare(H, W, CMDs, freq,  )