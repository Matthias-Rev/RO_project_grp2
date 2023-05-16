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
    #electre = ELECTRE(weights, concordance_index, discordance_index)
    score_matrix = build_matrix(liste_pop)
    #ranking = electre.rank_solutions(score_matrix)

    #liste_pop[ranking[0]].draw_matrix("with Electre")
    for parcel in best.return_clusterList():
        print(parcel.returnPosition())
    Instance_Map.write_solution(best.return_clusterList())


    def is_pareto_efficient(costs):
        is_efficient = np.ones(costs.shape[0], dtype=bool)
        for i, c in enumerate(costs):
            if is_efficient[i]:
                is_efficient[is_efficient] = np.any(costs[is_efficient] <= c, axis=1)  # Vérifie la domination
        return is_efficient

    # Générer des points aléatoires en 3D
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

    # Vérifier l'efficacité selon la frontière de Pareto
    is_efficient = is_pareto_efficient(points)

    # Extraire les points de la frontière de Pareto
    pareto_points = points[is_efficient]

    # Afficher les points en 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='blue', label='Points')
    ax.scatter(pareto_points[:, 0], pareto_points[:, 1], pareto_points[:, 2], c='red', label='Frontière de Pareto')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.legend()
    plt.show()
