import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
import time
import numpy as nps
from mpl_toolkits.mplot3d import Axes3D

Instance_Map=Map(constructMap(), costDic)

def build_matrix(instances):
    matrix = np.array([[p.return_totalComp(),p.return_minDistHabitation(), p.return_totalProd()] for p in instances])
    return matrix

start_time = time.time()
test = Algo_genetic(1,1000,0.80,0.99,Instance_Map)
liste_pop =test.genetic_algorithm()
elapsed_time = time.time() - start_time

# afficher le temps d'exécution
print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")







