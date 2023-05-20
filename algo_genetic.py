import random
import copy
import Individual
import bisect
import numpy as np
import time
import multiprocessing

class Algo_genetic:
    def __init__(self, nbr_iter,n_pop,r_cross,r_mut,mapfile) -> None:
        self.m_iter_max = nbr_iter                          #Number of generation
        self.m_n_pop = n_pop                                #Number of individual for the first generation
        self.m_r_cross = r_cross                            #coef for crossover
        self.m_r_mut = r_mut                                #coef for mutation
        self.m_scores = []                                  #list of score
        self.m_pop = []                                     #List that contain individuals
        self.m_mapfile = mapfile                            #matrix with cost,Prod,type of each parcel
        self.m_register_list = []                           #list that keep the score of each indiv. through the generation (allows to see the trend)
        self.m_initial_doc=self.m_mapfile.returnDic()       #dictionnary with the cost and numbers of parcel with this cost
                                                            #ex: {4: 354} -> parcel cost: number of parcels with this cost
        self.m_total_score = 0                              #total score of the population
        self.m_prob = []                                    #list of probability for the roulette selection
        self.m_cumulative_prob = []                         #cumulative list of probability for the roulette selec.

        #elitism
        self.m_listElitism = []                             #list of the ellitist

        #multiprocessing
        self.num_processes = multiprocessing.cpu_count()    #number of core
    
    #add the individual to the list to keep it for the next generation
    def add_elitism(self,elit_indiv):
        self.m_listElitism.append(elit_indiv)
        
    #build the normalized score
    def build_matrix_score(self,instances):
        matrix = np.array([[p.return_totalComp(), p.return_totalProd(), p.return_minDistHabitation(),p.return_dcluster()] for p in instances])
        normalized_scores = np.zeros_like(matrix)
        for i in range(matrix.shape[1]):
            normalized_scores[:,i] = (matrix[:,i] - np.min(matrix[:,i])) / (np.max(matrix[:,i]) - np.min(matrix[:,i]))
        return normalized_scores

    #construct the cumulative list for the selection
    def construct_roulette(self):
        index = 0
        for individual_prob in self.m_scores:
            p=(individual_prob/self.m_total_score)*100
            self.m_prob.append(p)
            if index == 1:
                self.m_cumulative_prob.append(self.m_cumulative_prob[-1]+p)
            else:
                self.m_cumulative_prob.append(p)
            index=1
    
    #create an individual for the fist generation
    def create_population(self,_):
        m_initial_doc_init = copy.deepcopy(self.m_initial_doc)
        indiv_map = Individual.Individual_algo_genetic(self.m_mapfile)
        indiv_map.chooseCandidate(m_initial_doc_init)
        return indiv_map
    
    #run faster selection_wheel function with created process
    def process_chunk(self, chunk_size):
        chunk_results = []
        for _ in range(chunk_size):
            chunk_results.append(self.selection_wheel())
        return chunk_results
    
    #creat mutliple process as possible for run faster function
    def run_parallel(self):
        chunk_size = self.m_n_pop // self.num_processes
        with multiprocessing.Pool(self.num_processes) as pool:
            chunks = [chunk_size] * (self.num_processes - 1)
            chunks.append(self.m_n_pop - chunk_size * (self.num_processes - 1))
            results = pool.map(self.process_chunk, chunks)
        selected = []
        for chunk_result in results:
            selected.extend(chunk_result)
        return selected
    
    #take two parents to create zero to two children
    def crossover(self,p1,p2,r_cross):
        return_list=[]
        m_initial_doc_init = copy.deepcopy(self.m_initial_doc)

        if random.uniform(0, 1) < r_cross:
            parent_tupple1 = p1.return_clusterList()
            parent_cluster1 = p1.return_cluserListGroup()
            parent_tupple2 = p2.return_clusterList()
            parent_cluster2 = p2.return_cluserListGroup()

            #if the parent is composed of a single cluster, we'll cut this cluster in multiple parcels and give
            #some of the parcels to a children.
            #if there are many clusters, parents'll give some clusters to their children
            c1 = Individual.Individual_algo_genetic(self.m_mapfile)
            c1.initiate_Cost_Dic(m_initial_doc_init)
            min_cluster = min(len(parent_cluster1), len(parent_cluster2))
            if min_cluster == 1:
                #a parent has only one cluster
                min_parcel = min(len(parent_tupple1),len(parent_tupple2))
                cut_gene_pt = random.randint(1, min_parcel-1)
                c1.changeParcel(p1,p2,cut_gene_pt,parent_tupple1[:cut_gene_pt],parent_tupple2[cut_gene_pt:])
            else: 
                cut_gene_cluster = random.randint(1,min_cluster-1)
                c1.change_clusterParcel(parent_cluster1[:cut_gene_cluster],parent_cluster2[cut_gene_cluster:])
            return_list.append(c1)
            if random.uniform(0, 1) < r_cross:
                c2 = Individual.Individual_algo_genetic(self.m_mapfile)
                c2.initiate_Cost_Dic(m_initial_doc_init)
                if min_cluster == 1:
                    min_parcel = min(len(parent_tupple1),len(parent_tupple2))
                    cut_gene_pt = random.randint(1, min_parcel-1)
                    c2.changeParcel(p1,p2,cut_gene_pt,parent_tupple2[:cut_gene_pt],parent_tupple1[cut_gene_pt:])
                else:
                    cut_gene_cluster = random.randint(1,min_cluster-1)
                    c2.change_clusterParcel(parent_cluster2[:cut_gene_cluster],parent_cluster1[cut_gene_cluster:])
                return_list.append(c2)

        #if a children is not valid, we kill it
        for child in return_list:
            cost = child.return_totalCost()
            if cost > 50:
                del return_list[return_list.index(child)]
        return return_list

    #main function
    def genetic_algorithm(self):
        self.m_pop = list()                                                 #list of population
   
        begin = time.time()                                                 #to measure the time efficiency
        pool = multiprocessing.Pool(self.num_processes)
        self.m_pop = pool.map(self.create_population, range(self.m_n_pop))  #use multi process to create our first gene.
        end = time.time()
        print(f"it takes {end-begin} to create population")
        best_eval = 0                                                       #initiate the best score

        for gen in range(self.m_iter_max):

            print(f"=========== {gen} generation ===========")
            print(f"population: {self.m_n_pop}")

            i = 0
            matrix_score = self.build_matrix_score(self.m_pop)             #build the matrix for the normalized scores
            for individual in self.m_pop:
                current_line =matrix_score[i]
                score = (current_line[0] *-1) + current_line[1] + (current_line[2]*-1) - (0.5*current_line[3])
                self.m_scores.append(score)
                self.m_total_score += score
                self.m_register_list.append(score)
                i +=1
                if self.m_scores[-1] > best_eval:                         #print the actual best score
                    best, best_eval = individual, self.m_scores[-1]
                    self.add_elitism(best)                                #add it to the elitist list
                    print(">%d, new best = %.3f" % (gen, best_eval))

            self.construct_roulette()                                     #build the cumulative probability list

            selected=[]
            begin = time.time()
            selected = self.run_parallel()                                #select the parents for the reproduction
            end = time.time()
            print(f"it takes {end-begin} to make selection_wheel")

            begin = time.time()
            children = list()
            for i in range(0, self.m_n_pop-1, 2):
                p1, p2 = selected[i], selected[i+1]
                crossoverList = self.crossover(p1, p2, self.m_r_cross)    #mate the selected parents

                for c in crossoverList:
                    if len(c.return_clusterList()) == 0:
                        continue
                    self.mutation(c, self.m_r_mut)                        #mutate a child
                    children.append(c)
            end = time.time()
            print(f"it takes {end-begin} to create childs")
            
            self.m_pop = children                                         #next generation so the parents die
            self.m_scores = []
            self.m_cumulative_prob=[]
            self.m_n_pop = len(children)
            self.m_total_score=0
            self.next_generation(children)                               #add the elitist list to the next gen.

        # Plot the data as a line graph
        #fig, ax = plt.subplots()
        #ax.plot(self.m_register_list)

        return self.m_pop, best                                          #return the last pop. and the best individual
 
    #add the elitist list to the next generation
    def next_generation(self,list_input):
        for elite in self.m_listElitism:
            list_input.append(elite)
        return 0

    def mutation(self,children, r_mut):
        # take the tupple of parcelle
        # check if a random number is less than r_mut
        # if yes then we flip the gene (but in our case we move a cluster with a random distance)
        if random.uniform(0, 1) < r_mut:
            children.shift_positions()
        return 0

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
        #select the parents
        #better the parent is, better chance it has to be selected
        #see this as a casino wheel, but a good indivdual has many case (increase its chance)
        select =random.uniform(0, self.m_cumulative_prob[-1])
        index = bisect.bisect_right(self.m_cumulative_prob, select)
        return self.m_pop[index]