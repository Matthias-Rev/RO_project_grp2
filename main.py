import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
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

weights = [1, 1, 1]
matrix = build_matrix(liste_pop)
promethe = PrometheeII(matrix,weights)
promethe.find_pareto_border()
promethe.show_3d_graph()

# mapObject = Map(constructMap(), costDic)
# i = 0
# algo = Individual.Individual_algo_genetic(copy.copy(mapObject))
# a = algo.chooseCandidate()