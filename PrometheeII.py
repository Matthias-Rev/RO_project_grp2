import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
# Test matrix,it will be the solution of the Gen Algo
matrix = np.array([[4, 3, 7],
                    [3, 5, 6],
                    [6, 2, 8],
                    [7, 4, 5]])

# Normalisation of the matrix
NormalMatrix = (matrix - matrix.min(axis=0)) / (matrix.max(axis=0) - matrix.min(axis=0))

# Calcul of concordance matrix and discordance matrix
concordance_matrix = np.zeros((matrix.shape[0], matrix.shape[0]))
discordance_matrix = np.zeros((matrix.shape[0], matrix.shape[0]))

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[0]):
        if i != j:
            concordance_i_j = np.sum(NormalMatrix[j] >= NormalMatrix[i]) / matrix.shape[1]
            concordance_matrix[i, j] = concordance_i_j
            discordance_i_j = np.max(NormalMatrix[j] - NormalMatrix[i])
            discordance_matrix[i, j] = discordance_i_j

# Upgrade Id
better_id = np.zeros(matrix.shape[0])

for i in range(matrix.shape[0]):
    somme_concordance_i = np.sum(concordance_matrix[i])
    somme_discordance_i = np.sum(concordance_matrix[i])
    better_id[i] = somme_concordance_i / (somme_concordance_i + somme_discordance_i)

# Definition of the id list of the pareto optimal solution
Pareto_Border = []

for i in range(matrix.shape[0]):
    is_pareto_solution = True
    for j in range(matrix.shape[0]):
        if i != j:
            if better_id[j] > better_id[i]:
                is_pareto_solution = False
                break
    if is_pareto_solution:
        Pareto_Border.append(i)

# Show Graph
    points = []
    for i in Pareto_Border:
        points.append(tuple(matrix[i]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter([p[0] for p in points], [p[1] for p in points], [p[2] for p in points])
plt.show()

