import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
import time
import numpy as nps
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

if __name__ == "__main__":
    Instance_Map=Map(constructMap(), costDic)

    def build_matrix(instances):
        matrix = np.array([[p.return_totalComp(),p.return_minDistHabitation(), p.return_totalProd()] for p in instances])
        return matrix

    start_time = time.time()
    test = Algo_genetic(1,10000 ,0.80,0.20,Instance_Map)
    liste_pop,best =test.genetic_algorithm()
    elapsed_time = time.time() - start_time
    best.draw_matrix("without Electre")

    # afficher le temps d'exécution
    print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")

    #essayer d'avoir +- 1000 individus
    weights = [-0.5, 0.5, -0.5]
    concordance_index = 0.6
    discordance_index = 0.4
    electre = ELECTRE(weights, concordance_index, discordance_index)
    #score_matrix = build_matrix(liste_pop)
    #ranking = electre.rank_solutions(score_matrix)

    #liste_pop[ranking[0]].draw_matrix("with Electre")
    for parcel in best.return_clusterList():
        print(parcel.returnPosition())
    Instance_Map.write_solution(best.return_clusterList())


    def find_pareto_frontier_indices(points):
        num_points = points.shape[0]
        is_pareto_efficient = np.ones(num_points, dtype=bool)

        for i in range(num_points):
            if is_pareto_efficient[i]:
                current_point = points[i]
                is_pareto_efficient[is_pareto_efficient] = np.any(points[is_pareto_efficient] <= current_point, axis=1)

        pareto_indices = np.where(is_pareto_efficient)[0]
        return pareto_indices

    def plot_pareto_frontier(points, pareto_indices):
        pareto_points = points[pareto_indices]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        #ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='blue', label='Frontière de Pareto')
        #ax.scatter(pareto_points[:, 0], pareto_points[:, 2], pareto_points[:, 1], c='red', label='Frontière de Pareto')
        ax.scatter(pareto_points[:, 0], pareto_points[:, 1], pareto_points[:, 2], c='red', label='Frontière de Pareto')
        #ax.scatter(pareto_points[:, 0], pareto_points[:, 1], pareto_points[:, 2], c='red', label='Frontière de Pareto')
        ax.set_xlabel('Compacity')
        ax.set_ylabel('Production')
        ax.set_zlabel('Habitation Dist')

        # Changer l'échelle des axes
        #ax.set_xlim(0, 0.2)
        #ax.set_ylim(0.2, 0.6)
        #ax.set_zlim(0, 0.8)

        plt.legend()
        plt.show()


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
    pointsN = electre.normalization(points)
    pointsNW = pointsN *np.array([-1, 1, -1])
    pareto_index = find_pareto_frontier_indices(pointsNW)
    plot_pareto_frontier(points,pareto_index)

