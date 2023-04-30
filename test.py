import matplotlib.pyplot as plt

# Liste de coordonnées
x = [1, 2, 3, 4]#, 5, 6]
y = [2, 4, 1, 5]#, 6, 3]

# Création du graphique et remplissage de la surface
fig, ax = plt.subplots()
ax.fill(x, y)

# Affichage du graphique
plt.show()

# Calcul de l'aire de la surface
aire = 0.5 * abs(sum([x[i]*y[i+1]-x[i+1]*y[i] for i in range(-1, len(x)-1)]))
print("L'aire de la surface est de :", aire)