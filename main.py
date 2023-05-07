import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *
import numpy as nps
from mpl_toolkits.mplot3d import Axes3D

Instance_Map=Map(constructMap(), costDic)


def build_matrix(instances):
    matrix = np.array([[p.return_totalComp(),p.return_minDistHabitation(), p.return_totalProd()] for p in instances])
    return matrix

test = Algo_genetic(1,10,0.80,0.99,Instance_Map)
liste_pop =test.genetic_algorithm()

weights = [1, 1, 1]
matrix = build_matrix(liste_pop)
promethe = PrometheeII(matrix,weights)
promethe.find_pareto_border()
points = []
for i in range(0,len(liste_pop)-1):
    points.append(tuple(matrix[i]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter([p[0] for p in points], [p[1] for p in points], [p[2] for p in points])
ax.set_xlabel("Compacity")
ax.set_ylabel("Distance")
plt.show()

def obj_func_1(x, y, z):
    return x + y + z

def obj_func_2(x, y, z):
    return 1 / (1 + x**2 + y**2 + z**2)

# Calculating the objective function values for the sample data
print(liste_pop[:, 0])
obj_1_values = obj_func_1(liste_pop[:, 0], liste_pop[:, 1], liste_pop[:, 2])
obj_2_values = obj_func_2(liste_pop[:, 0], liste_pop[:, 1], liste_pop[:, 2])

# Finding the Pareto frontier using numpy
pareto_mask = np.ones_like(obj_1_values, dtype=bool)
for i, (obj_1, obj_2) in enumerate(zip(obj_1_values, obj_2_values)):
    if pareto_mask[i]:
        pareto_mask[pareto_mask] = np.logical_or(
            obj_1_values[pareto_mask] > obj_1,
            obj_2_values[pareto_mask] > obj_2
        )
        pareto_mask[i] = True

# Plotting the Pareto frontier using Matplotlib
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(liste_pop[:, 0], liste_pop[:, 1], liste_pop[:, 2], c=obj_1_values, cmap='viridis')
ax.scatter(liste_pop[pareto_mask, 0], liste_pop[pareto_mask, 1], liste_pop[pareto_mask, 2], c=obj_1_values[pareto_mask], cmap='viridis', edgecolors='r', linewidths=2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
plt.show()
