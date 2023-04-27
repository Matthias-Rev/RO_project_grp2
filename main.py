import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
import numpy as np

Instance_Map=Map(constructMap(), costDic)


# Print the resulting matrix
#Instance_Map = Map(readMapFile(mapfile))
#Instance_Map.posInit()
#print(Instance_Map.returnGrid())

#algo = Individual.Individual_algo_genetic(Matrix, Instance_Map, 0)
test = Algo_genetic(5,1000,0.80,0.20,Instance_Map)
liste_pop =test.genetic_algorithm()

promethe = PrometheeII([1,2])
print(promethe.build_matrix(liste_pop))
promethe.normalize_matrix()
promethe.calculate_concordance_and_discordance_matrices()
promethe.upgrade_id()
promethe.find_pareto_border()
promethe.show_3d_graph()

# algo.returnNbParcel()
#a = algo.chooseCandidate()
#print(a)
#matrix[0][90]

#print(a)
# print(len(a))
#algo.putParcel()
#algo.objectDistance((-10,10))
