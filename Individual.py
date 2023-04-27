import random 
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib import colors
import utils
import copy

# class Individual_algo_genetic:

#     def __init__(self, map,listParcel=[]):
#         self.m_map = map
#         self.m_totalCost = 0                        #must be <500.000
#         self.m_totalProd = 0
#         self.m_totalCompacity = 0
#         self.m_listParcel = listParcel
#         #distance entre les zones habitées
#         #compacité ???? -> surface d'une "nasse"

#         self.m_parcels_placed = []
    
#     def showMatrix(self):
#         return self.m_map.returnGrid()
    
#     def returnList_Parcel(self):
#         return self.m_listParcel
        
#     #define the compacity
#     def coefCompact(self, highestNasse, allParcel):
#         return highestNasse/allParcel
    
#     def returnM_totalCost(self):
#         return self.m_totalCost
    
#     def returnM_totalProd(self):
#         return self.m_totalProd
    
#     def changeParcel(self, new_parcel):
#         #print(new_parcel)
#         self.m_listParcel = new_parcel
#         for parcel in self.m_listParcel:
#             self.m_totalCost+=parcel.returnCost()
#             self.m_totalProd+=parcel.returnProd()
    
#     #create our individual
#     def chooseCandidate(self):
#         print(self.m_map.returnGrid())
#         self.m_listParcel = []
#         restoreDic = copy.copy(self.m_map.returnDic())
#         while self.m_totalCost+int(next(iter(restoreDic))) <= 50:
#             candidateOk = False
#             while not candidateOk:
#                 i = random.randint(0, len(self.m_map.returnGrid())-1)
#                 j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
#                 randomCandidate = self.m_map.returnObject(i,j)
#                 if randomCandidate.returnType() == ' ' and self.putParcel(randomCandidate,restoreDic):
#                     candidateOk = True
#                     #randomCandidate.changeTypeElem('x')
#                     self.m_listParcel.append(randomCandidate)
#         print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
#         #self.cleanIndividual(self.m_listParcel, restoreDic)
#         return self.m_listParcel

#     #define if a parcel is checked
#     #TODO problème: python donne les arguments par référence donc dic est modifier je pense pour tous les individus
#     #TODO optimiser ce que je change l'individu (genre map reste commun à tous,mais dico deviens personnelle)
#     def putParcel(self, parcelCandidate,restoreDic):
#         if not parcelCandidate.parcelPlaced() and ((parcelCandidate.returnCost()+self.m_totalCost)<=50):
#             parcelCandidate.parcelPlaced(True)
#             restoreDic[str(parcelCandidate.returnCost())] -=1
#             if restoreDic[str(parcelCandidate.returnCost())] == 0:
#                 print("mort de la clé:", restoreDic[str(parcelCandidate.returnCost())])
#                 restoreDic.pop(parcelCandidate.returnCost())
#             self.m_totalCost += parcelCandidate.returnCost()
#             self.m_totalProd += parcelCandidate.returnProd()
#             #parcel checked
#             return True 
        
#         #if constraints are not met
#         return False
    




class Individual_algo_genetic:

    def __init__(self, map,listParcel=[]):
        self.m_map = map
        self.m_listParcel = listParcel
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
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
    
    #create our individual
    def chooseCandidate(self):
        self.m_listParcel = []
        restoreDic = copy.copy(self.m_map.returnDic())
        while self.m_totalCost+int(next(iter(self.m_map.returnDic()))) < 50:
            candidateOk = False
            while not candidateOk:
                i = random.randint(0, len(self.m_map.returnGrid())-1)
                j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
                randomCandidate = self.m_map.returnObject(i,j)
                if randomCandidate.returnType() == ' ' and self.putParcel(randomCandidate):
                    candidateOk = True
                    randomCandidate.changeTypeElem('x')
                    self.m_listParcel.append(randomCandidate)
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        self.cleanIndividual(self.m_listParcel, restoreDic)
        return self.m_listParcel

    #define if a parcel is checked
    def putParcel(self, parcelCandidate):
        if not parcelCandidate.parcelPlaced() and ((parcelCandidate.returnCost()+self.m_totalCost)<=50):
            parcelCandidate.parcelPlaced(True)
            self.m_map.returnDic()[str(parcelCandidate.returnCost())] -=1
            if self.m_map.returnDic()[str(parcelCandidate.returnCost())] == 0:
                print("mort de la clé:", self.m_map.returnDic()[str(parcelCandidate.returnCost())])
                self.m_map.returnDic().pop(parcelCandidate.returnCost())
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