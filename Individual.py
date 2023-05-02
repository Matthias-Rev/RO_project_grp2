import random
import compacity 
from parcel import Parcel
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy
import math

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Individual_algo_genetic:

    def __init__(self, map,listParcel=[]):
        self.m_map = map
        self.m_listParcel = listParcel
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        self.m_totalArea = map.returnTotalArea()
        self.m_CluserList = []
        self.m_minDistHabitation = 0

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
    def compacity(self, listParcels):
        listObjet = compacity.recoveryCoords(listParcels)
        #Maj de l'emplacement dans le sens anti-horlogique par partitionnement
        AHSortList = compacity.Partitionning(listObjet)

        listObjet = set(listObjet)
        AHSortList = set(AHSortList)
        listObjet.difference_update(AHSortList)
        listObjet = list(listObjet)
        AHSortList = list(AHSortList)

        #Tri des listes par ligne
        listObjet = compacity.returnSortLineList(listObjet)
        
        if len(AHSortList) > 0:
            recoveryElem = AHSortList[0]
            AHSortList[0] = listObjet[0]
            AHSortList.append(recoveryElem)
        AHSortList = compacity.returnSortLineList(AHSortList)

        #Tri des partitions de liste par colones
        listObjet = compacity.returnPartialColSort2(listObjet, 'L')
        AHSortList = compacity.returnPartialColSort2(AHSortList, 'R')

        compacity.returnVisitedPoint(listObjet)
        compacity.returnVisitedPoint(AHSortList)

        #Ajout de la jonction entre les deux parties
        junctionList = compacity.returnJunctionSurface(listObjet,AHSortList)

        print(listObjet)
        print(AHSortList)
        print(junctionList)

        return (compacity.returnSurface(listObjet,AHSortList,junctionList)/self.m_totalArea)*100
    
    #create our individual
    def chooseCandidate(self):
        if len(self.m_listParcel) == 0:
            self.m_listParcel = []
        restoreDic = copy.copy(self.m_map.returnDic())
        randomNumber = random.randint(1,5)
        while self.m_totalCost+int(next(iter(self.m_map.returnDic()))) <= 50 and len(self.m_listParcel) < randomNumber:
            candidateOk = False
            while not candidateOk:
                i = random.randint(0, len(self.m_map.returnGrid())-1)
                j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
                randomCandidate = self.m_map.returnObject(i,j)
                if randomCandidate.returnType() == ' ' and str(randomCandidate.returnCost()) in self.m_map.returnDic().keys() and self.putParcel(randomCandidate):
                    candidateOk = True
                    randomCandidate.changeTypeElem('x')
                    self.m_listParcel.append(randomCandidate)

        self.choosePosition()
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        #self.m_minDistHabitation = self.moyenne_min_dist_parcel()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.cleanIndividual(self.m_CluserList, restoreDic)
        return self.m_CluserList

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


    def choosePosition(self):

        allCluster = []
        i = 0
        while i<len(self.m_listParcel):
            allCluster.append([self.m_listParcel[i]])
            i +=1

        while self.m_totalCost+int(next(iter(self.m_map.returnDic()))) <= 50:
            # print("lowest key = ",int(next(iter(self.m_map.returnDic()))))
            candidateOk = False
            # Choix aléatoire d'un cluster dans la liste
            cluster = random.choice(allCluster)
            parcelChoice = random.choice(cluster)
            col, row = parcelChoice.returnPosition()
            i,j = col,row
            while not candidateOk:
                randomCol = random.randint(-1,1)
                randomRow = random.randint(-1,1)
                if (i + randomCol) < self.m_map.returnWidth()-1 and (i + randomCol) >= 0: 
                    i += randomCol
                if (j + randomRow) < self.m_map.returnHeigth()-1 and (j + randomRow) >= 0: 
                    j += randomRow
                randomCandidate = self.m_map.returnObject(j,i)
                if randomCandidate.returnType() == ' ' and str(randomCandidate.returnCost()) in self.m_map.returnDic().keys() and self.putParcel(randomCandidate):
                    randomCandidate.changeTypeElem('x')
                    self.m_listParcel.append(randomCandidate)
                    cluster.append(randomCandidate)
                    candidateOk = True
        
        for list in allCluster:
            for elem in list:
                self.m_CluserList.append(elem)

        return 0

    def min_dist_parcel(self, group_taken_parcel):
        min_distances = []
        habitate_parcel = self.m_map.returnHouses()
        for p in group_taken_parcel:
            distances_p = []
            for hLine in habitate_parcel:
                for h in hLine:
                    distance = math.sqrt((h[0] - p.returnPosition()[0]) ** 2 + (h[1] - p.returnPosition()[1]) ** 2)
                    distances_p.append(distance)
            min_distances.append(min(distances_p))
        print(min_distances)
        occur_nb = len(min_distances)
        min_dist = min(min_distances) if min_distances else 0
        return min_dist / occur_nb

    def moyenne_min_dist_parcel(self):
        coeff_dist = []
        for p in self.m_GroupCluserList:
            dist_p = self.min_dist_parcel(p)
            coeff_dist.append(dist_p)
        return sum(coeff_dist) / len(coeff_dist)