import numpy as np
import matplotlib.pyplot as plt


class Electre:

    def __init__(self, data, weights, thresholds, preference_thresholds):
        self.data = data
        self.weights = weights
        self.thresholds = thresholds
        self.preference_thresholds = preference_thresholds
        self.normalized_data = self.normalize_data()
        self.discordance_matrix = self.compute_discordance_matrix()
        self.concordance_matrix = self.compute_concordance_matrix()
        self.outranking_matrix = self.compute_outranking_matrix()
        self.ranking = self.compute_ranking()

    def normalize_data(self):
        """Normalise la matrice de données."""
        return (self.data - np.min(self.data, axis=0)) / (np.max(self.data, axis=0) - np.min(self.data, axis=0))

    def compute_discordance_matrix(self):
        """Calcule la matrice de discordance."""
        num_alternatives = len(self.data)
        discordance_matrix = np.zeros((num_alternatives, num_alternatives))
        for i in range(num_alternatives):
            for j in range(i + 1, num_alternatives):
                discordance_matrix[i, j] = np.max(np.abs(self.normalized_data[i] - self.normalized_data[j]) /
                                                  self.preference_thresholds)
                discordance_matrix[j, i] = discordance_matrix[i, j]
        return discordance_matrix

    def compute_concordance_matrix(self):
        """Calcule la matrice de concordance."""
        num_alternatives = len(self.data)
        concordance_matrix = np.zeros((num_alternatives, num_alternatives))
        for i in range(num_alternatives):
            for j in range(i + 1, num_alternatives):
                num_criteria = len(self.weights)
                concordance_values = []
                for k in range(num_criteria):
                    if self.normalized_data[i, k] >= self.normalized_data[j, k]:
                        concordance_values.append(self.weights[k])
                if sum(concordance_values) >= self.thresholds[0]:
                    concordance_matrix[i, j] = 1
                concordance_matrix[j, i] = 1 - concordance_matrix[i, j]
        return concordance_matrix

    def compute_outranking_matrix(self):
        """Calcule la matrice d'outrangement."""
        num_alternatives = len(self.data)
        outranking_matrix = np.zeros((num_alternatives, num_alternatives))
        for i in range(num_alternatives-1):
            for j in range(i + 1, num_alternatives-1):
                concordance_diff = self.concordance_matrix[i, j] - self.concordance_matrix[j, i]
                discordance_diff = self.discordance_matrix[i, j] - self.discordance_matrix[j, i]
                if concordance_diff >= self.thresholds[1] and discordance_diff <= self.thresholds[2]:
                    outranking_matrix[i, j] = 1
                if concordance_diff <= -self.thresholds[1] and discordance_diff >= -self.thresholds[3]:
                    outranking_matrix[j, i] = 1
        return outranking_matrix

    def compute_ranking(self):
        """Calcule le classement final."""
        num_alternatives = len(self.data)
        ranking = np.zeros(num_alternatives)
        for i in range(num_alternatives):
            num_outranking = np.sum(self.outranking_matrix[i])
            num_outranked_by = np.sum(self.outranking_matrix[:, i])
            ranking[i] = num_outranking / (num_outranking + num_outranked_by)
        return ranking

    def pareto_frontier(self,rankings):
        # On commence par transformer le classement en tableau numpy
        rankings = np.array(rankings)

        # On récupère le nombre d'alternatives et de critères
        num_alternatives, num_criteria = rankings.shape

        # On initialise la liste des points de la frontière de Pareto
        pareto_frontier = []

        # Pour chaque alternative, on vérifie si elle est dominante ou non
        for i in range(num_alternatives):
            is_dominated = False

            for j in range(num_alternatives):
                # On ne compare pas l'alternative avec elle-même
                if i == j:
                    continue

                # On compare les alternatives selon chaque critère
                better = np.less(rankings[i], rankings[j])

                # Si l'alternative i est dominée par l'alternative j,
                # on passe à l'alternative suivante
                if np.all(better):
                    is_dominated = True
                    break

            # Si l'alternative i n'est pas dominée, on l'ajoute à la frontière de Pareto
            if not is_dominated:
                pareto_frontier.append(i)

        # On retourne la liste des points de la frontière de Pareto
        return pareto_frontier

    def show_3d_graph(self,pareto_border):
        points = []
        for i in pareto_border:
            points.append(tuple(self.data[i]))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter([p[0] for p in points], [p[1] for p in points], [p[2] for p in points])
        plt.show()

    def get_ranked_indices(self):
        """Renvoie les indices des alternatives classées par ordre décroissant."""
        return np.argsort(self.compute_ranking())[::-1]