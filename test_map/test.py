
def readFile(f):
    with open(f, "r") as file:
        line = file.readline()
        index = 0
        colindex = 0        # index in Parcel_listParcel
        lineIndex = 0
        list_parcel = []
        while line:
                lineMatrix = []
                for element in line.strip('\n'):
                    if element == "x":
                        list_parcel.append([lineIndex,colindex])
                    colindex += 1
                colindex = 0
                lineIndex += 1
                line = file.readline()
    return list_parcel


print(readFile("./test_20000_7_13_52_53_solut.txt"))