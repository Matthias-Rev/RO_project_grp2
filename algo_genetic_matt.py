import random
from copy import copy

class Algo_genetic:
    def __init__(self, nbr_iter,n_pop,r_cross,r_mut) -> None:
        self.iter_max = nbr_iter
        self.m_n_pop = n_pop
        self.m_r_cross = r_cross
        self.m_r_mut = r_mut
        self.m_score = []
        self.m_pop = []
    
    def selection(self, k=3):
        # select a parent from the population
        # first random selection
        selection_ix = random.randint(len(self.pop))
        for ix in random.randint(0, len(self.pop), k-1):
        # check if better (e.g. perform a tournament)
            if self.scores[ix] < self.scores[selection_ix]:
                selection_ix = ix
        return self.pop[selection_ix]

    def crossover(self,p1, p2, r_cross):
        # here we copy the parent to create 2 children
        # r_cross is the crossover rate (normally equal to 80%)
         # children are copies of parents by default
        c1, c2 = p1.copy(), p2.copy()
        # check for recombination
        if random.rand() < r_cross:
        # select crossover point that is not on the end of the string
            pt = random.randint(1, len(p1)-2)
            # perform crossover
            c1 = p1[:pt] + p2[pt:]
            c2 = p2[:pt] + p1[pt:]
        return [c1, c2]
    
    def mutation(self,bitstring, r_mut):
        # take the tupple of parcelle
        # check if a random number is less than r_mut (nearly 20%)
        # if yes then we flip the gene (but in our case we take the line and take another parcelle)
        for i in range(len(bitstring)):
            # check for a mutation
            if random.rand() < r_mut:
                #flip tupple
                ok = 1
                
    
    def genetic_algorithm(self, n_iter, n_pop, r_cross, r_mut):

        pop = list()
        best, best_eval = 0, pop[0].score()

        for gen in range(n_iter):
            scores = [individual.score() for individual in pop]
            for i in range(n_pop):
                if scores[i] < best_eval:
                    best, best_eval = pop[i], scores[i]
                    print(">%d, new best f(%s) = %.3f" % (gen,  pop[i], scores[i]))

                selected = [self.selection(pop, scores) for _ in range(n_pop)]
                children = list()
                for i in range(0, n_pop, 2):
                    p1, p2 = selected[i], selected[i+1]
                
                    for c in self.crossover(p1, p2, r_cross):
                        self.mutation(c, r_mut)
                    
                    children.append(c)
                # replace population
            pop = children
        return [best, best_eval]    