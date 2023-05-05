class Parcel:
    def __init__(self, x, y, cost=0):
        self.m_cost = cost
        self.m_prod  = None
        self.m_pos = (x,y)
        self.m_typeElement = None
        self.m_Put = False

    def changeCost(self, cost):
        self.m_cost = cost
        return 0

    def changeProd(self, prod):
        self.m_prod = prod
        return 0
    
    def changeTypeElem(self, typeElem):
        self.m_typeElement = typeElem
        return 0

    def returnCost(self):
        return int(self.m_cost)
    
    def returnProd(self):
        return int(self.m_prod)
    
    def returnType(self):
        return self.m_typeElement
    
    def parcelPlaced(self, placed=False):
        if placed == True:
            self.m_Put = True
        elif placed == False:
            self.m_Put = False
        return self.m_Put
    
    def returnPosition(self):
        return self.m_pos
    
    def returnColPosition(self):
        return self.m_pos[0]
    
    def returnLinePosition(self):
        return self.m_pos[1]
    
    def returnColPosition(self):
        return self.m_pos[0]