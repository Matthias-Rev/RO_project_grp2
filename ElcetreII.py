import numpy as np
from multiprocessing import Pool

class ELECTRE:
    def __init__(self, weights, concordance_index, discordance_index):
        self.weights = weights
        self.concordance_index = concordance_index
        self.discordance_index = discordance_index


    def normalization(self,score_matrix):
        normalized_scores = np.zeros_like(score_matrix)
        for i in range(score_matrix.shape[1]):
            normalized_scores[:,i] = (score_matrix[:,i] - np.min(score_matrix[:,i])) / (np.max(score_matrix[:,i]) - np.min(score_matrix[:,i]))
        return  normalized_scores

    def calculate_concordance(self, score_matrix, normalized_scores):
        concordance_matrix = np.zeros((score_matrix.shape[0], score_matrix.shape[0]))
        for i in range(score_matrix.shape[0]):
            diff_matrix = normalized_scores[i, :] - normalized_scores
            concordance_matrix[i, :] = np.sum((diff_matrix >= 0) * self.weights, axis=1)
        return concordance_matrix

    def calculate_discordance(self, score_matrix, normalized_scores):
        discordance_matrix = np.zeros((score_matrix.shape[0], score_matrix.shape[0]))
        for i in range(score_matrix.shape[0]):
            diff_matrix = normalized_scores - normalized_scores[i, :]
            discordance_matrix[i, :] = np.max((diff_matrix * self.weights), axis=1)
        return discordance_matrix

    def calculate_net_flow(self,score_matrix):
        normal_matrix = self.normalization(score_matrix)
        concordance_matrix = self.calculate_concordance(score_matrix,normal_matrix)
        discordance_matrix = self.calculate_discordance(score_matrix,normal_matrix)
        net_flow = np.zeros((score_matrix.shape[0],))
        for i in range(score_matrix.shape[0]):
            net_flow[i] = sum([self.concordance_index * concordance_matrix[i][j] - self.discordance_index * discordance_matrix[i][j] for j in range(score_matrix.shape[0])])
        return net_flow

    def rank_solutions(self,score_matrix):
        print("begin electree")
        net_flow = self.calculate_net_flow(score_matrix)
        ranking = np.argsort(-net_flow)
        print("end electree")
        return ranking

    def build_matrix(self,instances):
        matrix = np.array([[p.returnM_totalComp(), p.returnM_totalProd(), p.return_m_minDistHabitation()] for p in instances])
        return matrix

    def pareto_frontier(self,matrix):
        print("begin pareto")
        # Triez la matrice par ordre décroissant de la deuxième colonne
        matrix = np.multiply(matrix,np.array([-1,1,-1]))
        matrix = matrix[np.argsort(-matrix[:, 1])]

        # Initialisez une liste pour stocker les points de la frontière de Pareto
        pareto_points = [matrix[0]]

        # Parcourez la matrice, en ajoutant les points à la liste si ils sont sur la frontière de Pareto
        for i in range(1, matrix.shape[0]):
            if matrix[i, 2] <= pareto_points[-1][2]:
                pareto_points.append(matrix[i])

        # Convertissez la liste des points en une matrice numpy
        pareto_frontier = np.array(pareto_points)
        pareto_frontier = np.multiply(pareto_frontier,np.array([-1,1,-1]))

        return pareto_frontier