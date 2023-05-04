import numpy as np
import matplotlib.pyplot as plt

def recoveryCoords(listParcel):
    listCoords = []
    #print(listParcel)
    for elem in listParcel:
        listCoords.append(elem.returnPosition())
    return listCoords

def returnLine(objet):
    line = objet[1]
    return line

def returnCol(objet):
    col = objet[0]
    return col

def Partitionning(listObj):
    AHSortList = []
    for elem in listObj:
        if returnCol(elem) > returnCol(min(listObj, key=returnLine)):
            AHSortList.append(elem)

    return AHSortList

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
    listPoint=[listObj[0]]
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
    listPoint.append(listObj[-1])
    return listPoint

def returnSlope(ObjA, ObjB):
    
    if (returnCol(ObjA)-returnCol(ObjB)) != 0:
        slope = abs((returnLine(ObjA)-returnLine(ObjB))/(returnCol(ObjA)-returnCol(ObjB)))/10
        
    elif ObjA == ObjB:
        slope=0
    else:
        slope=1
    return slope

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

def returnSurface(listObjA, listObjB):
    i=1
    #fig, ax = plt.subplots()
    totalSurface = 0
    while i < len(listObjA) -1:

        coords = [listObjA[0], listObjA[i], listObjA[i+1]]

        # Calcul de l'aire du triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(p*(p-a)*(p-b)*(p-c))
        totalSurface += surface

        # Création du triangle
        plt.Polygon(coords, color='blue', alpha=0.5)
        #ax.add_patch(plt.Polygon(coords, color='blue', alpha=0.5))
        i+=1
    i=1
    while i < len(listObjB) -1:

        coords = [listObjB[0], listObjB[i], listObjB[i+1]]

        # Calcul de l'aire du triangle
        a = np.linalg.norm(np.array(coords[0]) - np.array(coords[1]))
        b = np.linalg.norm(np.array(coords[1]) - np.array(coords[2]))
        c = np.linalg.norm(np.array(coords[2]) - np.array(coords[0]))
        p = (a+b+c)/2
        surface = np.sqrt(p*(p-a)*(p-b)*(p-c))
        totalSurface += surface

        # Création du triangle
        plt.Polygon(coords, color='blue', alpha=0.5)
        #ax.add_patch(plt.Polygon(coords, color='blue', alpha=0.5))
        i+=1
    #plt.close()
    # Affichage du triangle
    # plt.axis('equal')
    # plt.show()
    # print("la surface totale est de :", totalSurface)
    return totalSurface
