import random
import copy
import Individual
import utils
import map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from Electre import *
import time

class Algo_genetic:
    def __init__(self, nbr_iter,n_pop,r_cross,r_mut,mapfile) -> None:
        self.m_iter_max = nbr_iter
        self.m_n_pop = n_pop
        self.m_r_cross = r_cross
        self.m_r_mut = r_mut
        self.m_scores = []
        self.m_pop = []
        self.m_mapfile = mapfile
        self.m_register_list = []
        self.m_initial_doc=self.m_mapfile.returnDic()

        #wheel selection
        self.m_total_score = 0
        self.m_prob = []
        self.m_cumulative_prob = []

        #elitism
        self.m_listElitism = []
    
    def add_elitism(self,elit_indiv):
        self.m_listElitism.append(elit_indiv)
    
    def build_matrix(self,instances):
        matrix = np.array([[p.return_totalComp(), p.return_totalProd(), p.return_minDistHabitation()] for p in instances])
        return matrix        

    def compute_selection_probs(rankings):
        n = len(rankings)
        weights = [n - i + 1 for i in range(1, n + 1)]
        total_weight = sum(weights)
        probs = [w / total_weight for w in weights]
        return probs
        
    def construct_wheel(self):
        index = 0
        for individual_prob in self.m_scores:
            p=(individual_prob/self.m_total_score)*1000
            self.m_prob.append(p)
            if index == 1:
                self.m_cumulative_prob.append(self.m_cumulative_prob[-1]+p)
            else:
                self.m_cumulative_prob.append(p)
            index=1
    
    def crossover(self,p1,p2,r_cross):

        return_list=[]
        if random.uniform(0, 1) < r_cross:

            parent_tupple1 = p1.return_clusterList()
            parent_tupple2 = p2.return_clusterList()
            parent_cluster1 = p1.return_cluserListGroup()
            parent_cluster2 = p2.return_cluserListGroup()

            #mapfile1 = copy.deepcopy(self.m_mapfile)
            #mapfile2 = copy.deepcopy(self.m_mapfile)
            m_initial_doc_init = copy.deepcopy(self.m_initial_doc)
            c1 = Individual.Individual_algo_genetic(self.m_mapfile)
            c2 = Individual.Individual_algo_genetic(self.m_mapfile)
            c1.initiate_Cost_Dic(m_initial_doc_init)
            c2.initiate_Cost_Dic(m_initial_doc_init)

            min_cluster = min(len(parent_cluster1), len(parent_cluster2))
            if min_cluster == 1:
                min_parcel = min(len(parent_tupple1),len(parent_tupple2))
                cut_gene_pt = random.randint(1, min_parcel-1)
                c1.changeParcel(p1,p2,cut_gene_pt,parent_tupple1[:cut_gene_pt],parent_tupple2[cut_gene_pt:])
                c2.changeParcel(p1,p2,cut_gene_pt,parent_tupple2[:cut_gene_pt],parent_tupple1[cut_gene_pt:])
            else:
                cut_gene_cluster = random.randint(1,min_cluster-1)
                c1.change_clusterParcel(p1,p2,parent_cluster1[:cut_gene_cluster],parent_cluster2[cut_gene_cluster:])
                c2.change_clusterParcel(p1,p2,parent_cluster2[:cut_gene_cluster],parent_cluster1[cut_gene_cluster:])

            return_list = [c1,c2]

            for child in return_list:
                cost = child.return_totalCost()
                if cost > 50:
                    del return_list[return_list.index(child)]
        return return_list

    def genetic_algorithm(self):


        self.m_pop = list()
        #Initial doc
        #peut être le crée pour les enfants à chaque fois ce serai pas mal
   
        begin = time.time()
        for i in range(self.m_n_pop):
            #mapfile = copy.deepcopy(self.m_mapfile)
            m_initial_doc_init = copy.deepcopy(self.m_initial_doc)
            indiv_map = Individual.Individual_algo_genetic(self.m_mapfile)
            indiv_map.chooseCandidate(m_initial_doc_init)
            self.m_pop.append(indiv_map)
        end = time.time()
        print(f"it takes {end-begin}")
        
        best, best_eval = self.m_pop[0], self.moyenne(self.m_pop[0])
        print(best_eval,"init")

        for gen in range(self.m_iter_max):
            print(f"=========== {gen} generation ===========")
            print(f"population: {self.m_n_pop}")

            for individual in self.m_pop:
                score = self.moyenne(individual)
                self.m_scores.append(score)
                self.m_total_score += score
                self.m_register_list.append(score)            
          
            self.construct_wheel()

            for i in range(self.m_n_pop):
                if self.m_scores[i] > best_eval:
                    best, best_eval = self.m_pop[i], self.m_scores[i]
                    print(">%d, new best = %.3f" % (gen, self.m_scores[i]))
                    print(f"valeur production = {best.return_totalProd()}, compacity = {best.return_totalComp()}, distance = {best.return_minDistHabitation()}")

            selected=[]
            for _ in range(self.m_n_pop):
                selected.append(self.selection_wheel())

            children = list()
            for i in range(0, self.m_n_pop-1, 2):
                p1, p2 = selected[i], selected[i+1]
                crossoverList = self.crossover(p1, p2, self.m_r_cross)

                for c in crossoverList:
                    if len(c.return_clusterList()) == 0:
                        continue
                    #self.mutation(c, self.m_r_mut)
                    children.append(c)
            
            self.m_pop = children
            self.m_scores = []
            self.m_cumulative_prob=[]
            self.m_n_pop = len(children)
            self.m_total_score=0

        fig, ax = plt.subplots()

        # Plot the data as a line graph
        ax.plot(self.m_register_list)

        # Show the plot
        plt.show()
        for i in self.m_pop:
            print(self.moyenne(i))
        return self.m_pop
 
    def next_generation(self,list_input):
        for elite in self.m_listElitism:
            list_input.append(elite)
            
    def moyenne_Electre(self):
        weights = np.array([5, -10, 1])
        concordance_thresholds = np.array([0.6, 0.6, 0.6,0.6])
        discordance_threshold = 0.3
        self.electre = Electre(self.build_matrix(self.m_pop),weights, concordance_thresholds, discordance_threshold)
        ranking = self.electre.get_ranked_indices()
        return ranking    

    def mutation(self,children, r_mut):
        # take the tupple of parcelle
        # check if a random number is less than r_mut (nearly 20%)
        # if yes then we flip the gene (but in our case we take the line and take another parcelle)
        if random.uniform(0, 1) < r_mut:
            #children.draw_matrix()
            children.shift_positions()
            #children.draw_matrix()


    def moyenne(self, indiv):
        moyenne = (-1*indiv.return_totalComp()-1*indiv.return_minDistHabitation()+2*indiv.return_totalProd())
        if moyenne < 0:
            moyenne=abs(moyenne)
        else:
            moyenne*=2
        return moyenne    
        
    def print_pop(self):
        for indiv in self.m_pop:
            print(f"Le score de l'individu {indiv.returnM_totalCost()+indiv.return_totalProd()}")
        return
 
    def selection_tournament(self, k=3):
        # select a parent from the population
        # first random selection
        selection_ix = random.randint(0,len(self.m_pop)-1)
        for ix in np.random.randint(0, len(self.m_pop)-1, k-1):
        # check if better (e.g. perform a tournament)
            if self.m_scores[ix] < self.m_scores[selection_ix]:
                selection_ix = ix
        return self.m_pop[selection_ix]

    def selection_wheel(self):
        r = random.uniform(0, self.m_cumulative_prob[-1])
        if r <= self.m_cumulative_prob[0]:
            return self.m_pop[0]
        else:
            for i in range(1,len(self.m_cumulative_prob)):
                if self.m_cumulative_prob[i-1] < r <= self.m_cumulative_prob[i]:
                    return self.m_pop[i]
              