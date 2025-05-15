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

# win = pygame.display.set_mode((s_width, s_height))
# pygame.display.set_caption('Tetris')

# score = main_menu_AI(win, weights)

# print('score: ', score)
BEST_SCORE=0
best_per_generation=[]

class Game:
    def __init__(self, weights=[], score=0):
        self.weights=weights
        self.score = score
    def play(self):
        #plays game and returns score 
        win = pygame.display.set_mode((s_width, s_height))
        pygame.display.set_caption('Tetris')

        self.score = main_menu_AI(win, self.weights)
        
        print('score: ', self.score)
        

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
        weight_samples = self.generate_samples(self.popsize)
        new_population=[Game for i in range(self.popsize)]
        
        for i in range(self.popsize):
            g1=Game(weight_samples[i])
            new_population[i]=g1
            
        self.population=new_population
            
        
    def evaluate(self):
        for game in self.population:
            game.play()
        
    def selection(self):
        #selects best based on fitness
        num=int(proportion*self.popsize)
        sortedlist=sorted(self.population,key=lambda game: game.score, reverse=True)
        selected=[]
        for i in range(num):
            selected.append(sortedlist[i])
        return selected

    def update_dist(self, selected:list[Game]): 
        #changes mean and std dev based on best samples
        newmean=[0 for i in range(numOfFactors)]
        newstd=[0 for i in range(numOfFactors)]
        
        all_weights=[s.weights for s in selected]
        columns = list(zip(*all_weights))
        # print(all_weights)
        # print(columns)
        
        for i in range(6):
            newstd[i]=statistics.stdev(columns[i])
            newmean[i] = statistics.mean(columns[i])
            
        self.mean=newmean
        self.std=newstd
        
    def main(self, generations):
        #initalise population
        self.set_population()
        
        for i in range(generations):
            print(f"\nGENERATION {i} \n")
            #evaluate each game in pop
            self.evaluate()
            
            #note best score in generation
            bestg=max(self.population, key=lambda game: game.score)
            best_per_generation.append((i+1,bestg))
            
            #select best proportion
            selected=self.selection()
            
            #update distribution
            self.update_dist(selected)
            
            #create new population
            self.set_population()
        

number_of_generations=10
       
ce = CrossEntropy()  
ce.main(number_of_generations) 

print(best_per_generation)
BEST_GAME=max(best_per_generation, key=lambda gen: gen[1].score)[1]
BEST_SCORE=BEST_GAME.score
BEST_WEIGHTS=BEST_GAME.weights
print(f"\nOVERALL BEST SCORE: {BEST_SCORE}")
print(f"\nOVERALL BEST WEIGHTS: {BEST_WEIGHTS}")
