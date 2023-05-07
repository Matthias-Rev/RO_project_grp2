import numpy as np

class ELECTRE:
    def __init__(self, score_matrix, weights, concordance_index, discordance_index):
        self.score_matrix = score_matrix
        self.weights = weights
        self.concordance_index = concordance_index
        self.discordance_index = discordance_index

        # normalization
        self.normalized_scores = np.zeros_like(self.score_matrix)
        for i in range(self.score_matrix.shape[1]):
            self.normalized_scores[:,i] = (self.score_matrix[:,i] - np.min(self.score_matrix[:,i])) / (np.max(self.score_matrix[:,i]) - np.min(self.score_matrix[:,i]))

    def calculate_concordance(self):
        concordance_matrix = np.zeros((self.score_matrix.shape[0], self.score_matrix.shape[0]))
        for i in range(self.score_matrix.shape[0]):
            for j in range(self.score_matrix.shape[0]):
                if i == j:
                    continue
                concordance_matrix[i][j] = sum([self.weights[k] * (self.normalized_scores[i][k] >= self.normalized_scores[j][k]) for k in range(self.score_matrix.shape[1])])
        return concordance_matrix

    def calculate_discordance(self):
        discordance_matrix = np.zeros((self.score_matrix.shape[0], self.score_matrix.shape[0]))
        for i in range(self.score_matrix.shape[0]):
            for j in range(self.score_matrix.shape[0]):
                if i == j:
                    continue
                discordance_matrix[i][j] = sum([self.weights[k] * (self.normalized_scores[j][k] - self.normalized_scores[i][k]) for k in range(self.score_matrix.shape[1])])
        return discordance_matrix

    def calculate_net_flow(self):
        concordance_matrix = self.calculate_concordance()
        discordance_matrix = self.calculate_discordance()
        net_flow = np.zeros((self.score_matrix.shape[0],))
        for i in range(self.score_matrix.shape[0]):
            net_flow[i] = sum([self.concordance_index * concordance_matrix[i][j] - self.discordance_index * discordance_matrix[i][j] for j in range(self.score_matrix.shape[0])])
        return net_flow

    def rank_solutions(self):
        net_flow = self.calculate_net_flow()
        ranking = np.argsort(-net_flow)
        return ranking

    def build_matrix(self,instances):
        matrix = np.array([[p.returnM_totalComp(), p.returnM_totalProd(), p.return_m_minDistHabitation()] for p in instances])
        return matrix

    def pareto_frontier_ND(self,final_matrix):
        """
        Returns the indices of the Pareto frontier for a matrix of fitness values
        with multiple objectives (dimensions).
        """
        # Get number of dimensions
        num_dims = final_matrix.shape[1]
        # Initialize list to store indices of solutions in Pareto frontier
        pareto_frontier = []
        # Iterate over all solutions
        for i in range(final_matrix.shape[0]):
            # Assume solution i is in Pareto frontier until proven otherwise
            is_pareto = True
            # Compare solution i to all other solutions
            for j in range(final_matrix.shape[0]):
                # Check if solution j dominates solution i
                if np.all(final_matrix[j, :] <= final_matrix[i, :]) and np.any(
                        final_matrix[j, :] < final_matrix[i, :]):
                    # If solution j dominates solution i, then i is not in Pareto frontier
                    is_pareto = False
                    break
            # If solution i is still in Pareto frontier, add its index to the list
            if is_pareto:
                pareto_frontier.append(i)
        return pareto_frontier


# Define the weights for each criterion
weights = [0.3, 0.5, 0.2]

# Define the scores for each alternative on each criterion
score_matrix = np.array([
    [9, 9, 9],
    [30, 10, 10],
    [0, 0, 30],
    [30, 30, 30]
])

# Define the concordance and discordance thresholds
concordance_index = 0.6
discordance_index = 0.4

# Create an instance of the ELECTRE class
electre = ELECTRE(score_matrix, weights, concordance_index, discordance_index)

# Rank the alternatives based on their net flow values
ranking = electre.rank_solutions()
pareto = electre.pareto_frontier_ND(score_matrix)
print(ranking)
print(pareto)
