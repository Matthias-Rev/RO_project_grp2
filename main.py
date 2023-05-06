import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
from Electre import *
import numpy as np
import copy

Instance_Map=Map(constructMap(), costDic)


# # Print the resulting matrix
# #Instance_Map = Map(readMapFile(mapfile))
# #Instance_Map.posInit()
# #print(Instance_Map.returnGrid())

def build_matrix(instances):
    matrix = np.array([[p.returnM_totalComp(), p.returnM_totalComp(), p.return_m_minDistHabitation()] for p in instances])
    return matrix

# #algo = Individual.Individual_algo_genetic(Matrix, Instance_Map, 0)
test = Algo_genetic(1,1000,0.80,0.20,Instance_Map)
liste_pop =test.genetic_algorithm()

weights = [0.5, 0.5, -0.5]
# Seuils de concordance et de discordance
concordance_thresholds = np.array([0.6, 0.6, 0.6, 0.6])
discordance_threshold = 0.3
matrix = build_matrix(liste_pop)

electre = Electre(matrix, weights, concordance_thresholds, discordance_threshold)
pareto_border = electre.pareto_frontier(matrix)
electre.show_3d_graph(pareto_border)

#promethe = PrometheeII(matrix,weights)
#promethe.find_pareto_border()
#promethe.show_3d_graph()

# mapObject = Map(constructMap(), costDic)
# i = 0
# algo = Individual.Individual_algo_genetic(copy.copy(mapObject))
# a = algo.chooseCandidate()