import random
from Tetris import *
import numpy as np
import statistics 

POP_SIZE=20
numOfFactors = 6
initial_mean = [0 for i in range(numOfFactors)]
initial_variance= [100 for i in range(numOfFactors)]
initial_std=np.sqrt(initial_variance)
proportion = 0.25

weights = [-1,1,-1,-1,-4,-1] #placeholder weights

record_data = [] #mean, var, avg score of generations

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

score = main_menu_AI(win, weights)

print('score: ', score)

class Game:
    def __init__(self, weights=[], score=0):
        self.weights=weights
        self.score = score
    def play(self):
        #plays game and returns score 
        pass

class CrossEntropy:
    def __init__(self, popsize=POP_SIZE, mean=initial_mean, std=initial_std):
        self.popsize=popsize
        self.mean=mean
        self.std=std
        self.population = [Game for i in range(popsize)]
    
    def generate_samples(self, samplesize):
        weights_samples=np.random.normal(self.mean, self.std, size=(samplesize, 6)) #generates n vectors of size 6 (n games)
        return weights_samples
    
    def set_population(self):
        weight_samples = self.generate_samples(20)
        new_population=list[Game]
        
        for weights in weight_samples:
            new_population.append(Game(weights))
            
        self.population=new_population
            
        
    def evaluate(self):
        for game in self.population:
            game.play()
        
    def selection(self):
        #selects best based on fitness
        num=proportion*self.popsize
        sorted(self.population,key=lambda game: game.score, reverse=True)
        selected=[]
        for i in range(num):
            selected.append(self.population[i])
        return selected

    def update_dist(self, selected:list[Game]): 
        #changes mean and std dev based on best samples
        newmean=[0 for i in range(numOfFactors)]
        newstd=[0 for i in range(numOfFactors)]
        
        newmean=[((w1+w2+w3+w4+w5)/5) for w1,w2,w3,w4,w5 in zip(*[s.weights for s in selected])] 
        
        all_weights=[s.weights for s in selected]
        columns = list(zip(*all_weights))
        
        for i in range(6):
            newstd[i]=statistics.stdev(columns[i])
            
        self.mean=newmean
        self.std=newstd
        
    def main(self, generations):
        #initalise population
        self.set_population()
        
        for _ in generations:
            #evaluate each game in pop
            self.evaluate()
            
            #select best proportion
            selected=self.selection()
            
            #update distribution
            self.update_dist(selected)
            
            #create new population
            self.set_population()
        

number_of_generations=30 
       
ce = CrossEntropy()  
ce.main(number_of_generations) 
