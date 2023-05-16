import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
import time
import numpy as nps
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":
    Instance_Map=Map(constructMap(), costDic)

    def build_matrix(instances):
        matrix = np.array([[p.return_totalComp(),p.return_minDistHabitation(), p.return_totalProd()] for p in instances])
        return matrix

    start_time = time.time()
    test = Algo_genetic(3,10000 ,0.80,0.20,Instance_Map)
    liste_pop,best =test.genetic_algorithm()
    elapsed_time = time.time() - start_time
    best.draw_matrix("without Electre")

    # afficher le temps d'exécution
    print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")

    weights = [-0.5, 0.5, -0.5]
    concordance_index = 0.6
    discordance_index = 0.4
    electre = ELECTRE(weights, concordance_index, discordance_index)
    score_matrix = build_matrix(liste_pop)
    ranking = electre.rank_solutions(score_matrix)

    liste_pop[ranking[0]].draw_matrix("with Electre")
    for parcel in best.return_clusterList():
        print(parcel.returnPosition())
    Instance_Map.write_solution(best.return_clusterList())
    

    #weights = [1, 1, 1]
    #matrix = build_matrix(liste_pop)
    #promethe = PrometheeII(matrix,weights)
    #promethe.find_pareto_border()
    #points = []
    #for i in range(0,len(liste_pop)-1):
        #points.append(tuple(matrix[i]))

    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter([p[0] for p in points], [p[1] for p in points], [p[2] for p in points])
    #ax.set_xlabel("Compacity")
    #ax.set_ylabel("Distance")
    #plt.show()
