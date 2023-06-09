import numpy as np
import matplotlib.pyplot as plt

# Shift location counterclockwise by partitioning
def Partitionning(listObj):
    AHSortList = []

    minelem = min(listObj, key=returnLine)
    for elem in listObj:
        if returnLine(elem) == returnLine(minelem) and returnCol(elem) < returnCol(minelem):
            minelem = elem

    for elem in listObj:
        if returnCol(elem) > returnCol(minelem):
            AHSortList.append(elem)

    return AHSortList

# Compute compacity & draw
def DrawSurface(listObjA, listObjB, listObjC, draw):
    i=1
    if draw:
        fig, ax = plt.subplots()
    totalSurface = 0
    while i < len(listObjA) -1:

        coords = [listObjA[0], listObjA[i], listObjA[i+1]]

        # Calculation of the area of a triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
        totalSurface += surface

        # Creating the triangle
        if draw:
            plt.Polygon(coords, color='blue', alpha=0.5)
            ax.add_patch(plt.Polygon(coords, color='blue', alpha=0.5))
        i+=1
    i=1
    while i < len(listObjB) -1:

        coords = [listObjB[0], listObjB[i], listObjB[i+1]]

        # Calculation of the area of a triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
        totalSurface += surface

        # Creating the triangle
        if draw:
            plt.Polygon(coords, color='blue', alpha=0.5)
            ax.add_patch(plt.Polygon(coords, color='blue', alpha=0.5))
        i+=1
    i=1
    while i < len(listObjC) -1:

        coords = [listObjC[0], listObjC[i], listObjC[i+1]]

        # Calculation of the area of a triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
        totalSurface += surface

        # Creating the triangle
        if draw:
            plt.Polygon(coords, color='blue', alpha=0.5)
            ax.add_patch(plt.Polygon(coords, color='blue', alpha=0.5))
        i+=1
    # Show triangle
    if draw:
        plt.axis('equal')
        plt.savefig(f"{draw}_compacity.png")
    return totalSurface

# Compute compacity
def returnSurface(listObjA, listObjB, listObjC):
    i=1
    totalSurface = 0
    while i < len(listObjA) -1:

        coords = [listObjA[0], listObjA[i], listObjA[i+1]]

        # Calculation of the area of a triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
        totalSurface += surface

        i+=1
    i=1
    while i < len(listObjB) -1:

        coords = [listObjB[0], listObjB[i], listObjB[i+1]]

        # Calculation of the area of a triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
        totalSurface += surface

        i+=1
    i=1
    while i < len(listObjC) -1:

        coords = [listObjC[0], listObjC[i], listObjC[i+1]]

        # Calculation of the area of a triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(abs(p*(p-a)*(p-b)*(p-c)))
        totalSurface += surface
        i+=1
    plt.close()
    return totalSurface

# return objects in lists
def recoveryCoords(listParcel):
    listCoords = []
    for elem in listParcel:
        listCoords.append(elem.returnPosition())
    return listCoords

def returnCol(objet):
    col = objet[0]
    return col

# Add junction between partitions
def returnJunctionSurface(listObjA, listObjB):
    junctionList = [listObjA[0]]
    if len(listObjA) > 1 and len(listObjB) > 1:
        junctionList.append(listObjA[-1])
        junctionList.append(listObjB[-1])
    elif len(listObjA) == 1:
        junctionList.append(listObjB[-2])
        junctionList.append(listObjB[-1])
        listObjB.remove(listObjB[-1])
    elif len(listObjB) == 1:
        junctionList.append(listObjA[-2])
        junctionList.append(listObjA[-1])
        listObjA.remove(listObjA[-1])
    
    return junctionList

def returnLine(objet):
    line = objet[1]
    return line

# Sort partition'lists by colon
def returnPartialColSort2(listObj, side):
    i=0
    sortList = []
    while i < len(listObj):
        elem = listObj[i]
        trashList = []
        if (elem != listObj[0] and elem != listObj[-1]):
            while i<len(listObj) and returnLine(elem) == returnLine(listObj[i]):
                trashList.append(listObj[i])
                i+=1
            while len(trashList) > 0:
                if (returnLine(elem)!= returnLine(listObj[0])):
                    if side == 'L':
                        sortList.append(min(trashList, key=returnCol))
                        trashList.remove(min(trashList, key=returnCol))
                    elif side == 'R':
                        sortList.append(max(trashList, key=returnCol))
                        trashList.remove(max(trashList, key=returnCol))
                else:
                    if side == 'L':
                        sortList.append(max(trashList, key=returnCol))
                        trashList.remove(max(trashList, key=returnCol))
                    elif side == 'R':
                        sortList.append(min(trashList, key=returnCol))
                        trashList.remove(min(trashList, key=returnCol))
        elif elem == listObj[0]:
            sortList.append(elem)
            i+=1
        elif elem == listObj[-1]:
            sortList.append(elem)
            i+=1
    return sortList

# Define the slope between the reference and a point
def returnSlope(ObjA, ObjB):
    
    if (returnCol(ObjA)-returnCol(ObjB)) != 0:
        slope = abs((returnLine(ObjA)-returnLine(ObjB))/(returnCol(ObjA)-returnCol(ObjB)))/10
        
    elif ObjA == ObjB:
        slope=0
    else:
        slope=1
    return slope

# Sort line by line
def returnSortLineList(listObj):
    lenListObj = len(listObj)
    SortLineList = []
    i=0
    while i < lenListObj:
        sortObj = min(listObj, key = returnLine)
        SortLineList.append(sortObj)
        listObj.remove(sortObj)
        i += 1
    return SortLineList

def returnVisitedPoint(listObj):
    listPoint=[]
    if len(listObj)>1:
        listPoint.append(listObj[0])
    i=1
    while i < len(listObj)-1:
        slopePti=returnSlope(listObj[i], listObj[0])
        slopeSuccesor=returnSlope(listObj[i+1], listObj[0])
        if slopePti <= slopeSuccesor:
            listPoint.append(listObj[i])
            i+=1
        else:
            listObj.remove(listObj[i])
            i-=1
            listPoint.remove(listObj[i])
    if len(listObj)>1:
        listPoint.append(listObj[-1])
    return listPoint

