#Parcel object represent object in the map with associated cost and production
class Parcel:
    def __init__(self, x, y, cost=0):
        self.m_cost = cost
        self.m_prod  = None
        self.m_pos = (x,y)
        self.m_typeElement = None
        self.m_Put = False
    
    def __eq__(self, other):
        return self.m_pos == other.m_pos
    
    def __hash__(self):
        return hash(self.m_pos)

    #If we want change the cost for some reason 
    def changeCost(self, cost):
        self.m_cost = cost
        return 0

    #If we want change the production for some reason 
    def changeProd(self, prod):
        self.m_prod = prod
        return 0
    
    #If we want change the map for some reason 
    def changeTypeElem(self, typeElem):
        self.m_typeElement = typeElem
        return 0

    #Define if a parcel is used
    def parcelPlaced(self, placed=False):
        if placed == True:
            self.m_Put = True
        elif placed == False:
            self.m_Put = False
        return self.m_Put

######## ALL Return function #########
    #return cost of the curent parcel
    def returnCost(self):
        return int(self.m_cost)
    #return prod of the curent parcel
    def returnProd(self):
        return int(self.m_prod)

    #Say what kind of element the object is 
    def returnType(self):
        return self.m_typeElement

    #Return coord's object (x,y => c,l)
    def returnPosition(self):
        return self.m_pos
    
    # return j (=>col)
    def returnColPosition(self):
        return self.m_pos[0]
    
    # return i (=>line)
    def returnLinePosition(self):
        return self.m_pos[1]
    
    # define if a parcel is already take
    def returnPutState(self):
        return self.m_Put

    
