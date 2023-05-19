import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
import time
import numpy as nps
from mpl_toolkits.mplot3d import Axes3D
import datetime
import os

if __name__ == "__main__":
    Instance_Map=Map(constructMap(), costDic)
    iter=15
    pop_length=100000

    def check_prod(indiv,instance_map):
        prod = 0
        cost=0
        for parcel in indiv.return_clusterList():
            pos = parcel.returnPosition()
            prod+=instance_map.returnObject(pos[1],pos[0]).returnProd()
            cost+=instance_map.returnObject(pos[1],pos[0]).returnCost()
        return prod,cost

    def build_matrix(instances):
        matrix = np.array([[p.return_dcluster(),p.return_totalProd(),p.return_minDistHabitation()] for p in instances])
        return matrix


    start_time = time.time()
    test = Algo_genetic(iter, pop_length,0.9,0.4,Instance_Map)
    liste_pop,best =test.genetic_algorithm()
    elapsed_time = time.time() - start_time

    # afficher le temps d'exécution
    print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")

    weights = [-0.7, 0.5, -0.5]
    concordance_index = 0.6
    discordance_index = 0.4

    date = datetime.datetime.now()
    current_time = date.strftime("%H_%M_%S")
    os.mkdir(f"./result/{current_time}")


    draw_name=f"./result/{current_time}/test_{pop_length}_{iter}_{current_time}"

    print(check_prod(best,Instance_Map))
    best.draw_matrix(draw_name)
    best_index = liste_pop.index(best)
    print(best_index," :index best")
    Instance_Map.write_solution(best.return_clusterList(),draw_name)
    best.compacity(best.return_clusterList(), draw_name)


    x,y,z=[],[],[]
    for indiv in liste_pop:
        #x.append(indiv.return_totalComp())
        y.append(indiv.return_totalProd())
        z.append(indiv.return_minDistHabitation())
        x.append(indiv.return_dcluster())
    x=np.array(x)
    y=np.array(y)
    z=np.array(z)

    # Empiler les coordonnées pour former une matrice de points
    points = np.column_stack((x, y, z))
    electre = ELECTRE(weights, concordance_index, discordance_index)
    pointsN = electre.normalization(points)
    pointsNW = pointsN *np.array([-1, 1, -1])
    pareto_index = utils.find_pareto_frontier_indices(pointsNW)
    print(pareto_index)
    matrix = np.array([[p.return_dcluster(),p.return_totalProd(),p.return_minDistHabitation()] for p in liste_pop])
    matrix_normaliser = electre.normalization(matrix)
    utils.plot_pareto_frontier(points,pareto_index,[matrix_normaliser[best_index][0],matrix_normaliser[best_index][1],matrix_normaliser[best_index][2]],matrix_normaliser)

    pop = []
    for indiv_index in pareto_index:
        pop.append(liste_pop[indiv_index])

    weights = [-1, 1,-1]
    draw_name_Elec=f"./result/{current_time}/testElectre_{pop_length}_{iter}_{current_time}"
    score_matrix = build_matrix(pop)
    #electre.change_weight(weights)
    ranking = electre.rank_solutions(score_matrix)
    pop[ranking[0]].draw_matrix(draw_name_Elec)
    Instance_Map.write_solution(pop[ranking[0]].return_clusterList(),draw_name_Elec)
    pop[ranking[0]].compacity(pop[ranking[0]].return_clusterList(), draw_name_Elec)
    print(check_prod(pop[ranking[0]],Instance_Map),"elec prod")

    #print("Pareto candidate")
    #for indiv in pop:
    #    indiv.draw_matrix2()
