import random 
import copy

class Individual_algo_genetic:

    def __init__(self, map):
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
                    listParcel.append(randomCandidate)
        #print(self.m_map.returnGrid())
        print(f"valeur production = {self.m_totalProd}, valeur cout = {self.m_totalCost}")
        self.cleanIndividual(listParcel, restoreDic)
        return listParcel

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
                
            








        
