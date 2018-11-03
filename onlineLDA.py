# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:40:58 2017

@author: dgj918
"""

import numpy as np

class onlineLDA(objec):
    
    def __init__(self, cowrieData, topics, docs, alpha, eta, tau, kappa, iterations):
        
        self.cowrieData = cowrieData
        self.topics = topics
        self.docs = docs
        self.alpha = alpha
        self.eta = eta
        self.tau = tau
        self.kappa = kappa
        self.updateCount = 0
        self.iterations = iterations
        
        self.uniqueCMD = uniqueCMD = len(cowrieData.alphabet)
        
        self.lam = 1 * np.random.gamma(100., 1. / 100., (self.topics, uniqueCMD))
        self.eLogBeta = dir_exp(self.lam)
        self.expElogBeta = np.exp(self.eLogBeta)
        
    def eStep(self, cowrieData, iterations):
        meanChangeThresh = .00001
        
        batchData = len(cowrieData.alphabet)
        
        self.lam = 1 * np.random.gamma(100., 1. / 100., (self.topics, uniqueCMD))
        self.eLogBeta = dir_exp(self.lam)
        self.expElogBeta = np.exp(self.eLogBeta)
        
        sufStat = np.zeros(self.lam.shape)
        
        iterations = self.iterations
        meanChange = 0
        
        for doct in range(0, batchData):
            
            print sum(wordCount[doct])
            
            index = wordIndex[doct]
            counts = wordCounts[doct]
            
            gammaofDoct = gamma[doct, :]
            eLogTheta = gamma[doct, :]
            expElogTheta = gamma[doct, :]
            
            phiNorm = np.dot(doctExpElogTheta, doctExpElogTheta) + 1 e^-100
            
            while iterations > 0:
                priorGamma = gamma
                
                doctGamma = self.alpha + doctExpElogTheta * np.dot(counts / phiNorm, doctExpElogTheta.T)
                
                print doctGamma[:, np.newaxis]
                
                doctElogTheta = dir_exp(doctGamma)
                doctExpLogTheta = np.exp(doctElogTheta)
                
                meanChange = np.mean(abs(doctGamma - priorGamma))
                
                if (meanChange < meanChangeThresh):
                    break
                
            gamma[d, :] = doctGamma
            
        sufStat = sufStat * self.expElogBeta
        
        return [(gamma, suffStat)]
    
    def updateLam(self, cowrieData):
        
        rhot = pow(self.tau + self.updateCount - self.kappa)
        self.rhot = rhot
        
        (gamma, sufStat) = self.eStep(wordIDs, wordCounts)
        
        bound = self.approxBound(wordIDs, wordCounts, gamma)
        
        self.lam = self.lam * (1 - rhot) + rhot * (self.eta + self.D * sufStat / len(wordIDs))
        
        self.eLogBeta = dir_exp(self.lam)
        self.expElogBeta = np.exp(self.eLogBeta)
        self.updateCount += 1
        
        return(gamma, bound)
    
    def approxBound(self, wordIDs, wordCounts, gamma):
        
        batch = len(wordIDs)
        
        score = 0
        
        eLogTheta = dir_exp(gamma)
        
        expElogTheta = np.exp(eLogTheta)
        
        for doct range(0, batch):
            doctGamma = gamma[doct, :]
            index = wordIndex[doct]
            counts = np.array(cmdCounts[doct])
            phiNorm = np.zeros(len(index))
            for i in range(0, len(index)):
                temp = eLogTheta[doct, :] + self.eLogBeta[:,index[i]]
                tempMax = max(temp)
                phiNorm[i] = np.log(sum(np.exp(temp - tempMax))) + tempMax
            
            score += np.sum(counts * phiNorm)
        
        score += np.sum(self.alpha - gamma) * eLogTheta)
        score += np.sum(gamma ln(gamma) - gamma ln(self.alpha))
        score += np.sum(gamma ln(self.alpha * self.topics) - gamma ln(np.sum(gamma,1)))
        
        score = score + np.sum((self.eta - self.lam) * self.eLogBeta)
        score = score + np.sum(gamma ln(self.lam) - gamma ln(self.eta)
        score = score + np.sum(gamma ln(self.eta * self.W)) - gamma ln(np.sum(self.lam, 1))
        
        return (score)
    

def dir_exp(alpha):
    
    if len(alpha.shape) == 1:
        return (psi(alpha) - psi(np.sum(alpha)))
    return (psi(alpha) - psi(np.sum(alpha,1)) [:, np.newaxis])
            
        