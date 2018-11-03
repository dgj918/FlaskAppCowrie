# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:17:26 2017

@author: dgj918
"""

from matplotlib import pyplot

class plotData(object):
    
    def __init__(self, xlabel, ylabel):
        
        pyplot.ion()
        
        self.xlabel = xlabel
        self.ylabel = ylabel
        
        self.x = []
        self.y = []
        
        
    def updatePlot(self, xVal, yVal):
        
        x = self.x
        y = self.y
        
        x.append(xVal)
        y.append(yVal)
        
        pyplot.clf()
        
        pyplot.plot(x, y, 'k')
        
        
        pyplot.xlabel(self.xlabel)
        pyplot.ylabel(self.ylabel)
        
        pyplot.draw()


if __name__=='__main__':
    
    import time, math
    
    plt = plotData('x', 'y')
    
    for x in xrange(100):
        
        plt.updatePlot(x, x * math.sin(0.4 * x))
        time.sleep(.01)
        