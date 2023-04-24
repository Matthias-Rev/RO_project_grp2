import random 
import math
import utils 
class Individual_algo_genetic:

    def __init__(self, m_map_parcel, map, nbParcel):
        self.m_nb_parcel = nbParcel
        self.m_map_parcel = m_map_parcel
        self.m_map = map
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"

        self.m_parcels_placed = []
    
    def showMatrix(self):
        return self.m_map.returnGrid()
    
    def returnNbParcel(self):
        return self.m_nb_parcel
    
    #define the compacity
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel
    
    #create our individual
    def chooseCandidate(self):
        listParcel = []
        while self.m_totalCost+int(next(iter(utils.costDic))) <= 50:
            candidateOk = False
            while not candidateOk:
                i = random.randint(0, len(self.m_map.returnGrid())-1)
                j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
                randomCandidate = self.m_map.returnGrid()[i][j]
                if randomCandidate == ' ' and self.putParcel():
                    candidateOk = True
                    self.m_map.changeGrid((i,j), 'x')
                    candidate = (i,j)
                    listParcel.append(candidate)
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        return listParcel

    #define if a parcel is checked
    def putParcel(self):
        parcelOk = False
        while not parcelOk:
            randomParcel = 0
            i = random.randint(0, len(self.m_map_parcel)-1)
            j = random.randint(0, len(self.m_map_parcel[i])-1)
            randomParcel = self.m_map_parcel[i][j]
            if not randomParcel.parcelPlaced() and ((randomParcel.returnCost()+self.m_totalCost)<=50):
                self.m_map_parcel[i][j].parcelPlaced(True)
                utils.costDic[str(randomParcel.returnCost())] -=1
                if utils.costDic[str(randomParcel.returnCost())] == 0:
                    print("mort de la clé:", utils.costDic[str(randomParcel.returnCost())])
                    utils.costDic.pop(randomParcel.returnCost())
                parcelOk = True
                self.m_totalCost += randomParcel.returnCost()
                self.m_totalProd += randomParcel.returnProd()
                self.m_nb_parcel -= 1
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
                
            








        
