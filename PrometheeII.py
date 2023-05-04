
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np


# class PrometheeII:

#     def __init__(self, matrix):

#         self.matrix = np.array(matrix)
#         self.normal_matrix = None
#         self.concordance_matrix = None
#         self.discordance_matrix = None
#         self.better_id = None
#         self.pareto_border = None
        
#     def build_matrix(self, instances):
#         self.matrix = np.array([[p.returnM_totalComp(), p.returnM_totalComp(), p.return_m_minDistHabitation()] for p in instances])
#         return self.matrix

#     def normalize_matrix(self):
#         self.normal_matrix = (self.matrix - self.matrix.min(axis=0)) / (
#                     self.matrix.max(axis=0) - self.matrix.min(axis=0))

#     def calculate_concordance_and_discordance_matrices(self):
#         self.concordance_matrix = np.zeros((self.matrix.shape[0], self.matrix.shape[0]))
#         self.discordance_matrix = np.zeros((self.matrix.shape[0], self.matrix.shape[0]))
#         for i in range(self.matrix.shape[0]-1):
#             for j in range(self.matrix.shape[0]-1):
#                 if i != j:
#                     concordance_i_j = np.sum(self.normal_matrix[j] >= self.normal_matrix[i]) / self.matrix.shape[1]
#                     self.concordance_matrix[i, j] = concordance_i_j
#                     discordance_i_j = np.max(self.normal_matrix[j] - self.normal_matrix[i])
#                     self.discordance_matrix[i, j] = discordance_i_j

#     def upgrade_id(self):
#         self.better_id = np.zeros(self.matrix.shape[0])
#         for i in range(self.matrix.shape[0]-1):
#             #print(self.concordance_matrix[i])
#             somme_concordance_i = np.sum(self.concordance_matrix[i])
#             somme_discordance_i = np.sum(self.discordance_matrix[i])
#             #print(somme_concordance_i + somme_discordance_i)
#             self.better_id[i] = somme_concordance_i / (somme_concordance_i + somme_discordance_i)

#     def find_pareto_border(self):
#         self.pareto_border = []
#         for i in range(self.matrix.shape[0]):
#             is_pareto_solution = True
#             for j in range(self.matrix.shape[0]):
#                 if i != j:
#                     if self.better_id[j] > self.better_id[i]:
#                         is_pareto_solution = False
#                         break
#             if is_pareto_solution:
#                 self.pareto_border.append(i)

#     def show_3d_graph(self):
#         points = []
#         for i in self.pareto_border:
#             points.append(tuple(self.matrix[i]))
#         print(points,"point")
#         fig = plt.figure()
#         ax = fig.add_subplot(111, projection='3d')
#         ax.scatter([p[0] for p in points], [p[1] for p in points],[p[2] for p in points]) #, [p[2] for p in points]
#         plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class PrometheeII:
    def __init__(self, matrix, weights):
        self.matrix = np.array(matrix)
        self.weights = np.array(weights)
        self.n, self.m = matrix.shape
        self.p = 0.6
        self.q = 0.4

    def _calculate_p(self):
        self.p = np.zeros((self.m, self.m))
        for i in range(self.m):
            for j in range(self.m):
                if i != j:
                    sump = 0
                    for k in range(self.n):
                        sump += np.sign(self.matrix[k][j] - self.matrix[k][i]) * self.weights[k]
                    self.p[i][j] = sump / self.n

    def _calculate_q(self):
        self.q = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    sumq = 0
                    for k in range(self.m):
                        sumq += np.sign(self.matrix[i][k] - self.matrix[j][k]) * self.weights[k]
                    self.q[i][j] = sumq

    def calculate_rankings(self):
        self._calculate_p()
        self._calculate_q()
        rankings = np.zeros(self.n)
        for i in range(self.n):
            sumrank = 0
            for j in range(self.n):
                if i != j:
                    sumrank += self.q[i][j] - self.q[j][i]
            rankings[i] = sumrank
        return rankings

    def find_pareto_border(self):
        self.pareto_border = []
        for i in range(self.n):
            dominated = False
            for j in range(self.n):
                if all(self.matrix[j] >= self.matrix[i]) and any(self.matrix[j] > self.matrix[i]):
                    dominated = True
                    break
            if not dominated:
                self.pareto_border.append(i)
        return self.pareto_border
    
    def show_3d_graph(self):
        points = []
        for i in self.pareto_border:
            points.append(tuple(self.matrix[i]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter([p[0] for p in points], [p[1] for p in points], [p[2] for p in points])
        plt.show()