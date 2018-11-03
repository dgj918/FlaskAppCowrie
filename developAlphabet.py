# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:44:50 2017

@author: dgj918
"""
import numpy as np

class Alphabet(object):
    
    def __init__(self):
        self.mappings = {}
        self.reverseMappings = {}
        
        self.index = 0
        self.grow = True
        
    def stopGrowth(self):
        self.grow = False
        
    def lookup(self, i):
        
        assert isinstance(i, np.integer)
        return self.reverseMappings[i]
    
    def plainText(self):
        
        contents = self.reverseMappings.items()
        contents.sort(key=lambda x: x[0])
    
        return '\n'.join('%s\t%s' % (i,s) for i,s in contents)
    
    def __contains__(self, s):
        
        assert isinstance (s, basestring)
        return s in self.mappings
    
    def __getitem__(self,s):
        
        try: 
            return self.mappings[s]
            
        
        except KeyError:
            if not isinstance (s, basestring):
                raise ValueError('Invalid key')
            
            if not self.grow:
                return None
            
            i = self.mappings[s] = self.index
            self.reverseMappings[i] = s
            self.index += 1
            return i
    
    add = __getitem__
    
    def __iter__(self):
        
        for i in xrange(len(self)):
            yield self.reverseMappings[i]
            
    def __len__(self):
        
        return len(self.mappings)
    