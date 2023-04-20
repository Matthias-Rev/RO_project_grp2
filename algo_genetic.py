class Individual_algo_genetic:

    def __init__(self, m_map_cost, m_map_production, map):
        self.m_map_production = m_map_production
        self.m_map_cost = m_map_cost
        self.m_map = map
        self.m_totalCost = 0
        self.m_totalProd = 0
        self.m_totalCompacity = 0
        #distance entre les zones habitées
        #compacité ???? -> surface d'une "nasse"
    
    def showMatrix(self):
        return self.m_map
    
    def readFileMatrixCost(self,file_name):
        self.m_map = []
        with open(file_name, 'r') as f:
            ligne = f.readline()
            while ligne:
                ligne_matrice = []
                for caractere in ligne.strip():
                    if caractere.isdigit():
                        ligne_matrice.append(int(caractere))
                if ligne_matrice:
                    self.m_map.append(ligne_matrice)
                ligne = f.readline()
            
    def coefCompact(self, highestNasse, allParcel):
        return highestNasse/allParcel

        
