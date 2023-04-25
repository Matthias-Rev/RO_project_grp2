import random 
import math
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import colors
from matplotlib.colors import ListedColormap
import utils

class Individual_algo_genetic:

    def __init__(self, m_map_parcel, map, dic_utils,listParcel=[]):
        self.m_nb_parcel = 0
        self.m_map_parcel = m_map_parcel
        self.m_map = map
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        self.m_listParcel = listParcel
        self.m_dic_utils = dic_utils
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"

        self.m_parcels_placed = []
    
    def showMatrix(self):
        return self.m_map.returnGrid()
    
    def returnNbParcel(self):
        return self.m_nb_parcel

    def returnList_Parcel(self):
        return self.m_listParcel

    def returnM_totalCost(self):
        return self.m_totalCost
    
    def returnM_totalProd(self):
        return self.m_totalProd

    def changeParcel(self, new_parcel):
        #print(new_parcel)
        self.m_listParcel = new_parcel
        for parcel in self.m_listParcel:
            self.m_totalCost+=self.m_map_parcel[parcel[0]][parcel[1]].returnCost()
            self.m_totalProd+=self.m_map_parcel[parcel[0]][parcel[1]].returnProd()
    
    #define the compacity
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel
    
    #create our individual
    def chooseCandidate(self):
        self.m_listParcel = []
        while self.m_totalCost+int(next(iter(self.m_dic_utils))) <= 50:#50
            #print("waiting here")
            candidateOk = False
            while not candidateOk:
                print(len(self.m_map.returnGrid()),"self map len")
                #print("waiting candidate ok")
                i = random.randint(0, len(self.m_map.returnGrid())-1)
                j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
                print(len(self.m_map.returnGrid()[i]),"length list")
                randomCandidate = self.m_map.returnGrid()[i][j]
                #print(randomCandidate)
                if randomCandidate == ' ' and self.putParcel(i,j):
                    candidateOk = True
                    #self.m_map.changeGrid((i,j), 'x')
                    candidate = (i,j)
                    self.m_listParcel.append(candidate)
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        return self.m_listParcel

    #define if a parcel is checked
    def putParcel(self,i,j):
        print(len(self.m_map_parcel))
        print(i," ",j)
        randomParcel = self.m_map_parcel[i][j]
        if (randomParcel.returnCost()+self.m_totalCost)<=50:
            self.m_map_parcel[i][j].parcelPlaced(True)
            self.m_dic_utils[str(randomParcel.returnCost())] -=1
            if self.m_dic_utils[str(randomParcel.returnCost())] == 0:
                print(randomParcel.returnCost(), "le random parcel cost")
                print(str(randomParcel.returnCost()), "le random parcel cost en string")
                print("mort de la clé:", self.m_dic_utils[str(randomParcel.returnCost())])
                print(self.m_dic_utils)
                self.m_dic_utils.pop(str(randomParcel.returnCost()))
            self.m_totalCost += randomParcel.returnCost()
            self.m_totalProd += randomParcel.returnProd()
            return True 
        return False

    def draw_matrix(self):
        # Define the matrix
        matrix = self.m_map.returnGrid()
        print(matrix)
        for i in self.m_listParcel:
            print(i[1],i[0])

        # Define the color map for the matrix values
        color_dict = {'C': 'red', 'R': 'grey', 'x': 'green'}  # Rename the dictionary to "color_dict"
        cmap = ListedColormap([color_dict.get(val, 'white') for val in set(np.ravel(matrix))])

        # Convert the matrix to a numerical array
        data = np.zeros((3, 3), dtype=int)
        for i in range(3):
            for j in range(3):
                if matrix[i][j] == 'C':
                    data[i, j] = 3
                elif matrix[i][j] == 'R':
                    data[i, j] = 2
                elif matrix[i][j] == 'x':
                    data[i, j] = 1

        # Plot the matrix
        fig, ax = plt.subplots()
        im = ax.imshow(data, cmap=cmap)

        # Add color bar
        cbar = ax.figure.colorbar(im, ax=ax, ticks=[0, 1, 2])
        cbar.ax.set_yticklabels(['R', 'C', 'P'])

        # Add grid lines
        ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
        ax.set_xticks(np.arange(-0.5, 3.5, 1))
        ax.set_yticks(np.arange(-0.5, 3.5, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Add labels
        for i in range(3):
            for j in range(3):
                ax.text(j, i, matrix[i][j], ha='center', va='center', color='w')

        # Show the plot
        plt.show()