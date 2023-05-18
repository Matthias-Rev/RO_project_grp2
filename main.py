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
    iter=2
    pop_length=100

    def build_matrix(instances):
        matrix = np.array([[p.return_totalComp(), p.return_totalProd(),p.return_minDistHabitation()] for p in instances])
        return matrix

    start_time = time.time()
    test = Algo_genetic(iter, pop_length,0.80,0.20,Instance_Map)
    liste_pop,best =test.genetic_algorithm()
    elapsed_time = time.time() - start_time

    # afficher le temps d'exécution
    print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")

    weights = [-0.5, 0.5, -0.5]
    concordance_index = 0.6
    discordance_index = 0.4

    draw_name=f"test_{pop_length}_{iter}"

    best.draw_matrix(draw_name)
    for parcel in best.return_clusterList():
        print(parcel.returnPosition())
    Instance_Map.write_solution(best.return_clusterList(),draw_name)
    

    x,y,z=[],[],[]
    for indiv in liste_pop:
        x.append(indiv.return_totalComp())
        y.append(indiv.return_totalProd())
        z.append(indiv.return_minDistHabitation())
    x=np.array(x)
    y=np.array(y)
    z=np.array(z)

    # Empiler les coordonnées pour former une matrice de points
    points = np.column_stack((x, y, z))
    electre = ELECTRE(weights, concordance_index, discordance_index)
    pointsN = electre.normalization(points)
    pointsNW = pointsN *np.array([-1, 1, -1])
    pareto_index = utils.find_pareto_frontier_indices(pointsNW)
    utils.plot_pareto_frontier(points,pareto_index)

    score_matrix = build_matrix(liste_pop)
    ranking = electre.rank_solutions(score_matrix)
    liste_pop[ranking[0]].draw_matrix("with Electre")
