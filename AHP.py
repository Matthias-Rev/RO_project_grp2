import math

criteria = ["Production", "Compacité", "DistancesHabitation"]

importance12 = 3
importance13 = 5
importance23 = 3
importanceList = []
comparisonMatrix = [[1,importance12, importance13],
                     [1/importance12,1,importance23],
                     [1/importance13, 1/importance23, 1]]

Matrix = []
# i=0
# while i < len(criteria):
#     Matrix[i][i]=1
#     j=0
#     while j < len(criteria):
#         if i == j:    
#             Matrix[i][i]=1
#         else:
#             Matrix[i][j]=importanceList[j]
#             Matrix[i][j]=1/importanceList[j]

listSum = []
listWeigths = []
i = 0
while i < len(criteria):
    j = 0
    sumcol=0
    while j < len(criteria):
        sumcol += comparisonMatrix[j][i]
        j += 1
    listSum.append(sumcol)
    k=0
    while k < len(criteria):
        comparisonMatrix[k][i] /= sumcol
        k += 1

    i+=1

i = 0
while i < len(criteria):
    l=0
    sumline=0
    while l < len(criteria):
        sumline += comparisonMatrix[i][l]
        l+=1
    listWeigths.append(sumline/len(criteria))
    i += 1

i = 0
while i < len(criteria):
    print(f"valeur du poids {criteria[i]} = {listWeigths[i]}")
    i+=1


print(listWeigths[0]+listWeigths[1]+listWeigths[2])