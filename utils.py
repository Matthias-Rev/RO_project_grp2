from parcel import Parcel
from map import Map

costfile = "./donnes_V2/Cost_map.txt"
prodfile = "./donnes_V2/Production_map.txt"
mapfile = "./donnes_V2/Usage_map.txt"

Parcel_listParcel = []
matrix = []

# read costfile and prodfile
def readFile(f):
    try:
        with open(f, "r") as file:
            line = file.readline()
            index = 0        # index in Parcel_listParcel
            while line:
                    lineMatrix = []
                    element = file.read(1)
                    for element in line.strip():
                        if f == costfile :
                            Parcel_listParcel.append(Parcel(int(element)))
                        elif f == prodfile :
                            parcel = Parcel_listParcel[index]
                            parcel.changeProd(int(element))
                            lineMatrix.append(parcel)
                            index += 1
                        elif f == mapfile:
                            lineMatrix.append(element)
                    line = file.readline()
                    if f == prodfile:
                        matrix.append(lineMatrix)
                    elif f == mapfile:
                        map.append(lineMatrix)
                
    except FileNotFoundError:
        if f == costfile:
            print("Error : prodfile_path wrong")
        elif f == prodfile:
            print("Error : costfile_path wrong")
        elif f == mapfile:
            print("Error : mapfile_path wrong")

def readMapFile(f):
    try:
        with open(f, "r") as file:
            map = []
            line = file.readline()
            index = 0        # index in Parcel_listParcel
            while line:
                    lineMatrix = []
                    element = file.read(1)
                    for element in line.strip():
                        if f == mapfile:
                            lineMatrix.append(element)
                    line = file.readline()
                    if f == mapfile:
                        map.append(lineMatrix)
            return map

                
    except FileNotFoundError:
        if f == mapfile:
            print("Error : mapfile_path wrong")
    
def returnMatrix():
    readFile(costfile)
    readFile(prodfile)
    return matrix
    
# readFile(costfile)
# readFile(prodfile)

# matrrixA = returnMatrix()
# el = matrrixA[0][0]

# # print(el)

# mapp = Map(readMapFile(mapfile))

# mapp.printRoads(1)

# mapRoad = mapp.returnRoads()
# print(mapRoad[1][3])

# print(len(mapp))
# print(len(map))
# print(len(map[0]))
