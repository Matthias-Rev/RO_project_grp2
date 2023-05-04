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
        self.m_GroupCluserList = []

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
    
    def returnM_totalComp(self):
        return self.m_totalCompacity

    def return_m_minDistHabitation(self):
        return self.m_minDistHabitation
    
    def return_m_Clusterlist(self):
        return self.m_CluserList

    def change_cluster(self,parcel):
        self.m_CluserList = parcel
    
    def return_m_GroupCluserList(self):
        return self.m_GroupCluserList
    
    def Cluster_group_change(self, p1,p2,new_parcel1,new_parcel2,cluster_state,cut_gene=0):

        if cluster_state == True:
            for element_1 in new_parcel1:
                self.m_GroupCluserList.append(element_1)
            for element_2 in new_parcel2:
                self.m_GroupCluserList.append(element_2)
        
        else:
            self.m_GroupCluserList.append(new_parcel1[:cut_gene])
            self.m_GroupCluserList.append(new_parcel2[cut_gene:])
            # print(new_parcel1,"1")
            # print(new_parcel2,"2")
            # p1_cluster = p1.return_m_GroupCluserList()
            # for parcel_to_cluster in new_parcel1:
            #     print(parcel_to_cluster,"cluster")
            #     #presence  = [element for element in parcel_to_cluster if element in new_parcel1]
            #     if parcel_to_cluster in p1_cluster:
            #         self.m_GroupCluserList.append(parcel_to_cluster)
            #     else:
            #         list_for_cluster  = [element for element in new_parcel1]
            #         self.m_GroupCluserList.append(list_for_cluster)

    
            # for parcel_to_cluster in p2.return_m_GroupCluserList():
            #     if parcel_to_cluster in new_parcel2:
            #         self.m_GroupCluserList.append(parcel_to_cluster)
            #     else:
            #         list_for_cluster  = [element for element in new_parcel1]
            #         self.m_GroupCluserList.append(list_for_cluster)

    def changeParcel_cluster(self,p1,p2,new_parcel1=[],new_parcel2=[]):
        self.m_totalCost=0
        self.m_totalProd=0

        #print(new_parcel1,"1")
        #print(new_parcel2,"2")
        # print(p1.return_m_GroupCluserList(),"p1")
        # print(p2.return_m_GroupCluserList(),"p2")

        parcel1 = [element for row in new_parcel1 for element in row]
        parcel2 = [element for row in new_parcel2 for element in row]
        #print(parcel1)
        #print(parcel2)
        self.change_cluster(parcel1+parcel2)
        #print(self.m_CluserList,"cluster list")

        for parcel in self.m_CluserList:
            self.m_totalCost+=parcel.returnCost()
            self.m_totalProd+=parcel.returnProd()


        random_parcel_position, random_parcel_x,random_parcel_y,random_parcel = self.random_choice()
        #print(random_parcel_position, random_parcel_x, random_parcel_y,random_parcel)
        #print(random_parcel_position[0]+random_parcel_x,random_parcel_position[1]+random_parcel_y)

        #TODO gros problème ou on peut aller ou of range
        first_parcel = self.m_map.returnGrid()[random_parcel_position[1]+random_parcel_y][random_parcel_position[0]+random_parcel_x]

        while self.m_totalCost+first_parcel.returnCost() <= 50 and first_parcel.returnType()!="R" and first_parcel not in self.m_CluserList:
            print("again")
            self.m_CluserList.insert(self.m_CluserList.index(random_parcel)+1,first_parcel)
            self.m_totalProd+=first_parcel.returnProd()
            self.m_totalCost+=first_parcel.returnCost()
            random_parcel_position, random_parcel_x,random_parcel_y,random_parcel = self.random_choice()
            print(random_parcel_position," ", random_parcel_x," ",random_parcel_y," ",random_parcel)
            first_parcel = self.m_map.returnGrid()[random_parcel_position[1]+random_parcel_y][random_parcel_position[0]+random_parcel_x]

        
        #print(self.m_CluserList,"next cluster")

        self.Cluster_group_change(p1,p2,new_parcel1,new_parcel2,True)
        #print(self.m_GroupCluserList,"before min")

        #print(self.return_m_GroupCluserList(),"grp")

        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()

    def moyenne(self):
        return (1*self.returnM_totalComp()+1*self.return_m_minDistHabitation()+2*self.returnM_totalProd())  

    def random_choice(self):
        out_of_range = True
        while out_of_range == True:
            random_parcel = random.choice(self.m_CluserList)
            random_parcel_position = random_parcel.returnPosition()
            random_parcel_y = random.choice([-1,1])
            random_parcel_x = random.choice([1,-1])
            if random_parcel_position[0]+random_parcel_x < 170 and random_parcel_position[1]+random_parcel_y < 70:
                out_of_range = False
        return random_parcel_position,random_parcel_x,random_parcel_y,random_parcel

    def changeParcel(self ,p1,p2,cut_gene,new_parcel1=[],new_parcel2=[]):

        self.m_totalCost=0
        self.m_totalProd=0

        #print(new_parcel1,"1")
        #print(new_parcel2,"2")
        #print(p1.return_m_GroupCluserList(),"p1")
        #print(p2.return_m_GroupCluserList(),"p2")

        self.change_cluster(new_parcel1+new_parcel2)

        for parcel in self.m_CluserList:
            self.m_totalCost+=parcel.returnCost()
            self.m_totalProd+=parcel.returnProd()
    
        #pq pas faire parent aléatoire
        while cut_gene+1 < len(p1.return_m_Clusterlist()) and self.m_totalCost+p1.return_m_Clusterlist()[cut_gene+1].returnCost() <= 50:
            parcel_add = p1.return_m_Clusterlist()[cut_gene+1]
            new_parcel1.append(parcel_add)
            self.m_totalProd+=parcel_add.returnProd()
            self.m_totalCost+=parcel_add.returnCost()
            cut_gene+=1

        self.change_cluster(new_parcel1+new_parcel2)

        self.Cluster_group_change(p1,p2,new_parcel1,new_parcel2,False,cut_gene)

        #print(self.return_m_GroupCluserList(),"grp")

        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()
    
    def showMatrix(self):
        return self.m_map.returnGrid()
    
    #define the compacity
    def compacity(self, listParcels):
        listObjet = compacity.recoveryCoords(listParcels)
        #Maj de l'emplacement dans le sens anti-horlogique par aprtitionnement
        AHSortList = compacity.Partitionning(listObjet)

        listObjet = set(listObjet)
        AHSortList = set(AHSortList)
        listObjet.difference_update(AHSortList)
        listObjet = list(listObjet)
        AHSortList = list(AHSortList)

        #Tri des listes par ligne
        listObjet = compacity.returnSortLineList(listObjet)
        AHSortList.append(listObjet[0])
        AHSortList.append(listObjet[-1])
        AHSortList = compacity.returnSortLineList(AHSortList)

        #Tri des partitions de liste par colones
        listObjet = compacity.returnPartialColSort2(listObjet, 'L')
        AHSortList = compacity.returnPartialColSort2(AHSortList, 'R')

        compacity.returnVisitedPoint(listObjet)
        compacity.returnVisitedPoint(AHSortList)

        # print(listObjet)
        # print(AHSortList)

        return (compacity.returnSurface(listObjet,AHSortList)/self.m_totalArea)*100
    
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
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.cleanIndividual(self.m_CluserList, restoreDic)
        print(f"valeur production = {self.m_totalProd}, compacity = {self.m_totalCompacity}, score = {self.moyenne()}")
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
        
        for instane_parcel in self.return_m_Clusterlist():
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
        self.m_GroupCluserList = allCluster

        return 0

    def min_dist_parcel(self,group_taken_parcel):
        min_distances = []
        habitate_parcel=self.m_map.returnHouses()
        #TODO sometimes grouplist = [[OO], [OO],[]]
        for p in group_taken_parcel:
            distances_p = []
            for hLine in habitate_parcel:
                for h in hLine:
                    # print(h)
                    # print(p.returnPosition())
                    distance = math.sqrt((h[0] - p.returnPosition()[1])**2 + (h[1] -p.returnPosition()[0])**2)
                    distances_p.append(distance)
            min_distances.append(min(distances_p))
            occur_nb = len(min_distances)
        #print(min(min_distances))
        return min(min_distances)# / occur_nb

    def moyenne_min_dist_parcel(self):
        coeff_dist = []
        self.Cluster_verif()
        #print(self.m_GroupCluserList, "min problem")
        for p in self.m_GroupCluserList:
            dist_p = self.min_dist_parcel(p)
            coeff_dist.append(dist_p)
        return sum(coeff_dist) / len(coeff_dist)

    def Cluster_verif(self):
        for cluster_list in self.m_GroupCluserList:
            if len(cluster_list)==0:
                self.m_GroupCluserList.remove(cluster_list)