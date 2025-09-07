import random
from Tetris import *
import numpy as np
import math
import csv
import statistics

POP_SIZE = 20
numOfFactors = 6
initial_mean = [0 for i in range(numOfFactors)]
initial_variance = [100 for i in range(numOfFactors)]
initial_std = [math.sqrt(var) for var in initial_variance]
proportion = 0.3
min_std = 0.5

weights = [-1, 1, -1, -1, -4, -1]  # placeholder weights

record_data = []  # mean, var, avg score of generations

# win = pygame.display.set_mode((s_width, s_height))
# pygame.display.set_caption('Tetris')

# score = main_menu_AI(win, weights)

# print('score: ', score)
BEST_SCORE = 0
best_per_generation = []


class Game:
    def __init__(self, weights=[], score=0):
        self.weights = weights
        self.score = score

    def play(self, shape_pattern):
        # plays game and returns score
        win = pygame.display.set_mode((s_width, s_height))
        pygame.display.set_caption('Tetris')

        self.score += main_menu_AI(win, self.weights, shape_pattern)


class CrossEntropy:
    def __init__(self, popsize=POP_SIZE, mean=initial_mean, std=initial_std, var=initial_variance):
        self.popsize = popsize
        self.mean = mean
        self.std = std
        self.variance = var
        self.population = []

    def generate_samples(self, samplesize):
        weights_samples = np.random.normal(self.mean, self.std, size=(samplesize, 6))  # generates n vectors of size 6 (n games)
        return weights_samples

    def set_population(self, elites=[]):
        weight_samples = self.generate_samples(self.popsize-len(elites))
        new_population = []

        for elite in elites:
            elite.score = 0
            new_population.append(elite)

        for i in range(self.popsize - len(elites)):
            g1 = Game(weight_samples[i])
            new_population.append(g1)
        self.population = new_population

    def evaluate(self, shape_pattern):
        for game in self.population:
            game.play(shape_pattern)

    def selection(self):
        #selects best based on fitness
        num=int(proportion*self.popsize)
        sortedlist=sorted(self.population,key=lambda game: game.score, reverse=True)
        selected=[]
        for i in range(num):
            selected.append(sortedlist[i])
        return selected

    def update_dist(self, selected: list[Game], gen):
        # changes mean and std dev based on best samples
        newmean = [0 for i in range(numOfFactors)]
        newstd = [0 for i in range(numOfFactors)]
        newvar = [0 for i in range(numOfFactors)]

        all_weights = [s.weights for s in selected]
        columns = list(zip(*all_weights))
        # print(all_weights)
        # print(columns)

        for i in range(6):
            newstd[i] = max(min_std, statistics.stdev(columns[i]))
            newmean[i] = statistics.mean(columns[i])
            newvar[i] = statistics.variance(columns[i])

        self.variance = newvar
        self.mean = newmean
        self.std = newstd
        self.constant_noise()


    def constant_noise(self):
        noise = 0.1
        self.variance = [var + noise for var in self.variance]
        self.std = [math.sqrt(var) for var in self.variance]

    def linear_dec_noise(self, gen):
        noise = max(0, 5 - (gen / 10))
        self.variance = [var + noise for var in self.variance]
        self.std = [math.sqrt(var) for var in self.variance]

    def record_population(self, generation, filename="population.csv"):
        with open(filename, mode="a") as file:
            writer = csv.writer(file)
            writer.writerow([f"GENERATION {generation + 1}"])
            for individual in self.population:
                row = list(individual.weights) + [individual.score]
                writer.writerow(row)
            writer.writerow([])

    def record_population_next(self, filename="population_next.csv"):
        with open(filename, mode="w", newline='') as file:
            writer = csv.writer(file)
            for individual in self.population:
                row = list(individual.weights) + [individual.score]
                writer.writerow(row)

    def load_population(self, filename="population_next.csv"):
        with open(filename, mode="r") as file:
            reader = csv.reader(file)
            i = 1
            for row in reader:
                if i > POP_SIZE:
                    break
                weights = list(map(float, row[:6]))
                score = float(row[6])
                i = i+1
                self.population.append(Game(weights=weights, score=score))

    def generate_pattern(self):
        pattern = [random.randint(0, 10) for _ in range(1000)]
        return pattern

    def avg_evaluate(self, shape_pattern_set):
        for pattern in shape_pattern_set:
            self.evaluate(pattern)
        #average scores
        for game in self.population:
            game.score = game.score/len(shape_pattern_set)
            print(game.score)

    def generate_n_patterns(self, n):
        shape_pattern_set = []
        for _ in range(n):
            shape_pattern_set.append(self.generate_pattern())
        return shape_pattern_set


    def main(self, generations):
        # initalise population
        self.load_population()

        for i in range(generations):
            print(f"\nGENERATION {i + 1} \n")

            shape_pattern_set = self.generate_n_patterns(5)
            self.avg_evaluate(shape_pattern_set)

            # note best score in generation
            bestg = max(self.population, key=lambda game: game.score)
            best_per_generation.append((i + 1, bestg))

            # select best proportion p
            selected = self.selection()
            elites = selected[:2]

            # update distribution
            self.update_dist(selected, i+1)

            # record data
            self.record_population(i)

            # create new population
            self.set_population(elites)

        shape_pattern_set = self.generate_n_patterns(5)
        self.avg_evaluate(shape_pattern_set)
        self.record_population_next()

number_of_generations = 10

ce = CrossEntropy()
ce.main(number_of_generations)

print(best_per_generation)
BEST_GAME = max(best_per_generation, key=lambda gen: gen[1].score)[1]
BEST_SCORE = BEST_GAME.score
BEST_WEIGHTS = BEST_GAME.weights
print(f"\nOVERALL BEST SCORE: {BEST_SCORE}")
print(f"\nOVERALL BEST WEIGHTS: {BEST_WEIGHTS}")
