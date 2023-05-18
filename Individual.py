import random
import compacity
import parcel
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy
import math
import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

BREAK = 0
VALID = 1


class Individual_algo_genetic:

    def __init__(self, map, listParcel=[]):
        self.m_map = map
        self.m_totalArea = map.returnTotalArea()
        self.m_totalCost = 0  # must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        self.m_distance_cluster = 0

        self.m_listParcel = listParcel
        self.m_CluserList = []
        self.m_GroupCluserList = []
        self.m_minDistHabitation = 0
        self.m_dic_pos = {}

    def initiate_Cost_Dic(self, dic_init):
        self.m_dic_pos = dic_init

    def change_cluster(self, parcel):
        self.m_CluserList = parcel
        return 0

    def change_clusterList(self):
        self.m_CluserList = [element for row in self.m_GroupCluserList for element in row]
        return 0

    def change_clusterSingleGroup(self, cluster_list):
        self.m_GroupCluserList = cluster_list
        return 0

    def change_clusterGroup(self, new_parcel1, new_parcel2, cluster_state):
        if cluster_state == True:
            for element_1 in new_parcel1:
                self.m_GroupCluserList.append(element_1)
            for element_2 in new_parcel2:
                self.m_GroupCluserList.append(element_2)

        else:
            self.m_GroupCluserList.append(new_parcel1)
            self.m_GroupCluserList.append(new_parcel2)
        return 0

    def change_clusterParcel(self, p1, p2, new_parcel1=[], new_parcel2=[]):

        self.m_totalCost = 0
        self.m_totalProd = 0

        parcel_u, parcel2_u = self.check_unicity_Group(new_parcel1, new_parcel2)

        parcel1 = [element for row in parcel_u for element in row]
        parcel2 = [element for row in parcel2_u for element in row]

        self.change_cluster(parcel1 + parcel2)
        self.change_clusterGroup(parcel_u, parcel2_u, True)

        for p_parcel in self.m_CluserList:
            x, y = p_parcel.returnPosition()
            parcel = self.m_map.returnObject(y, x)
            self.m_dic_pos[str(parcel.returnCost())] -= 1
            self.m_totalCost += parcel.returnCost()
            self.m_totalProd += parcel.returnProd()

        if self.m_totalCost < 50:
            self.list_choice()

        self.change_clusterList()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()
        self.m_distance_cluster = self.distance_cluster()

        return 0

    def changeParcel(self, p1, p2, cut_gene, new_parcel1=[], new_parcel2=[]):

        self.m_totalCost = 0
        self.m_totalProd = 0

        parcel1, parcel2 = self.check_unicity(new_parcel1, new_parcel2)
        self.change_cluster(parcel1 + parcel2)
        self.change_clusterGroup(parcel1, parcel2, False)

        for p_parcel in self.m_CluserList:
            x, y = p_parcel.returnPosition()
            parcel = self.m_map.returnObject(y, x)
            self.m_dic_pos[str(parcel.returnCost())] -= 1
            self.m_totalCost += parcel.returnCost()
            self.m_totalProd += parcel.returnProd()

        # pq pas faire parent aléatoire ?
        while cut_gene + 1 < len(p1.return_clusterList()) and self.m_totalCost + p1.return_clusterList()[
            cut_gene + 1].returnCost() <= 50:
            parcel_add = p1.return_clusterList()[cut_gene + 1]
            self.m_GroupCluserList[0].insert(0, parcel_add)
            self.m_totalProd += parcel_add.returnProd()
            self.m_totalCost += parcel_add.returnCost()
            self.m_dic_pos[str(parcel_add.returnCost())] -= 1
            cut_gene += 1
        self.change_clusterList()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()
        self.m_distance_cluster = self.distance_cluster()

    # define the compacity
    def compacity(self, listParcels):
        listObjet = compacity.recoveryCoords(listParcels)
        # Maj de l'emplacement dans le sens anti-horlogique par partitionnement
        AHSortList = compacity.Partitionning(listObjet)

        listObjet = set(listObjet)
        AHSortList = set(AHSortList)
        listObjet.difference_update(AHSortList)
        listObjet = list(listObjet)
        AHSortList = list(AHSortList)

        # Tri des listes par ligne
        listObjet = compacity.returnSortLineList(listObjet)

        if len(AHSortList) > 0:
            recoveryElem = AHSortList[0]
            AHSortList[0] = listObjet[0]
            AHSortList.append(recoveryElem)
        AHSortList = compacity.returnSortLineList(AHSortList)

        # Tri des partitions de liste par colones
        listObjet = compacity.returnPartialColSort2(listObjet, 'L')
        AHSortList = compacity.returnPartialColSort2(AHSortList, 'R')

        compacity.returnVisitedPoint(listObjet)
        compacity.returnVisitedPoint(AHSortList)

        # Ajout de la jonction entre les deux parties
        junctionList = compacity.returnJunctionSurface(listObjet, AHSortList)

        return (compacity.returnSurface(listObjet, AHSortList, junctionList) / self.m_totalArea) * 100

    # create our individual
    def chooseCandidate(self, init_doc):

        self.initiate_Cost_Dic(init_doc)
        h = self.m_map.returnHeigth()
        w = self.m_map.returnWidth()

        if len(self.m_listParcel) == 0:
            self.m_listParcel = []

        randomNumber = random.randint(1, 5)
        while self.m_totalCost + int(next(iter(self.m_dic_pos))) <= 50 and len(self.m_listParcel) < randomNumber:
            candidateOk = False
            while not candidateOk:
                if len(self.m_listParcel) == 0:
                    i = random.randint(0, len(self.m_map.returnGrid()) - 1)
                    j = random.randint(0, len(self.m_map.returnGrid()[i]) - 1)
                else:
                    i_prime = self.m_listParcel[0].returnPosition()[1] - 20
                    j_prime = self.m_listParcel[0].returnPosition()[0] - 20
                    i_prime2 = self.m_listParcel[0].returnPosition()[1] + 20
                    j_prime2 = self.m_listParcel[0].returnPosition()[0] + 20
                    i_prime, j_prime = self.in_grid(i_prime, j_prime, h, w)
                    i_prime2, j_prime2 = self.in_grid(i_prime2, j_prime2, h, w)
                    i = random.randint(i_prime, i_prime2 - 1)
                    j = random.randint(j_prime, j_prime2 - 1)
                randomCandidate = self.m_map.returnObject(i, j)
                if randomCandidate.returnType() == ' ' and str(
                        randomCandidate.returnCost()) in self.m_dic_pos.keys() and self.putParcel(randomCandidate):
                    candidateOk = True
                    self.m_listParcel.append(randomCandidate)
        self.choosePosition()
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_distance_cluster = self.distance_cluster()
        # print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        return self.m_CluserList

    def in_grid(self, i, j, h, w):
        if i > h:
            i = h - 1
        elif i < 0:
            i = 0
        if j > w:
            j = w - 1
        elif j < 0:
            j = 0
        return i, j

    def choosePosition(self):

        allCluster = []
        i = 0

        while i < len(self.m_listParcel):
            allCluster.append([self.m_listParcel[i]])
            i += 1

        while self.m_totalCost + int(next(iter(self.m_dic_pos))) <= 50:
            candidateOk = False
            # Choix aléatoire d'un cluster dans la liste
            cluster = random.choice(allCluster)
            parcelChoice = random.choice(cluster)
            col, row = parcelChoice.returnPosition()
            i, j = col, row
            while not candidateOk:
                randomCol = random.randint(-1, 1)
                randomRow = random.randint(-1, 1)
                if (i + randomCol) < self.m_map.returnWidth() - 1 and (i + randomCol) >= 0:
                    i += randomCol
                if (j + randomRow) < self.m_map.returnHeigth() - 1 and (j + randomRow) >= 0:
                    j += randomRow
                randomCandidate = self.m_map.returnObject(j, i)
                if randomCandidate.returnType() == ' ' and str(
                        randomCandidate.returnCost()) in self.m_dic_pos.keys() and self.putParcel(randomCandidate):
                    self.m_listParcel.append(randomCandidate)
                    cluster.append(randomCandidate)
                    candidateOk = True

        for list in allCluster:
            for elem in list:
                self.m_CluserList.append(elem)
        self.m_GroupCluserList = allCluster

        return 0

    def draw_matrix(self, name):

        # Define the dimensions of the map
        list_parcel_linear = [element for row in self.m_GroupCluserList
                              for element in row]
        matrix = self.m_map.returnGrid()

        y = len(matrix)
        x = len(matrix[0])

        # Define the colors for each letter
        colors = {
            "R": "grey",
            "C": "white",
            "x": "red",
            " ": "black"
        }

        # Define the colormap
        cmap = matplotlib.colors.ListedColormap(list(colors.values()))

        # Create the image array
        data = np.zeros((y, x), dtype=int)
        for i in range(y):
            for j in range(x):
                char = matrix[i][j].returnType()
                parcel = matrix[i][j]
                if char != 'x':
                    color = list(colors.keys()).index(char) + 1
                    data[i, j] = color
                else:
                    data[i, j] = "4"

        for instane_parcel in list_parcel_linear:
            data[instane_parcel.returnPosition()[1], instane_parcel.returnPosition()[0]] = 3

        # Display the image
        plt.figure(figsize=(10, 5))
        plt.figtext(0, 0,
                    f"C={self.return_totalComp()},P={self.return_totalProd()},D={self.return_minDistHabitation()},DD={self.return_dcluster()}",
                    fontsize=10, color='black')
        plt.imshow(data, cmap=cmap, interpolation="nearest")
        plt.axis("off")
        plt.show()
        #plt.savefig(f"{name}.png")

    def min_dist_parcel(self, group_taken_parcel):
        min_distances = []
        habitate_parcel = self.m_map.returnHouses()
        for p in group_taken_parcel:
            distances_p = []
            for hLine in habitate_parcel:
                for h in hLine:
                    distance = math.sqrt((h[0] - p.returnPosition()[1]) ** 2 + (h[1] - p.returnPosition()[0]) ** 2)
                    distances_p.append(distance)
            min_distances.append(min(distances_p))  # tester max

        distance = 0
        if len(min_distances) > 0:
            distance = sum(min_distances) / len(min_distances)
        else:
            distance = 0

        return distance  # / occur_nb

    # Calculate the average score of an individual
    def moyenne(self):
        moy = (1 * self.return_totalComp() + 1 * self.return_minDistHabitation() + 2 * self.return_totalProd())
        return moy

    def moyenne_min_dist_parcel(self):
        coeff_dist = []
        for p in self.m_GroupCluserList:
            dist_p = self.min_dist_parcel(p)
            coeff_dist.append(dist_p)
        return sum(coeff_dist) / len(coeff_dist)

    # define if a parcel is checked
    def putParcel(self, parcelCandidate):
        if parcelCandidate not in self.m_listParcel and ((parcelCandidate.returnCost() + self.m_totalCost) <= 50):
            self.m_dic_pos[str(parcelCandidate.returnCost())] -= 1
            if self.m_dic_pos[str(parcelCandidate.returnCost())] == 0:
                self.m_dic_pos.pop(str(parcelCandidate.returnCost()))
            self.m_totalCost += parcelCandidate.returnCost()
            self.m_totalProd += parcelCandidate.returnProd()
            return True
            # if constraints are not met
        return False

    def check_map(self):
        count = 0
        count_S = 0
        for row in self.m_map.returnGrid():
            for i in row:
                if i.returnType() not in ["R", "C", "x"]:
                    count = count + 1
                if i.returnPutState() == False:
                    count_S += 1
        return count, count_S

    def list_choice(self):
        for cluster_list in self.m_GroupCluserList:
            for parcel in cluster_list:
                liste_possible = []
                position_init = parcel.returnPosition()
                if position_init[0] > 1:
                    down = (position_init[0] - 1, position_init[1])
                    liste_possible.append(down)
                if position_init[0] < 168:
                    up = (position_init[0] + 1, position_init[1])
                    liste_possible.append(up)
                if position_init[1] > 1:
                    left = (position_init[0], position_init[1] - 1)
                    liste_possible.append(left)
                if position_init[1] < 68:
                    right = (position_init[0], position_init[1] + 1)
                    liste_possible.append(right)
                for try_position in liste_possible:
                    parcel_candidate = self.m_map.returnObject(try_position[1], try_position[0])
                    if self.m_totalCost + parcel_candidate.returnCost() <= 50 and parcel_candidate not in self.m_CluserList and parcel_candidate.returnType() not in [
                        "R", "C"]:
                        self.m_dic_pos[str(parcel_candidate.returnCost())] -= 1
                        self.m_totalCost += parcel_candidate.returnCost()
                        self.m_totalProd += parcel_candidate.returnProd()
                        self.m_GroupCluserList[self.m_GroupCluserList.index(cluster_list)].append(parcel_candidate)
                        return 0
        return 0

    def random_choice(self):
        out_of_range = True
        while out_of_range == True:
            random_list = random.choice(self.m_GroupCluserList)
            random_parcel = random.choice(random_list)
            index_random_parcel = self.m_GroupCluserList.index(random_list)
            random_parcel_position = random_parcel.returnPosition()
            random_parcel_y = random.choice([-1, 1])
            random_parcel_x = random.choice([1, -1])
            if random_parcel_position[0] + random_parcel_x < 170 and random_parcel_position[1] + random_parcel_y < 70:
                out_of_range = False
        return random_parcel_position, random_parcel_x, random_parcel_y, index_random_parcel

    def shift_positions(self):

        debug = 0
        state = VALID
        list_cluster = self.return_cluserListGroup()
        list_of_parcels = random.choice(self.m_GroupCluserList)
        index_list = self.m_GroupCluserList.index(list_of_parcels)
        # Décalage de 1 ou 2 unités en x et/ou y pour chaque parcelle

        parcel_moved_safely = False
        while parcel_moved_safely == False:
            debug = debug + 1
            if debug == 20:
                state = BREAK
                break
            i = random.randint(-2, 2)
            j = random.randint(-2, 2)
            liste_new_parcel = []
            for parcel in list_of_parcels:
                col, row = parcel.returnPosition()

                # vérification position hors des limites
                if (i + col) < self.m_map.returnWidth() - 1 and (i + col) >= 0:
                    col += i
                if (j + row) < self.m_map.returnHeigth() - 1 and (j + row) >= 0:
                    row += j
                parcelCandidate = self.m_map.returnObject(row, col)

                # Réinititalisation de la parcelle initiale
                if str(parcel.returnCost()) in self.m_dic_pos:
                    self.m_dic_pos[str(parcel.returnCost())] += 1
                elif str(parcel.returnCost()) not in self.m_dic_pos:
                    self.m_dic_pos[str(parcel.returnCost())] = 1
                self.m_totalCost -= parcel.returnCost()
                self.m_totalProd -= parcel.returnProd()

                # Vérification que la nouvelle position est valide (pas déjà occupée...)
                if ((parcelCandidate.returnType() == ' ' and parcelCandidate not in list_of_parcels) and str(
                        parcelCandidate.returnCost()) in self.m_dic_pos.keys()
                        and self.putParcel(parcelCandidate)):
                    liste_new_parcel.append(parcelCandidate)

                # On garde la parcelle initiale en cas d'echec du candidat
                else:
                    self.m_dic_pos[str(parcel.returnCost())] -= 1
                    if self.m_dic_pos[str(parcel.returnCost())] == 0:
                        self.m_dic_pos.pop(str(parcel.returnCost()))
                    self.m_totalCost += parcel.returnCost()
                    self.m_totalProd += parcel.returnProd()

            if len(list_of_parcels) == len(liste_new_parcel):
                parcel_moved_safely = True

        if state == VALID:
            list_cluster[index_list] = liste_new_parcel
            self.change_clusterSingleGroup(list_cluster)
            self.change_clusterList()
        return 0

    # ALL RETURN_FUNCTION
    def return_clusterList(self):
        return self.m_CluserList

    def return_cluserListGroup(self):
        return self.m_GroupCluserList

    def return_grid(self):
        return self.m_map.returnGrid()

    def return_listParcel(self):
        return self.m_listParcel

    def return_minDistHabitation(self):
        return self.m_minDistHabitation

    def return_totalCost(self):
        return self.m_totalCost

    def return_totalComp(self):
        return self.m_totalCompacity

    def return_totalProd(self):
        return self.m_totalProd

    def return_dic(self):
        return self.m_dic_pos

    def return_dcluster(self):
        return self.m_distance_cluster

    def check_unicity(self, parcel1, parcel2):
        seen = set()
        liste_candidat = [parcel1, parcel2]

        for candidate_list in liste_candidat:
            for i in range(len(candidate_list) - 1, -1, -1):
                if candidate_list[i] in seen:
                    del candidate_list[i]
                else:
                    seen.add(candidate_list[i])

        return liste_candidat[0], liste_candidat[1]

    def check_unicity_Group(self, new_parcel1, new_parcel2):
        seen = set()
        liste_counter = 0
        liste_canditate = [new_parcel1, new_parcel2]
        for new_parcel in liste_canditate:
            while liste_counter < len(new_parcel):
                i_counter = 0
                while 0 <= i_counter < len(new_parcel[liste_counter]):
                    if new_parcel[liste_counter][i_counter] in seen:
                        del new_parcel[liste_counter][i_counter]
                        i_counter -= 1
                    if len(new_parcel[liste_counter]) != 0:
                        seen.add(new_parcel[liste_counter][i_counter])
                    else:
                        del new_parcel[liste_counter]
                        liste_counter -= 1
                        i_counter = len(new_parcel[liste_counter])
                    i_counter += 1
                liste_counter += 1
        return liste_canditate[0], liste_canditate[1]

    def distance_cluster(self):
        parcel_mean_x = []
        parcel_mean_y = []
        cluster_pos = []
        distance_clusters = 0
        num_points = len(self.m_GroupCluserList)
        for cluster in self.m_GroupCluserList:
            if num_points == 1:
                return 0
            for parcel in cluster:
                pos_parcel = parcel.returnPosition()
                parcel_mean_x.append(pos_parcel[0])
                parcel_mean_y.append(pos_parcel[1])
            cluster_x = sum(parcel_mean_x) / len(parcel_mean_x)
            cluster_y = sum(parcel_mean_y) / len(parcel_mean_y)
            cluster_pos.append((cluster_y, cluster_x))

        for parcel_first in range(num_points):
            x1, y1 = cluster_pos[parcel_first]
            for second_parcel in range(parcel_first + 1, num_points):
                x2, y2 = cluster_pos[second_parcel]
                distance = self.mean_distance(x1, y1, x2, y2)
                distance_clusters += distance

        return distance_clusters / (num_points * (num_points - 1) / 2)

    def mean_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)