import random
from copy import copy
import Individual
import utils
import map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

class Algo_genetic:
    def __init__(self, nbr_iter,n_pop,r_cross,r_mut,mapfile) -> None:
        self.m_iter_max = nbr_iter
        self.m_n_pop = n_pop
        self.m_r_cross = r_cross
        self.m_r_mut = r_mut
        self.m_score = []
        self.m_pop = []
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
        parent_tupple1 = p1.returnList_Parcel()
        parent_tupple2 = p2.returnList_Parcel()
        # check for recombination
        if random.uniform(0, 1) < r_cross:
            c1 = Individual.Individual_algo_genetic(self.m_mapfile,parent_tupple1)
            c2 = Individual.Individual_algo_genetic(self.m_mapfile,parent_tupple2)
        # select crossover point that is not on the end of the string
            #print(len(c1.returnList_Parcel()),"len du candidat")
            cut_gene_pt = random.randint(1, len(c1.returnList_Parcel())-1)
            # perform crossover
            #c1.m_listParcel = parent_tupple1[:pt] + parent_tupple2[pt:]
            #c2.m_listParcel = parent_tupple2[:pt] + parent_tupple1[pt:]

            #print(parent_tupple1[:pt] + parent_tupple2[pt:],"new tupple c1")
            #print(parent_tupple2[:pt] + parent_tupple1[pt:],"new tupple c2")
            c1.changeParcel(parent_tupple1[:cut_gene_pt] + parent_tupple2[cut_gene_pt:])
            c2.changeParcel( parent_tupple2[:cut_gene_pt] + parent_tupple1[cut_gene_pt:])
            return [c1, c2]
        return []
    
    def mutation(self,children, r_mut):
        # take the tupple of parcelle
        # check if a random number is less than r_mut (nearly 20%)
        # if yes then we flip the gene (but in our case we take the line and take another parcelle)
        list_propriety = children.returnList_Parcel()
        for i in range(len(list_propriety)):
            # check for a mutation
            if random.uniform(0, 1) < r_mut:
                #flip tupple
                #list_propriety[i] = (random.randint(0,len(utils.matrix[1])),list_propriety[i][1])
                # print(self.m_mapfile.returnGrid()[31][159])
                # print(len(self.m_mapfile.returnGrid()[1]),"length")
                # print(random.randint(0,len(self.m_mapfile.returnGrid()[1])),"random number for x")
                # print(list_propriety[i].returnPosition()[1],"return Position")
                #print()
                #self.m_mapfile.returnGrid()[list_propriety[i].returnPosition()[0]][len(self.m_mapfile.returnGrid()[1])]
                list_propriety[i] = self.m_mapfile.returnGrid()[list_propriety[i].returnPosition()[1]][random.randint(0,len(self.m_mapfile.returnGrid())-1)]
                
    
    def genetic_algorithm(self):


        self.m_pop = list()

        for i in range(self.m_n_pop):
            print("Candidate",i)
            indiv_map = Individual.Individual_algo_genetic(self.m_mapfile)
            indiv_map.chooseCandidate()
            #print(indiv_map.returnList_Parcel(),"candidate début")
            self.m_pop.append(indiv_map)
        
        best, best_eval = self.m_pop[0], self.m_pop[0].returnM_totalCost()+self.m_pop[0].returnM_totalProd()
        print(best,"init")

        for gen in range(self.m_iter_max):
            self.m_scores = [individual.m_totalCost+individual.m_totalProd for individual in self.m_pop]
            for i in range(self.m_n_pop):
                #print(f"{i} individu {self.m_scores[i]} score")
                if self.m_scores[i] > best_eval:
                    best, best_eval = self.m_pop[i], self.m_scores[i]
                    print(">%d, new best = %.3f" % (gen, self.m_scores[i]))

                selected = [self.selection() for _ in range(self.m_n_pop)]

            children = list()
            for i in range(0, self.m_n_pop-1, 2):
                p1, p2 = selected[i], selected[i+1]
                #print(p1,p2)
            
                for c in self.crossover(p1, p2, self.m_r_cross):
                    self.mutation(c, self.m_r_mut)
                    children.append(c)
            # replace population
            self.m_pop = children
            self.m_scores = []
            self.m_n_pop = len(children)
            #print(len(best.returnList_Parcel()))
            #print(best,"end")
            #best.draw_matrix()
        return self.m_pop