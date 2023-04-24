class Map:
    def __init__(self, map):
        self.m_grid = map
        self.m_roads_pos = []
        self.m_roads_Colpos = {}
        self.m_houses_pos = []
        self.m_houses_Colpos = {}

        self.posInit()

    def posInit(self):
        j = 0
        for line in self.m_grid:
            i=0
            lineRoads = []
            lineHouses = []
            for element in line:
                if element == "R":
                    lineRoads.append((j,i))
                    #if i not in dico_
                elif element == "C":
                    lineHouses.append((j,i))
                i += 1
            j +=1

            self.m_roads_pos.append(lineRoads)
            self.m_houses_pos.append(lineHouses)

    def printRoads(self, i=0, j=0):
        print(self.m_roads_pos[i])
    
    def printHouses(self, i=0, j=0):
        print(self.m_houses_pos[i])

    def returnGrid(self):
        return self.m_grid
    
    def returnRoads(self):
        return self.m_roads_pos

    def returnHouses(self):
        return self.m_houses_pos
    
    def changeGrid(self, tuple, char):
        i = tuple[0]
        j = tuple[1]
        self.m_grid[i][j] = char
        return 0