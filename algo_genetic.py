import random 
import math

class Individual_algo_genetic:

    def __init__(self, m_map_parcel, map):
        self.m_map_parcel = m_map_parcel
        self.m_map_production = 0 #m_map_production
        self.m_map_cost = 0 #m_map_cost
        self.m_map = map
        self.m_totalCost = 0                        #must be <500.000
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"
    
    def showMatrix(self):
        return self.m_map.returnGrid()
    
    #define the compacity
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel
    
    #define the first candidate where we put the first parcel
    def chooseFirstCandidate(self):
        candidateOk = False
        while not candidateOk:
            i = random.randint(0, len(self.m_map.returnGrid())-1)
            j = random.randint(0, len(self.m_map.returnGrid()[i])-1)
            if self.m_map.returnGrid()[i][j] == ' ':
                candidateOk = True
                print("position : ",i,j)
                # #for element in self.m_map.m_roads_pos:
                # #posNearestObj = min(abs(self.m_map.m_roads_pos[i]-(i,j)))
                # #posNearestObj = min(self.m_map.m_roads_pos, key=lambda pos: ((pos[0] - i) ** 2 + (pos[1] - j) ** 2) ** 0.5)

                # # Calcul de la distance entre deux positions représentées par des tuples
                # pos1 = self.m_map.m_roads_pos[i]
                # pos2 = (i, j)
                # #distance = math.dist(pos1, pos2)
                # # Trouver la position de l'objet le plus proche
                # #posNearestObj = min(self.m_map.m_roads_pos, key=lambda pos: math.dist(pos, (i, j)))


                # #print(f"posMax = {posNearestObj}")
                # self.objectDistance((i,j), self.m_map.returnRoads()[i][0], i)
    
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
                
            








        
