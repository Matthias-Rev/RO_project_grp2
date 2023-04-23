import random 
import math
import numpy as np
import matplotlib.pyplot as plt
#from matplotlib import colors
from matplotlib.colors import ListedColormap

class Individual_algo_genetic:

    def __init__(self, m_map_parcel, map ,parcel_list=[]):
        #self.m_nb_parcel = nbr_parcel
        self.m_map_parcel = m_map_parcel
        self.m_map_production = 0 #m_map_production
        self.m_map_cost = 0 #m_map_cost
        self.m_map = map
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        self.m_listParcel = parcel_list
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"

        self.m_parcels_placed = []
    
    def showMatrix(self):
        return self.m_map.returnGrid()

    def returnM_totalCost(self):
        return self.m_totalCost
    
    def returnM_totalProd(self):
        return self.m_totalProd
    
    def returnNbParcel(self):
        return self.m_nb_parcel

    def changeParcel(self, new_parcel):
        self.m_listParcel = new_parcel
    
    #define the compacity
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel
    
    #define the first candidate where we put the first parcel
    def chooseFirstCandidate(self):
        candidateOk = False
        while not candidateOk:
            i = random.randint(0, len(self.m_map.returnGrid())-1)
            j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
            if self.m_map.returnGrid()[i][j] == ' ' and self.putParcel():
                candidateOk = True
                print("position : ",i,j)
    
    #create our individual
    def chooseCandidate(self):
        while self.m_totalCost < 20: #change here and self.returnNbParcel()>0
            candidateOk = False
            while not candidateOk:
                print(len(self.m_map.returnGrid()))
                i = random.randint(0, len(self.m_map.returnGrid())-1)
                print(len(self.m_map.returnGrid()[i]),"autre")
                j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
                randomCandidate = self.m_map.returnGrid()[i][j]
                if randomCandidate == ' ' and self.putParcel():
                    candidateOk = True
                    self.m_map.changeGrid((i,j), 'x')
                    candidate = (i,j)
                    self.m_listParcel.append(candidate)
        #print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        return self.m_listParcel

    #define if a parcel is checked
    def putParcel(self):
        parcelOk = False
        while not parcelOk:
            i = random.randint(0, len(self.m_map_parcel)-1)
            j = random.randint(0, len(self.m_map_parcel[i])-1)
            randomParcel = self.m_map_parcel[i][j]
            #peut rentrer dans une boucle infinie => 500+1 (ou : self.m_totalCost < 499)
            if not randomParcel.parcelPlaced() and ((randomParcel.returnCost()+self.m_totalCost)<=500):
                # print("cost = ", randomParcel.returnCost()+self.m_totalCost)
                # if randomParcel.returnCost()+self.m_totalCost <= 500:
                randomParcel.parcelPlaced(True)
                parcelOk = True
                self.m_totalCost += randomParcel.returnCost()
                self.m_totalProd += randomParcel.returnProd()
                #self.m_nb_parcel -= 1
        return True 

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
        matrix = self.m_map.returnGrid()
    #     print(matrix)
    #     for i in self.m_listParcel:
    #         print(i[1],i[0])

        cmap = ListedColormap(['grey', 'red', 'green'])
        matrix_norm = [[-1 if j == ' ' else 0 if j == 'R' else 1 if j == 'C' else 2 if j == 'P' else j for j in i] for i in matrix]
        matrix_color = cmap(matrix_norm)

        # Create the plot
        fig, ax = plt.subplots()
        ax.imshow(matrix_color)

        # Customize the ticks
        ax.set_xticks(np.arange(len(matrix[0])))
        ax.set_yticks(np.arange(len(matrix)))
        ax.set_xticklabels(['' if i == ' ' else i for i in matrix[0]])
        ax.set_yticklabels(['' if i == ' ' else i for i in [row[0] for row in matrix]])

        # Add the values to the cells
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] != ' ':
                    ax.text(j, i, matrix[i][j], ha="center", va="center", color="w")

        # Add the grid lines
        ax.grid(which="major", color="k", linestyle='-', linewidth=2)
        ax.tick_params(size=0)

        # Show the plot
        plt.show()
    # def draw_matrix(self):
    #     # Define the matrix
    #     matrix = self.m_map.returnGrid()
    #     print(matrix)
    #     for i in self.m_listParcel:
    #         print(i[1],i[0])

    #     # Define the color map for the matrix values
    #     color_dict = {'C': 'red', 'R': 'grey', 'x': 'green'}  # Rename the dictionary to "color_dict"
    #     cmap = colors.ListedColormap([color_dict.get(val, 'white') for val in set(np.ravel(matrix))])

    #     # Convert the matrix to a numerical array
    #     data = np.zeros((3, 3), dtype=int)
    #     for i in range(3):
    #         for j in range(3):
    #             if matrix[i][j] == 'C':
    #                 data[i, j] = 3
    #             elif matrix[i][j] == 'R':
    #                 data[i, j] = 2
    #             elif matrix[i][j] == 'x':
    #                 data[i, j] = 1

    #     # Plot the matrix
    #     fig, ax = plt.subplots()
    #     im = ax.imshow(data, cmap=cmap)

    #     # Add color bar
    #     cbar = ax.figure.colorbar(im, ax=ax, ticks=[0, 1, 2])
    #     cbar.ax.set_yticklabels(['R', 'C', 'P'])

    #     # Add grid lines
    #     ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    #     ax.set_xticks(np.arange(-0.5, 3.5, 1))
    #     ax.set_yticks(np.arange(-0.5, 3.5, 1))
    #     ax.set_xticklabels([])
    #     ax.set_yticklabels([])

    #     # Add labels
    #     for i in range(3):
    #         for j in range(3):
    #             ax.text(j, i, matrix[i][j], ha='center', va='center', color='w')

    #     # Show the plot
    #     plt.show()