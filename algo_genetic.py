import random
from copy import copy
import Individual
import utils
import map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class Algo_genetic:
    def __init__(self, nbr_iter,n_pop,r_cross,r_mut,matrix,mapfile, nbr_parcel) -> None:
        self.m_iter_max = nbr_iter
        self.m_n_pop = n_pop
        self.m_r_cross = r_cross
        self.m_r_mut = r_mut
        self.m_score = []
        self.m_pop = []
        self.m_matrix = matrix
        self.m_nbr_parcel = nbr_parcel
        self.m_mapfile = mapfile
    
    def selection(self, k=3):
        # select a parent from the population
        # first random selection
        selection_ix = random.randint(0,len(self.m_pop)-1)
        for ix in np.random.randint(0, len(self.m_pop)-1, k-1):
        # check if better (e.g. perform a tournament)
            if self.m_scores[ix] < self.m_scores[selection_ix]:
                selection_ix = ix
        return self.m_pop[selection_ix]

    def crossover(self,p1, p2, r_cross):
        # here we copy the parent to create 2 children
        # r_cross is the crossover rate (normally equal to 80%)
        # children are copies of parents by default
        parent_tupple1 = p1.chooseCandidate()
        parent_tupple2 = p2.chooseCandidate()

        c1 = Individual.Individual_algo_genetic(self.m_matrix,self.m_mapfile,parent_tupple1)
        c2 = Individual.Individual_algo_genetic(self.m_matrix,self.m_mapfile,parent_tupple2)
        # check for recombination
        if random.randint(0,1) < r_cross:
        # select crossover point that is not on the end of the string
            #print(len(c1.chooseCandidate()),"len du candidat")
            pt = random.randint(1, len(c1.chooseCandidate())-2)
            # perform crossover
            #c1.m_listParcel = parent_tupple1[:pt] + parent_tupple2[pt:]
            #c2.m_listParcel = parent_tupple2[:pt] + parent_tupple1[pt:]
            #print(parent_tupple1[:pt] + parent_tupple2[pt:],"new tupple")
            c1.changeParcel(parent_tupple1[:pt] + parent_tupple2[pt:])
            c1.changeParcel( parent_tupple2[:pt] + parent_tupple1[pt:])
        return [c1, c2]
    
    def mutation(self,children, r_mut):
        # take the tupple of parcelle
        # check if a random number is less than r_mut (nearly 20%)
        # if yes then we flip the gene (but in our case we take the line and take another parcelle)
        list_propriety = children.chooseCandidate()
        for i in range(len(list_propriety)):
            # check for a mutation
            if random.randint(0,1) < r_mut:
                #flip tupple
                list_propriety[i] = (random.randint(0,len(utils.matrix[1])),list_propriety[i][1])
                
    
    def genetic_algorithm(self):

        self.m_pop = list()

        for _ in range(self.m_n_pop):
            indiv_map = Individual.Individual_algo_genetic(self.m_matrix, self.m_mapfile)
            indiv_map.chooseCandidate()
            #print(indiv_map.chooseCandidate())
            self.m_pop.append(indiv_map)
        
        best, best_eval = 0, self.m_pop[0].returnM_totalCost()+self.m_pop[0].returnM_totalProd()

        for gen in range(self.m_iter_max):
            self.m_scores = [individual.m_totalCost+individual.m_totalProd for individual in self.m_pop]
            for i in range(self.m_n_pop):
                print(i)
                if self.m_scores[i] > best_eval:
                    best, best_eval = self.m_pop[i], self.m_scores[i]
                    print(">%d, new best = %.3f" % (gen, self.m_scores[i]))

                selected = [self.selection() for _ in range(self.m_n_pop)]
                children = list()
                for i in range(0, self.m_n_pop-1, 2):
                    p1, p2 = selected[i], selected[i+1]
                
                    for c in self.crossover(p1, p2, self.m_r_cross):
                        self.mutation(c, self.m_r_mut)
                    
                    children.append(c)
                # replace population
            self.m_pop = children
        best.draw_matrix()
        return [best, best_eval]