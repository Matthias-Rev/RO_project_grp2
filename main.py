import utils
from algo_genetic import *
from utils import *
from Elcetree import *
import time
import datetime
import os

#build the list for Electre
def build_matrix(instances):
    matrix = np.array([[p.return_dcluster(),p.return_totalProd(),p.return_minDistHabitation()] for p in instances])
    return matrix


if __name__ == "__main__":

    Instance_Map=Map(constructMap(), costDic)   #Instance that handle the maps
    iter=3                                      #Iteration number
    pop_length=1000                             #initial population


    start_time = time.time()
    test = Algo_genetic(iter, pop_length,0.9,0.4,Instance_Map)  #genetic algorithm
    liste_pop,best =test.genetic_algorithm()
    elapsed_time = time.time() - start_time

    # show the execution time
    print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")

    weights = [-0.7, 0.5, -0.7]                 #weight for Electre
    concordance_index = 0.6
    discordance_index = 0.4

    #date and time to diffirentiate multiple tests
    date = datetime.datetime.now()
    current_time = date.strftime("%H_%M_%S")
    os.mkdir(f"./result/{current_time}")        #create a folder that contains the test results

    draw_name=f"./result/{current_time}/test_{pop_length}_{iter}_{current_time}"

    best.draw_matrix(draw_name)                 #download the map for the best individual from the algorithm
    best_index = liste_pop.index(best)

    Instance_Map.write_solution(best.return_clusterList(),draw_name)    #write the solution in a text file
    best.compacity(best.return_clusterList(), draw_name)                #download the compacity figure

    #build a matrix for pareto
    x,y,z=[],[],[]
    for indiv in liste_pop:
        x.append(indiv.return_dcluster())
        y.append(indiv.return_totalProd())
        z.append(indiv.return_minDistHabitation())
    x=np.array(x)
    y=np.array(y)
    z=np.array(z)

    points = np.column_stack((x, y, z))
    electre = ELECTREE(weights, concordance_index, discordance_index)
    pointsN = electre.normalization(points)
    pointsNW = pointsN *np.array([-1, 1, -1])
    pareto_index = utils.find_pareto_frontier_indices(pointsNW)
    matrix = np.array([[p.return_dcluster(),p.return_totalProd(),p.return_minDistHabitation()] for p in liste_pop])
    normalized_matrix = electre.normalization(matrix)
    utils.plot_pareto_frontier(points,pareto_index,[normalized_matrix[best_index][0],normalized_matrix[best_index][1],normalized_matrix[best_index][2]],normalized_matrix)

    #build the population for Electre
    pop = []
    for indiv_index in pareto_index:
        pop.append(liste_pop[indiv_index])

    draw_name_Elec=f"./result/{current_time}/testElectre_{pop_length}_{iter}_{current_time}"
    score_matrix = build_matrix(pop)
    ranking = electre.rank_solutions(score_matrix)
    pop[ranking[0]].draw_matrix(draw_name_Elec)
    Instance_Map.write_solution(pop[ranking[0]].return_clusterList(),draw_name_Elec)
    pop[ranking[0]].compacity(pop[ranking[0]].return_clusterList(), draw_name_Elec)
