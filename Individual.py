import random 
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib import colors
import utils
import copy

class Individual_algo_genetic:

    def __init__(self, map,listParcel=[]):
        self.m_map = map
        self.m_listParcel = listParcel
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        self.m_listCluster = []
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"

        self.m_parcels_placed = []
    
    def returnList_Parcel(self):
        return self.m_listParcel
        
    #define the compacity
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel
    
    def returnM_totalCost(self):
        return self.m_totalCost
    
    def returnM_totalProd(self):
        return self.m_totalProd
    
    def changeParcel(self, new_parcel):
        #print(new_parcel)
        self.m_listParcel = new_parcel
        for parcel in self.m_listParcel:
            self.m_totalCost+=parcel.returnCost()
            self.m_totalProd+=parcel.returnProd()
    
    def showMatrix(self):
        return self.m_map.returnGrid()
    
    #define the compacity
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel

    def min_dist_parcel(self, group_taken_parcel, habitate_parcel):
        min_distances = []
        for p in group_taken_parcel:
            distances_p = []
            for h in habitate_parcel:
                distances_p.append(np.linalg.norm(np.array(p.coordonnees) - np.array(h.coordonnees)))
            min_distances.append(min(distances_p))
            occur_nb = min_distances.count(min_distances)
            return min(min_distances) / occur_nb

    def moyenne_min_dist_parcel(self, all_group_taken_parcel, habitate_parcel):
        coeff_dist = []
        for p in all_group_taken_parcel:
            dist_p = self.min_dist_parcel(p, habitate_parcel)
            coeff_dist.append(dist_p)
        return sum(coeff_dist) / len(coeff_dist)
    
    #create our individual
    def chooseCandidate(self):
        self.m_listParcel = []
        restoreDic = copy.copy(self.m_map.returnDic())
        while self.m_totalCost+int(next(iter(self.m_map.returnDic()))) <= 50:
                randomCandidate = self.m_map.returnObject(0,0)
                if randomCandidate.returnType() == ' ' and str(randomCandidate.returnCost()) in self.m_map.returnDic().keys() and self.putParcel(randomCandidate):
                    randomCandidate.changeTypeElem('x')
                    self.m_listParcel.append(randomCandidate)
        #print(self.m_map.returnGrid())
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        self.cleanIndividual(self.m_listParcel, restoreDic)
        return self.m_listParcel


    def createCluster(self,max_num_Cluster):
        self.m_listCluster = []
        restoreDic = copy.copy(self.m_map.returnDic())
        for i in range(random.randint(0, max_num_Cluster)):
            candidateOk = False
        while not candidateOk:
            i = random.randint(0, len(self.m_map.returnGrid()) - 1)
            j = random.randint(0, len(self.m_map.returnGrid()[i]) - 1)
            randomCandidate = self.m_map.returnObject(i, j)
            if randomCandidate.returnType() == ' ' and self.putParcel(randomCandidate):
                candidateOk = True
                randomCandidate.changeTypeElem('x')
                self.m_listCluster.append(randomCandidate)
        self.cleanIndividual(self.m_listParcel, restoreDic)
        return self.m_listCluster

    def choosePosition(self, cluster_List):
        # Copie de la carte actuelle
        restoreDic = copy.copy(self.m_map.returnDic())

        # Choix aléatoire d'un cluster dans la liste
        cluster = random.choice(cluster_List)

        # Boucle pour essayer de trouver une position adjacente libre
        for i in range(len(cluster)):
            # Choix aléatoire d'une parcelle dans le cluster
            parcel = random.choice(cluster)
            row, col = parcel.getPosition()

            # Choix aléatoire d'une position adjacente à la parcelle choisie
            positions_adjacentes = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            #random.shuffle(positions_adjacentes)
            random_element = random.choice(positions_adjacentes)
            randomCandidate = self.m_map.returnObject(random_element)

            for pos in positions_adjacentes:
                # Vérification si la position est libre
                if randomCandidate.returnType() == ' ' and self.putParcel(randomCandidate):
                    # Ajout de la position à l'élément choisi
                    new_parcel = parcel(pos[0], pos[1], 'x')
                    cluster.append(new_parcel)
                    self.m_listCluster.append(new_parcel)

                    # Retrait de la position de la parcelle originale
                    cluster.remove(parcel)
                    self.m_listCluster.remove(parcel)

                    # Restauration de la carte originale
                    self.cleanIndividual(self.m_listParcel, restoreDic)

                    # Modification de la cluster_List avec le cluster modifié
                    cluster_List[cluster_List.index(cluster)] = cluster

                    return cluster_List

            # Si aucune position adjacente n'a été trouvée, on recommence avec un autre cluster
            new_cluster_list = [c for c in cluster_List if c != cluster]
            if len(new_cluster_list) > 0:
                return self.choosePosition(new_cluster_list)
            else:
                return cluster_List

    #define if a parcel is checked
    def putParcel(self, parcelCandidate):
        if not parcelCandidate.parcelPlaced() and ((parcelCandidate.returnCost()+self.m_totalCost)<=50):
            parcelCandidate.parcelPlaced(True)
            self.m_map.returnDic()[str(parcelCandidate.returnCost())] -=1
            if self.m_map.returnDic()[str(parcelCandidate.returnCost())] == 0:

                #print("mort de la clé:", parcelCandidate.returnCost())
                self.m_map.returnDic().pop(str(parcelCandidate.returnCost()))
                
            self.m_totalCost += parcelCandidate.returnCost()
            self.m_totalProd += parcelCandidate.returnProd()
            #parcel checked
            return True 
        #if constraints are not met
        return False
    
    def cleanIndividual(self, listeParcelObj, initialDoc):
        for elem in listeParcelObj:
            elem.changeTypeElem(' ')
            elem.parcelPlaced(False)
        self.m_totalCost = 0
        self.m_totalProd = 0
        self.m_map.restoreDic(initialDoc)
        return 0 
        
    ### in process...
    def objectDistance(self, objectA=(0,0), objectB=(0,0), i=0):
        print("object = ", self.m_map.m_roads_pos[i])
        print(f"difference ligne = {abs(objectA[0]-objectB[0])}, difference col = {abs(objectA[1]-objectB[1])}")
    
    ### in process...
    def findNearestObj(self, posActualObj=(0,0),typeTargetObj=' '):
        found = False
        distance = 0
        while not found:
            if typeTargetObj == 'R':
                self.m_map.m_roads_pos
            
    def draw_matrix(self):

        # Define the dimensions of the map
        matrix = self.m_map.returnGrid()
        y =len(matrix)
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
                if char != 'x':
                    color = list(colors.keys()).index(char) + 1
                    data[i, j] = color
                else:
                    data[i, j] = "4"
        
        for instane_parcel in self.returnList_Parcel():
            data[instane_parcel.returnPosition()[1],instane_parcel.returnPosition()[0]] = 3

        # Display the image
        plt.figure(figsize=(10, 5))
        plt.imshow(data, cmap=cmap, interpolation="nearest")
        plt.axis("off")
        plt.show()
