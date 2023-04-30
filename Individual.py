import random
import compacity 
from parcel import Parcel
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import copy

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

        print(listObjet)
        print(AHSortList)

        return (compacity.returnSurface(listObjet,AHSortList)/self.m_totalArea)*100
    
    #create our individual
    def chooseCandidate(self):
        if len(self.m_listParcel) == 0:
            self.m_listParcel = []
        restoreDic = copy.copy(self.m_map.returnDic())
        while self.m_totalCost+int(next(iter(self.m_map.returnDic()))) <= 50:
            candidateOk = False
            while not candidateOk:
                i = random.randint(0, len(self.m_map.returnGrid())-1)
                j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
                randomCandidate = self.m_map.returnObject(i,j)
                if randomCandidate.returnType() == ' ' and str(randomCandidate.returnCost()) in self.m_map.returnDic().keys() and self.putParcel(randomCandidate):
                    candidateOk = True
                    randomCandidate.changeTypeElem('x')
                    self.m_listParcel.append(randomCandidate)
        #print(self.m_map.returnGrid())
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        self.compacity(self.m_listParcel)
        self.cleanIndividual(self.m_listParcel, restoreDic)
        return self.m_listParcel

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
    
    def returnCompacity(self, listParcel):

        listParcelcopy = copy.copy(listParcel)
        
        
        #print(printList)
        
        minLineParcel = min(listParcel, key=Parcel.returnLinePosition)
        maxLineParcel = max(listParcel, key=Parcel.returnLinePosition)

        lowestLineParcel = [parcel for parcel in listParcel if parcel.returnLinePosition() == minLineParcel.returnLinePosition()]
        highestLineParcel = [parcel for parcel in listParcel if parcel.returnLinePosition() == maxLineParcel.returnLinePosition()]

        lowParcelA  = min(lowestLineParcel, key = Parcel.returnColPosition); lowParcelB  = max(lowestLineParcel, key = Parcel.returnColPosition)
        highParcelA  = min(highestLineParcel, key = Parcel.returnColPosition); highParcelB  = max(highestLineParcel, key = Parcel.returnColPosition)
        
        listParcelcopy.remove(lowParcelA); listParcelcopy.remove(highParcelA)
        if len(lowestLineParcel)>1:
            listParcelcopy.remove(lowParcelB)
        if len(highestLineParcel)>1:
            listParcelcopy.remove(highParcelB)

        minColParcel = min(listParcelcopy, key=Parcel.returnColPosition)
        maxColParcel = max(listParcelcopy, key=Parcel.returnColPosition)

        lowestMidColParcel = [parcel for parcel in listParcelcopy if parcel.returnColPosition() == minColParcel.returnColPosition()]
                              #and parcel.returnColPosition() < lowParcelA.returnColPosition()]
        highestMidColParcel = [parcel for parcel in listParcelcopy if parcel.returnColPosition() == maxColParcel.returnColPosition()]
                              #and parcel.returnColPosition() < highParcelA.returnColPosition()]
        
        
        lowMidParcelA  = min(lowestMidColParcel, key = Parcel.returnLinePosition); lowMidParcelB  = max(lowestMidColParcel, key = Parcel.returnLinePosition)
        highMidParcelA  = min(highestMidColParcel, key = Parcel.returnLinePosition); highMidParcelB  = max(highestMidColParcel, key = Parcel.returnLinePosition)
        
        picliste = [lowParcelA, lowMidParcelA, highParcelA,highMidParcelA]
        printList=[]
        for elem in picliste:
            printList.append(elem.returnPosition())
        print(printList)

        x = []
        y = []
        for elem in printList:
            x.append(elem[0])
            y.append(elem[1])
        # Tracer les points
        plt.scatter(x, y)

        # Créer la surface à partir des coordonnées
        plt.fill_between(x, y, color='blue', alpha=0.2)

        # Calculer l'aire de la surface
        area = np.abs(np.trapz(y, x))

        # Afficher l'aire sur le graphique
        plt.text(2, 2, f'Aire = {area}', fontsize=12)

        # Afficher le graphique
        plt.show()


        self.draw_matrix()


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
