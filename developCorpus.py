# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 13:38:42 2017

@author: dgj918
"""
import numpy as np
import developAlphabet 

class Document(object):
    
    def __init__(self, corpus, session, cmds):
        
        assert isinstance(corpus, Corpus)
        assert isinstance (session, basestring)
        assert isinstance (cmds, np.ndarray)
        
        self.corpus = corpus
        self.session = session
        self.cmds = cmds
        
    def __len__(self):
        return len(self.cmds)
    
    def plaintext(self):
        return ' '.join([self.corpus.alphabet.lookup(x) for x in self.cmds])
    
class Corpus(object):
    
    def __init__(self):
        
        self.documents = []
        self.alphabet = developAlphabet.Alphabet()
        
    def addDocument(self, name, data):
        
        assert isinstance(name, basestring)
        assert isinstance(data, list)
        
     
        cmds = np.array([self.alphabet[x] for x in data])
        self.documents.append(Document(self, name, cmds))

    
    def __iter__(self):
        return iter(self.documents)
    
    def __len__(self):
        return len(self.documents)

                   


