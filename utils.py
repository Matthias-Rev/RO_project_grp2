from parcel import Parcel
from map import Map

costfile = "./donnes_V3/Cost_map.txt"
prodfile = "./donnes_V3/Production_map.txt"
mapfile = "./donnes_V3/Usage_map.txt"
#mapfile = "./donnes_V2/Map2.txt"

Parcel_listParcel = []
costDic = {}

# read costfile and prodfile
def readFile(f):
    try:
        with open(f, "r") as file:
            line = file.readline()
            index = 0
            colindex = 0        # index in Parcel_listParcel
            lineIndex = 0
            while line:
                    lineMatrix = []
                    for element in line.strip('\n'):
                        if f == costfile :
                            Parcel_listParcel.append(Parcel(colindex, lineIndex, int(element)))
                            costParcelDic(element)
                            colindex += 1
                        elif f == prodfile :
                            parcel =  Parcel_listParcel[index]
                            parcel.changeProd(int(element))
                            lineMatrix.append(parcel)
                            index += 1
                    colindex = 0
                    lineIndex += 1
                    line = file.readline()
                    
    except FileNotFoundError:
        if f == costfile:
            print("Error : prodfile_path wrong")
        elif f == prodfile:
            print("Error : costfile_path wrong")

def readMapFile(f):
    try:
        with open(f, "r") as file:
            map = []
            line = file.readline()
            index = 0
            while line:
                    lineMatrix = []
                    for element in line.strip('\n'):
                        if f == mapfile:
                            parcel =  Parcel_listParcel[index]
                            parcel.changeTypeElem(element)
                            lineMatrix.append(parcel)
                            index += 1
                    line = file.readline()
                    if f == mapfile:
                        map.append(lineMatrix)
            return map

                
    except FileNotFoundError:
        if f == mapfile:
            print("Error : mapfile_path wrong")
    
def constructMap():
    Parcel_listParcel = []
    costDic = {}
    readFile(costfile)
    readFile(prodfile)
    return readMapFile(mapfile)

def returnNbParcel():
    return len(Parcel_listParcel)

def costParcelDic(cost):
    if cost in costDic.keys():
        costDic[cost] +=1
    else:
        costDic[cost] = 1

