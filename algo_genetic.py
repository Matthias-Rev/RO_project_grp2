import random
from copy import copy
import Individual
import utils
import map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from Electre import *

class Algo_genetic:
    def __init__(self, nbr_iter,n_pop,r_cross,r_mut,mapfile) -> None:
        self.m_iter_max = nbr_iter
        self.m_n_pop = n_pop
        self.m_r_cross = r_cross
        self.m_r_mut = r_mut
        self.m_scores = []
        self.m_pop = []
        self.m_mapfile = mapfile
        self.register_list = []

        #wheel selection
        self.m_total_score = 0
        self.m_prob = []
        self.m_cumulative_prob = []

        #elitism
        self.m_listElitism = []
    
    def selection_tournament(self, k=3):
        # select a parent from the population
        # first random selection
        selection_ix = random.randint(0,len(self.m_pop)-1)
        for ix in np.random.randint(0, len(self.m_pop)-1, k-1):
        # check if better (e.g. perform a tournament)
            if self.m_scores[ix] < self.m_scores[selection_ix]:
                selection_ix = ix
        #print(self.moyenne(self.m_pop[selection_ix]))
        return self.m_pop[selection_ix]
    
    def construct_wheel(self):
        index = 0
        for individual_prob in self.m_scores:
            #p=round(individual_prob/self.m_total_score,3)
            p=(individual_prob/self.m_total_score)*1000
            #print(p,"p")
            self.m_prob.append(p)
            if index == 1:
                #self.m_cumulative_prob.append(round(self.m_cumulative_prob[-1]+p,3))
                self.m_cumulative_prob.append(self.m_cumulative_prob[-1]+p)
            else:
                self.m_cumulative_prob.append(p)
            index=1
        #print(self.m_cumulative_prob,"cumulative")
    
    def selection_wheel(self):
        #r = round(random.uniform(0, self.m_cumulative_prob[-1]),3)
        r = random.uniform(0, self.m_cumulative_prob[-1])
        #print(r,"random choice")
        if r <= self.m_cumulative_prob[0]:
            return self.m_pop[0]
        else:
            #TODO -1 maybe not useful
            for i in range(1,len(self.m_cumulative_prob)):
                if self.m_cumulative_prob[i-1] < r <= self.m_cumulative_prob[i]:
                    #print(self.moyenne(self.m_pop[i]))
                    #print(self.m_pop[i],"write in function")
                    return self.m_pop[i]

    def add_elitism(self,elit_indiv):
        self.m_listElitism.append(elit_indiv)
    
    def next_generation(self,list_input):
        for elite in self.m_listElitism:
            list_input.append(elite)
            
    
    def crossover(self,p1,p2,r_cross):

        #TODO attention des enfants peuvent avoir un double de parcelle, vérifier les indices de parcelles
        #lorsqu'un enfant va chercher une parcelle chez un parent !!!!

        return_list=[]
        if random.uniform(0, 1) < r_cross:

            parent_tupple1 = p1.return_m_Clusterlist()
            parent_tupple2 = p2.return_m_Clusterlist()
            parent_cluster1 = p1.return_m_GroupCluserList()
            parent_cluster2 = p2.return_m_GroupCluserList()

            c1 = Individual.Individual_algo_genetic(self.m_mapfile)
            c2 = Individual.Individual_algo_genetic(self.m_mapfile)

            min_cluster = min(len(parent_cluster1), len(parent_cluster2))
            if min_cluster == 1:
                min_parcel = min(len(parent_tupple1),len(parent_tupple2))
                #print(min_parcel,len(parent_tupple1),len(parent_tupple2),"min p1 et p2")
                cut_gene_pt = random.randint(1, min_parcel-1)
                #print(cut_gene_pt,"cut gene")
                c1.changeParcel(p1,p2,cut_gene_pt,parent_tupple1[:cut_gene_pt],parent_tupple2[cut_gene_pt:])
                c2.changeParcel(p1,p2,cut_gene_pt,parent_tupple2[:cut_gene_pt],parent_tupple1[cut_gene_pt:])
            else:
                #print(min_cluster,"passer là")
                cut_gene_cluster = random.randint(1,min_cluster-1)
                # print(cut_gene_cluster)
                # print(parent_cluster1,"p1 before")
                # print(parent_cluster2,"p2 before")
                c1.changeParcel_cluster(p1,p2,parent_cluster1[:cut_gene_cluster],parent_cluster2[cut_gene_cluster:])
                c2.changeParcel_cluster(p1,p2,parent_cluster2[:cut_gene_cluster],parent_cluster1[cut_gene_cluster:])

            #print(min_parcel, "min parcel")

            return_list = [c1,c2]

            for child in return_list:
                #print("child")
                cost = child.returnM_totalCost()
                #print(cost,"cost enfant")
                #print(self.moyenne(child))
                if cost > 50:
                    del return_list[return_list.index(child)]
                #else:
                    # print("enfant")
                    # print("cost enfant" ,child.returnM_totalCost())
                    # print("child score", self.moyenne(child))
                    # child.draw_matrix()
        return return_list
    
    def mutation(self,children, r_mut):
        #TODO prendre un cluster au hasard et le déplacer sur la map
        # take the tupple of parcelle
        # check if a random number is less than r_mut (nearly 20%)
        # if yes then we flip the gene (but in our case we take the line and take another parcelle)
        if random.uniform(0, 1) < r_mut:
            print("draw mut")
            #print(children.return_m_GroupCluserList(),"before")
            #children.draw_matrix()
            children.shift_positions()
            #children.draw_matrix()
            input("ok")
            #print(children.return_m_GroupCluserList(),"after")

    def print_pop(self):
        for indiv in self.m_pop:
            print(f"Le score de l'individu {indiv.returnM_totalCost()+indiv.returnM_totalProd()}")
        return

    def moyenne(self, indiv):
        moyenne = (-1*indiv.returnM_totalComp()-1*indiv.return_m_minDistHabitation()+2*indiv.returnM_totalProd())
        if moyenne < 0:
            moyenne=abs(moyenne)
        else:
            moyenne*=2
        return moyenne    
        
    def genetic_algorithm(self):


        self.m_pop = list()

        for i in range(self.m_n_pop):
            #print("Candidate",i)
            indiv_map = Individual.Individual_algo_genetic(self.m_mapfile)
            indiv_map.chooseCandidate()
            #indiv_map.draw_matrix()
            #print(indiv_map.returnList_Parcel(),"candidate début")
            self.m_pop.append(indiv_map)
        
        best, best_eval = self.m_pop[0], self.moyenne(self.m_pop[0])
        print(best_eval,"init")

        for gen in range(self.m_iter_max):
            print(f"=========== {gen} generation ===========")
            print(f"population: {self.m_n_pop}")

            for individual in self.m_pop:
                #print("############# New indiv #############\n")
                #print(individual.returnM_totalComp(),"compa")
                #print(individual.returnM_totalProd(),"score de prod")
                #print(individual.return_m_minDistHabitation(),"distance from hab.")
                #individual.draw_matrix()
                score = self.moyenne(individual)
                #print(score,"score total")
                #print("\n")
                self.m_scores.append(score)
                self.m_total_score += score
                self.register_list.append(score)
            
            # ranking = self.moyenne_Electre()
            # print(f"valeur production = {self.m_pop[ranking[-1]].returnM_totalProd()}, compacity = {self.m_pop[ranking[-1]].returnM_totalComp()}, distance = {self.m_pop[ranking[-1]].return_m_minDistHabitation()}")
            # self.m_pop[ranking[-1]].draw_matrix()
            # print(f"valeur production = {self.m_pop[ranking[0]].returnM_totalProd()}, compacity = {self.m_pop[ranking[0]].returnM_totalComp()}, distance = {self.m_pop[ranking[0]].return_m_minDistHabitation()}")
            # self.m_pop[ranking[0]].draw_matrix()
            
            #self.m_scores = [individual.m_totalCost+individual.m_totalProd for individual in self.m_pop]           
            self.construct_wheel()

            for i in range(self.m_n_pop):
                #print(f"{i} individu {self.m_scores[i]} score")
                if self.m_scores[i] > best_eval:
                    best, best_eval = self.m_pop[i], self.m_scores[i]
                    #self.add_elitism(self.m_pop[i])
                    print(">%d, new best = %.3f" % (gen, self.m_scores[i]))
                    print(f"valeur production = {best.returnM_totalProd()}, compacity = {best.returnM_totalComp()}, distance = {best.return_m_minDistHabitation()}")
                    best.draw_matrix()

            #TODO strange bc there are 13 individuals that are very good and they are not taken !!!
            #selected = [self.selection_tournament() for _ in range(self.m_n_pop)]
            #selected = [self.selection_wheel() for _ in range(self.m_n_pop)]
            selected=[]
            for ok in range(self.m_n_pop):
                #test = self.selection_wheel()
                #print(test,"test")
                selected.append(self.selection_wheel())

            #print(selected, "liste")

            children = list()
            for i in range(0, self.m_n_pop-1, 2):
                p1, p2 = selected[i], selected[i+1]
                #print(p1,p2)
            
                for c in self.crossover(p1, p2, self.m_r_cross):
                    if len(c.return_m_Clusterlist()) == 0:
                        continue
                    self.mutation(c, self.m_r_mut)
                    children.append(c)
            
            # replace population
            #self.print_pop()
            self.m_pop = children
            #self.next_generation(children)
            self.m_scores = []
            self.m_cumulative_prob=[]
            self.m_n_pop = len(children)
            self.m_total_score=0
            #print(len(best.returnList_Parcel()))
            #print(best,"end")
            #best.draw_matrix()
        #for indiv in self.m_pop:
            #print(((indiv.returnM_totalCost()+indiv.returnM_totalProd())/(indiv.returnM_totalComp())))
            #indiv.draw_matrix()
        fig, ax = plt.subplots()

        # Plot the data as a line graph
        ax.plot(self.register_list)

        # Show the plot
        plt.show()
        for i in self.m_pop:
            print(self.moyenne(i))
        return self.m_pop

    def compute_selection_probs(rankings):
        n = len(rankings)
        weights = [n - i + 1 for i in range(1, n + 1)]
        total_weight = sum(weights)
        probs = [w / total_weight for w in weights]
        return probs

    def build_matrix(self,instances):
        matrix = np.array([[p.returnM_totalComp(), p.returnM_totalProd(), p.return_m_minDistHabitation()] for p in instances])
        print(matrix)
        return matrix
    
    def moyenne_Electre(self):
                
        weights = np.array([5, -10, 1])
        concordance_thresholds = np.array([0.6, 0.6, 0.6,0.6])
        discordance_threshold = 0.3
        self.electre = Electre(self.build_matrix(self.m_pop),weights, concordance_thresholds, discordance_threshold)
        ranking = self.electre.get_ranked_indices()
        return ranking