from algo_genetic import *
from utils import *
from Elcetree import *
import time
import numpy as nps
from mpl_toolkits.mplot3d import Axes3D
import datetime
import os
 
def check_prod(indiv,instance_map):
    prod = 0
    cost=0
    for parcel in indiv.return_clusterList():
        pos = parcel.returnPosition()
        prod+=instance_map.returnObject(pos[1],pos[0]).returnProd()
        cost+=instance_map.returnObject(pos[1],pos[0]).returnCost()
    return prod,cost

def build_matrix(instances):
    matrix = np.array([[p.return_totalComp(),p.return_totalProd(),p.return_minDistHabitation()] for p in instances])
    return matrix

if __name__ == "__main__":
    Instance_Map=Map(constructMap(), costDic)
    iter=7
    pop_length=20000
    liste_electre_final = []
    for _ in range(2):

        start_time = time.time()
        test = Algo_genetic(iter, pop_length,0.9,0.4,Instance_Map)
        liste_pop,best =test.genetic_algorithm()
        elapsed_time = time.time() - start_time
    

        # afficher le temps d'exécution
        print(f"Le temps d'exécution est de {elapsed_time:.2f} secondes")
    
        weights = [-0.7, 0.5, -0.7]
        concordance_index = 0.6
        discordance_index = 0.4
    
        date = datetime.datetime.now()
        current_time = date.strftime("%H_%M_%S")
        os.mkdir(f"./result/{current_time}")
    

        draw_name=f"./result/{current_time}/test_{pop_length}_{iter}_{current_time}"
    
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
        electre = ELECTREE(weights, concordance_index, discordance_index)
        pointsN = electre.normalization(points)
        pointsNW = pointsN *np.array([1, -1, 1])
        pareto_index = find_pareto_frontier_indices(pointsNW)
        matrix = np.array([[p.return_totalComp(),p.return_totalProd(),p.return_minDistHabitation()] for p in liste_pop])
        matrix_normaliser = electre.normalization(matrix)
        plot_pareto_frontier(points,pareto_index)
    
        pop = []
        for indiv_index in pareto_index:
            pop.append(liste_pop[indiv_index])
    
        draw_name_Elec=f"./result/{current_time}/testElectre_{pop_length}_{iter}_{current_time}"
        score_matrix = build_matrix(pop)
        ranking = electre.rank_solutions(score_matrix)
        solut_electre=pop[ranking[0]]
        solut_electre.draw_matrix(draw_name_Elec)
        Instance_Map.write_solution(solut_electre.return_clusterList(),draw_name_Elec)
        solut_electre.compacity(solut_electre.return_clusterList(), draw_name_Elec)
        liste_electre_final.append(solut_electre)
    
    draw_name_Elec=f"./result/{current_time}/final_test_{pop_length}_{iter}_{current_time}"
    Electre_build_matrix=build_matrix(liste_electre_final)
    ranking = electre.rank_solutions(Electre_build_matrix)
    final_solution = liste_electre_final[ranking[0]]
    final_solution.draw_matrix(draw_name_Elec)
    Instance_Map.write_solution(final_solution.return_clusterList(),draw_name_Elec)
    final_solution.compacity(final_solution.return_clusterList(), draw_name_Elec)