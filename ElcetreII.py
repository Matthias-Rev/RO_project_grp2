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
        print("end ELECTREE")
        return ranking

    def build_matrix(self,instances):
        matrix = np.array([[p.returnM_totalComp(), p.returnM_totalProd(), p.return_m_minDistHabitation()] for p in instances])
        return matrix

    def pareto_frontier_ND(self,matrix):
        """
        Returns the indices of the Pareto frontier for a matrix of fitness values
        with multiple objectives (dimensions).
        """
        # Trier la matrice en ordre croissant sur les deux premières colonnes (scores à minimiser)
        sorted_matrix = matrix[np.lexsort((matrix[:, 1], matrix[:, 0]))]

        # Initialiser une liste vide pour stocker les indices des individus dans la frontière de Pareto
        pareto_front = []

        # Initialiser les valeurs à comparer pour la frontière de Pareto
        max_third_score = -np.inf
        min_second_score = sorted_matrix[0, 1]

        # Parcourir la matrice triée
        for i in range(sorted_matrix.shape[0]):
            # Si le score du troisième critère est supérieur à la valeur maximale trouvée jusqu'à présent,
            # le point est ajouté à la frontière de Pareto
            if sorted_matrix[i, 2] >= max_third_score:
                max_third_score = sorted_matrix[i, 2]
                pareto_front.append(i)

            # Si le score du deuxième critère est inférieur à la valeur minimale trouvée jusqu'à présent,
            # le point est ajouté à la frontière de Pareto
            if sorted_matrix[i, 1] <= min_second_score:
                min_second_score = sorted_matrix[i, 1]
                pareto_front.append(i)

        # Retourner la liste des indices des individus dans la frontière de Pareto
        return list(set(pareto_front))

    import numpy as np

    import numpy as np

    def pareto_frontier(self,matrix):
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






