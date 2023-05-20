import numpy as np

#Map object correspond to the given file of the representation map
class Map:
    def __init__(self, grid, dictionnary):
        self.m_grid = grid
        self.m_roads_pos = []
        self.m_roads_Colpos = {}
        self.m_houses_pos = []
        self.m_houses_Colpos = {}
        self.m_heigth = len(grid)
        self.m_width = len(grid[0])

        self.m_cost = 0
        self.m_prod  = 0
        self.m_Put = False

        self.m_costDic = dictionnary

        self.m_total_area = self.m_heigth*self.m_width

        self.posInit()

    #Change the map's position with the choose character
    def changeGrid(self, coord, char):
        i = coord[0]
        j = coord[1]
        self.m_grid[i][j] = char
        return 0

    def write_solution(self,list_pos,name):
        for i in list_pos:
            pos=i.returnPosition()
            self.m_grid[pos[1]][pos[0]].changeTypeElem("x")
        with open(f"{name}_solut.txt", "w") as file:
            for element in self.m_grid:
                for parcel in element:
                    file.write(parcel.returnType())
                file.write("\n")

    #List the position of roads & habitation   
    def posInit(self):
        j = 0
        for line in self.m_grid:
            i=0
            lineRoads = []
            lineHouses = []
            for element in line:
                if element.returnType() == "R":
                    lineRoads.append((j,i))
                elif element.returnType() == "C":
                    lineHouses.append((j,i))
                i += 1
            j +=1

            if len(lineRoads) > 0:
                self.m_roads_pos.append(lineRoads)
            if len(lineHouses) > 0:
                self.m_houses_pos.append(lineHouses)

    def printRoads(self, i=0, j=0):
        print(self.m_roads_pos[i])
        return 0
    
    def printHouses(self, i=0, j=0):
        print(self.m_houses_pos[i])
        return 0
    
    #return Map's width 
    def returnWidth(self):
        return self.m_width
    
    #return Map's heigth
    def returnHeigth(self):
        return self.m_heigth
    
    #return Map'sArea
    def returnTotalArea(self):
        return self.m_total_area
    
    #return Dictionary in wich are all maps'parcels not used
    def returnDic(self):
        return self.m_costDic
    
    def restoreDic(self, initialDic):
        self.m_costDic = initialDic
        return 0

    def returnCostDic(self):
        return self.costDic
    
    #return objet wich have the coord i,j (y,x => l,col)
    def returnObject(self, i,j):
        return self.m_grid[i][j]

    def returnGrid(self):
        return self.m_grid
    
    def returnRoads(self):
        return self.m_roads_pos

    def returnHouses(self):
        return self.m_houses_pos
    
