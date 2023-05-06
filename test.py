from Electre import *
import numpy as np
criteria_matrix = np.array([
    [3, 5, 2, 5],
    [2, 3, 5, 4],
    [10, 10, 10, 10],
    [5, 4, 4, 3],
    [4, 5, 4, 2]
])

# Matrice des poids des critères Production, compacité, 
weights = np.array([0.5, 0.5, -0.5, 0.5])

# Seuils de concordance et de discordance
concordance_thresholds = np.array([0.6, 0.6, 0.6, 0.6])
discordance_threshold = 0.3

# Noms des alternatives
names = ["A1", "A2", "A3", "A4", "A5"]

# Création de l'objet ELECTRE
electre = Electre(criteria_matrix, weights, concordance_thresholds, discordance_threshold)
pareto_border = electre.pareto_frontier(criteria_matrix)
print(electre.get_ranked_indices())
print(pareto_border)

# Calcul du classement final
electre.compute_ranking()
