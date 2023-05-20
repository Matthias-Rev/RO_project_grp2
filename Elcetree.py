import numpy as np

class ELECTREE:
    def __init__(self, weights, concordance_index, discordance_index):
        # Constructor to initialize weights, concordance index, and discordance index
        self.weights = weights
        self.concordance_index = concordance_index
        self.discordance_index = discordance_index


    def normalization(self,score_matrix):
        # Method to normalize the score matrix
        normalized_scores = np.zeros_like(score_matrix)
        for i in range(score_matrix.shape[1]):
            normalized_scores[:,i] = (score_matrix[:,i] - np.min(score_matrix[:,i])) / (np.max(score_matrix[:,i]) - np.min(score_matrix[:,i]))
        return  normalized_scores

    def calculate_concordance(self,score_matrix,normalized_scores):
        # Method to calculate the concordance matrix
        concordance_matrix = np.zeros((score_matrix.shape[0], score_matrix.shape[0]))
        for i in range(score_matrix.shape[0]):
            for j in range(score_matrix.shape[0]):
                if i == j:
                    continue
                concordance_matrix[i][j] = sum([self.weights[k] * (normalized_scores[i][k] >= normalized_scores[j][k]) for k in range(score_matrix.shape[1])])
        return concordance_matrix

    def calculate_discordance(self,score_matrix,normalized_scores):
        # Method to calculate the discordance matrix
        discordance_matrix = np.zeros((score_matrix.shape[0], score_matrix.shape[0]))
        for i in range(score_matrix.shape[0]):
            for j in range(score_matrix.shape[0]):
                if i == j:
                    continue
                discordance_matrix[i][j] = sum([self.weights[k] * (normalized_scores[j][k] - normalized_scores[i][k]) for k in range(score_matrix.shape[1])])
        return discordance_matrix

    def calculate_net_flow(self,score_matrix):
        # Method to calculate the discordance matrix
        normal_matrix = self.normalization(score_matrix)
        concordance_matrix = self.calculate_concordance(score_matrix,normal_matrix)
        discordance_matrix = self.calculate_discordance(score_matrix,normal_matrix)
        net_flow = np.zeros((score_matrix.shape[0],))
        for i in range(score_matrix.shape[0]):
            net_flow[i] = sum([self.concordance_index * concordance_matrix[i][j] - self.discordance_index * discordance_matrix[i][j] for j in range(score_matrix.shape[0])])
        return net_flow

    def rank_solutions(self,score_matrix):
        # Method to rank the solutions based on net flow values
        net_flow = self.calculate_net_flow(score_matrix)
        ranking = np.argsort(-net_flow )
        return ranking

    def pareto_frontier(self,matrix):
        # Sort the matrix
        matrix = np.multiply(matrix,np.array([-1,1,-1,-1]))
        matrix = matrix[np.argsort(-matrix[:, 1])]

        # Inizialise list for Pareto frontier
        pareto_points = [matrix[0]]

        # Read the matrix and take the point on the Pareto frontier 
        for i in range(1, matrix.shape[0]):
            if matrix[i, 2] <= pareto_points[-1][2]:
                pareto_points.append(matrix[i])

        # Convert list on numpy matrix
        pareto_frontier = np.array(pareto_points)
        pareto_frontier = np.multiply(pareto_frontier,np.array([-1,1,-1,-1]))

        return pareto_frontier

    def change_weight(self,weight):
        self.weights = weight
        