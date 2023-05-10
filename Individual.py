import random
import compacity 
import parcel
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
        self.m_totalArea = map.returnTotalArea()
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        
        self.m_listParcel = listParcel
        self.m_CluserList = []
        self.m_GroupCluserList = []
        self.m_minDistHabitation = 0
        
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"
    
    def change_cluster(self,parcel):
        self.m_CluserList = parcel
        return 0
    
    def change_clusterList(self):
        self.m_CluserList = [element for row in self.m_GroupCluserList for element in row]
        return 0
    
    def change_clusterSingleGroup(self,cluster_list):
        self.m_GroupCluserList = cluster_list
        return 0
    
    def change_clusterGroup(self,new_parcel1,new_parcel2,cluster_state):
        if cluster_state == True:
            for element_1 in new_parcel1:
                self.m_GroupCluserList.append(element_1)
            for element_2 in new_parcel2:
                self.m_GroupCluserList.append(element_2)
        
        else:
            self.m_GroupCluserList.append(new_parcel1)
            self.m_GroupCluserList.append(new_parcel2)
        return 0
    
    def change_clusterParcel(self,p1,p2,new_parcel1=[],new_parcel2=[]):

        self.m_totalCost=0
        self.m_totalProd=0

        parcel1 = [element for row in new_parcel1 for element in row]
        parcel2 = [element for row in new_parcel2 for element in row]

        self.change_cluster(parcel1+parcel2)
        self.change_clusterGroup(new_parcel1,new_parcel2,True)

        for p_parcel in self.m_CluserList:
            x,y = p_parcel.returnPosition()
            parcel = self.m_map.returnObject(y,x)
            parcel.parcelPlaced(True)
            parcel.changeTypeElem('x')
            self.m_totalCost+=parcel.returnCost()
            self.m_totalProd+=parcel.returnProd()


        random_parcel_position, random_parcel_x,random_parcel_y,index = self.random_choice()
        first_parcel = self.m_map.returnGrid()[random_parcel_position[1]+random_parcel_y][random_parcel_position[0]+random_parcel_x]

        while self.m_totalCost+first_parcel.returnCost() <= 50 and first_parcel.returnType() not in ["R","C"] and first_parcel not in self.m_CluserList:
            self.m_GroupCluserList[index].append(first_parcel)
            self.m_totalProd+=first_parcel.returnProd()
            self.m_totalCost+=first_parcel.returnCost()
            first_parcel.parcelPlaced(True)
            first_parcel.changeTypeElem('x')
            random_parcel_position, random_parcel_x,random_parcel_y,index = self.random_choice()
            first_parcel = self.m_map.returnGrid()[random_parcel_position[1]+random_parcel_y][random_parcel_position[0]+random_parcel_x]

        self.change_clusterList()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()

        return 0

    def changeParcel(self ,p1,p2,cut_gene,new_parcel1=[],new_parcel2=[]):

        self.m_totalCost=0
        self.m_totalProd=0

        self.change_cluster(new_parcel1+new_parcel2)
        self.change_clusterGroup(new_parcel1,new_parcel2,False)

        for p_parcel in self.m_CluserList:
            x,y = p_parcel.returnPosition()
            parcel = self.m_map.returnObject(y,x)
            parcel.parcelPlaced(True)
            #parcel.changeTypeElem('x')
            self.m_totalCost+=parcel.returnCost()
            self.m_totalProd+=parcel.returnProd()

        #pq pas faire parent aléatoire ?
        while cut_gene+1 < len(p1.return_clusterList()) and self.m_totalCost+p1.return_clusterList()[cut_gene+1].returnCost() <= 50:
            parcel_add = p1.return_clusterList()[cut_gene+1]
            self.m_GroupCluserList[0].insert(0,parcel_add)
            self.m_totalProd+=parcel_add.returnProd()
            self.m_totalCost+=parcel_add.returnCost()

            parcel_add.parcelPlaced(True)
            #parcel_add.changeTypeElem('x')

            cut_gene+=1
        self.change_clusterList()
        self.m_totalCompacity = self.compacity(self.m_CluserList)
        self.m_minDistHabitation = self.moyenne_min_dist_parcel()
    
    def cleanIndividual(self, listeParcelObj, initialDoc):
        for elem in listeParcelObj:
            elem.changeTypeElem(' ')
            elem.parcelPlaced(False)
        self.m_map.restoreDic(initialDoc)
        return 0 
     
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

        return (compacity.returnSurface(listObjet,AHSortList,junctionList)/self.m_totalArea)*100
    
    #create our individual
    def chooseCandidate(self):

        if len(self.m_listParcel) == 0:
            self.m_listParcel = []
        #restoreDic = copy.copy(self.m_map.returnDic())
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
        return self.m_CluserList

    def choosePosition(self):

        allCluster = []
        i = 0

        while i<len(self.m_listParcel):
            allCluster.append([self.m_listParcel[i]])
            i +=1

        while self.m_totalCost+int(next(iter(self.m_map.returnDic()))) <= 50:
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

    def draw_matrix(self):

        # Define the dimensions of the map
        list_parcel_linear =  [element for row in self.m_GroupCluserList 
                               for element in row]
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
                parcel=matrix[i][j]
                if char != 'x':
                    color = list(colors.keys()).index(char) + 1
                    data[i, j] = color
                else:
                    data[i, j] = "4"
        
        for instane_parcel in list_parcel_linear:
            data[instane_parcel.returnPosition()[1],instane_parcel.returnPosition()[0]] = 3

        # Display the image
        plt.figure(figsize=(10, 5))
        plt.imshow(data, cmap=cmap, interpolation="nearest")
        plt.axis("off")
        plt.show()

    def min_dist_parcel(self,group_taken_parcel):
        min_distances = []
        habitate_parcel=self.m_map.returnHouses()
        for p in group_taken_parcel:
            distances_p = []
            for hLine in habitate_parcel:
                for h in hLine:
                    distance = math.sqrt((h[0] - p.returnPosition()[1])**2 + (h[1] -p.returnPosition()[0])**2)
                    distances_p.append(distance)
            min_distances.append(min(distances_p))
            occur_nb = len(min_distances)
        return min(min_distances)# / occur_nb

    #Calculate the average score of an individual
    def moyenne(self):
        moy = (1*self.return_totalComp()+1*self.return_minDistHabitation()+2*self.return_totalProd())
        return moy

    def moyenne_min_dist_parcel(self):
        coeff_dist = []
        for p in self.m_GroupCluserList:
            dist_p = self.min_dist_parcel(p)
            coeff_dist.append(dist_p)
        return sum(coeff_dist) / len(coeff_dist)
    
    #define if a parcel is checked
    def putParcel(self, parcelCandidate):
        if not parcelCandidate.parcelPlaced() and ((parcelCandidate.returnCost()+self.m_totalCost)<=50):
            parcelCandidate.parcelPlaced(True)
            self.m_map.returnDic()[str(parcelCandidate.returnCost())] -=1
            if self.m_map.returnDic()[str(parcelCandidate.returnCost())] == 0:
                self.m_map.returnDic().pop(str(parcelCandidate.returnCost()))
            self.m_totalCost += parcelCandidate.returnCost()
            self.m_totalProd += parcelCandidate.returnProd()
            #parcel checked
            return True 
        #if constraints are not met
        return False
   
    def random_choice(self):
        out_of_range = True
        while out_of_range == True:
            random_list = random.choice(self.m_GroupCluserList)
            random_parcel = random.choice(random_list)
            index_random_parcel = self.m_GroupCluserList.index(random_list)
            random_parcel_position = random_parcel.returnPosition()
            random_parcel_y = random.choice([-1,1])
            random_parcel_x = random.choice([1,-1])
            if random_parcel_position[0]+random_parcel_x < 170 and random_parcel_position[1]+random_parcel_y < 70:
                out_of_range = False
        return random_parcel_position,random_parcel_x,random_parcel_y,index_random_parcel
    
    def shift_positions(self):    

        list_cluster = self.return_cluserListGroup()
        list_of_parcels = random.choice(self.m_GroupCluserList)
        index_list = self.m_GroupCluserList.index(list_of_parcels)
        # Décalage de 1 ou 2 unités en x et/ou y pour chaque parcelle
        parcel_moved_safely = False
        while parcel_moved_safely==False:
            n = 0
            n +=1
            if n ==1000:
                break

            i = random.randint(-10, 10)
            j = random.randint(-10, 10)
            liste_new_parcel = []
            for parcel in list_of_parcels:
                col, row = parcel.returnPosition()

                #vérification position hors des limites
                if (i + col) < self.m_map.returnWidth()-1 and (i + col) >= 0: 
                    col += i
                if (j + row) < self.m_map.returnHeigth()-1 and (j + row) >= 0: 
                    row += j
                parcelCandidate = self.m_map.returnObject(row,col)
                
                #Réinititalisation de la parcelle initiale
                #parcel.changeTypeElem(' ') 
                parcel.parcelPlaced(False)
                if str(parcel.returnCost()) in self.m_map.returnDic():
                    self.m_map.returnDic()[str(parcel.returnCost())] += 1
                elif str(parcel.returnCost()) not in self.m_map.returnDic():
                    self.m_map.returnDic()[str(parcel.returnCost())] = 1    
                self.m_totalCost -= parcel.returnCost()
                self.m_totalProd -= parcel.returnProd()
                
                # Vérification que la nouvelle position est valide (pas déjà occupée...)
                #TODO peut tourner en boucle !!!!!!!
                if ((parcelCandidate.returnType() == ' ' and parcelCandidate not in list_of_parcels) and str(parcelCandidate.returnCost()) in self.m_map.returnDic().keys() 
                    and self.putParcel(parcelCandidate)):
                    liste_new_parcel.append(parcelCandidate)

                # On garde la parcelle initiale en cas d'echec du candidat
                else :
                    #parcel.changeTypeElem('x') 
                    parcel.parcelPlaced(True)
                    self.m_map.returnDic()[str(parcel.returnCost())] -= 1
                    if self.m_map.returnDic()[str(parcel.returnCost())] == 0:
                        self.m_map.returnDic().pop(str(parcel.returnCost()))
                    self.m_totalCost += parcel.returnCost()
                    self.m_totalProd += parcel.returnProd()

            if len(list_of_parcels) == len(liste_new_parcel):
                parcel_moved_safely=True

        list_cluster[index_list]=liste_new_parcel
        self.change_clusterSingleGroup(list_cluster)
        self.change_clusterList()
        return 0

    #ALL RETURN_FUNCTION
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
        