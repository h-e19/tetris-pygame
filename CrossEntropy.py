import random
import numpy as np

POP_SIZE=10
numOfFactors = 6
initial_mean = [0 for i in range(numOfFactors)]
initial_variance= [100 for i in range(numOfFactors)]

record_data = [] #mean, var, avg score of generations

class game:
    def __init__(self, weights=[], score=0):
        self.weights=weights
        self.score = score
        
    def get_weights(self):
        return self.weights
    
    def set_weights(self,w):
        self.weights = w
        
    def get_score(self):
        return self.score
    
    def set_score(self,s):
        self.score=s
        
    def play(self):
        #plays game and returns score 
        pass

class CrossEntropy:
    def __init__(self, popsize, mean=initial_mean, variance=initial_variance):
        self.popsize=popsize
        self.mean=mean
        self.variance=variance
        self.stds=np.sqrt(variance)
        self.population = [game for i in range(popsize)]
    
    def generate_samples(self, samplesize):
        weights_samples=np.random.normal(self.mean, self.stds, size=(samplesize, 6)) #generates n vectors of size 6 (n games)
        return weights_samples
        
    def evaluate(self, samples):
        #returns fitness using game.play
        pass
        
    def selection(self):
        #selects best based on fitness
        pass

    def update_dist(self): 
        #changes mean and std dev based on best samples
    
        
