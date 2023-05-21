from parcel import Parcel
from map import Map
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

costfile = "./donnes_V2/Cost_map.txt"
prodfile = "./donnes_V2/Production_map.txt"
mapfile = "./donnes_V2/Usage_map.txt"

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

# read data of given  mapfile
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

# construct map's object
def constructMap():
    Parcel_listParcel = []
    costDic = {}
    readFile(costfile)
    readFile(prodfile)
    return readMapFile(mapfile)

# return number of parcel on the map
def returnNbParcel():
    return len(Parcel_listParcel)

# identify how much parcel with cost n
def costParcelDic(cost):
    if cost in costDic.keys():
        costDic[cost] +=1
    else:
        costDic[cost] = 1

# creat pareto frontier
def plot_pareto_frontier(points, pareto_indices):
    pareto_points = points[pareto_indices]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pareto_points[:, 0], pareto_points[:, 1], pareto_points[:, 2], c='red', label='Frontière de Pareto')
    ax.set_xlabel('Compacity')
    ax.set_ylabel('Production')
    ax.set_zlabel('Habitation Dist')

    # Changer l'échelle des axes
    ax.set_ylim(0, 100)

    plt.legend()
    plt.show()
    #plt.savefig("./result/pareto.png")



def find_pareto_frontier_indices(points):
    num_points = points.shape[0]
    is_pareto_efficient = np.ones(num_points, dtype=bool)

    for i in range(num_points):
        if is_pareto_efficient[i]:
            current_point = points[i]
            is_pareto_efficient[is_pareto_efficient] = np.any(points[is_pareto_efficient] >= current_point, axis=1)

    pareto_indices = np.where(is_pareto_efficient)[0]
    return pareto_indices

