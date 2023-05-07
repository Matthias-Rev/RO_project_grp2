
import numpy as np

class ELECTRE:
    def __init__(self, score_matrix, weights, concordance_index, discordance_index):
        self.score_matrix = score_matrix
        self.weights = weights
        self.concordance_index = concordance_index
        self.discordance_index = discordance_index

    def calculate_concordance(self):
        concordance_matrix = np.zeros((self.score_matrix.shape[0], self.score_matrix.shape[0]))
        for i in range(self.score_matrix.shape[0]):
            for j in range(self.score_matrix.shape[0]):
                if i == j:
                    continue
                concordance_matrix[i][j] = sum([self.weights[k] * (self.score_matrix[i][k] >= self.score_matrix[j][k]) for k in range(self.score_matrix.shape[1])])
        return concordance_matrix

    def calculate_discordance(self):
        discordance_matrix = np.zeros((self.score_matrix.shape[0], self.score_matrix.shape[0]))
        for i in range(self.score_matrix.shape[0]):
            for j in range(self.score_matrix.shape[0]):
                if i == j:
                    continue
                discordance_matrix[i][j] = sum([self.weights[k] * (self.score_matrix[j][k] - self.score_matrix[i][k]) for k in range(self.score_matrix.shape[1])])
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

# Define the weights for each criterion
weights = [0.3, 0.5, 0.2]

# Define the scores for each alternative on each criterion
score_matrix = np.array([
    [5, 7, 8],
    [10, 10, 7],
    [8, 6, 6],
    [4, 9, 5]
])

# Define the concordance and discordance thresholds
concordance_index = 0.6
discordance_index = 0.4

# Create an instance of the ELECTRE class
electre = ELECTRE(score_matrix, weights, concordance_index, discordance_index)

# Calculate the concordance matrix
concordance_matrix = electre.calculate_concordance()

# Calculate the discordance matrix
discordance_matrix = electre.calculate_discordance()
# Calculate the net flow values for each alternative
net_flow = electre.calculate_net_flow()

# Rank the alternatives based on their net flow values
ranking = electre.rank_solutions()
print("Alternative ranking:")
print(ranking)
