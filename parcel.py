class Parcel:
    def __init__(self, cost=0, prod=0):
        self.m_cost = cost
        self.m_prod  = prod
        self.m_Put = False

    def changeCost(self, cost):
        self.m_cost = cost

    def changeProd(self, prod):
        self.m_prod = prod

    def returnCost(self):
        return int(self.m_cost)
    
    def returnProd(self):
        return int(self.m_prod)
    
    def parcelPlaced(self, placed=False):
        if placed == True:
            self.m_Put = True
        return self.m_Put