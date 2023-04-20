import random


def deplacement_aleatoire(matrice):
    # Initialisation de la liste des coordonnées visitées
    coordonnees_visitees = [(0, 0)]

    # Détermination des coordonnées de départ
    x, y = 0, 0

    # Boucle de déplacement aléatoire
    while True:
        # Détermination des cases adjacentes
        adjacentes = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        # Filtrage des cases valides
        valides = [c for c in adjacentes if
                   0 <= c[0] < len(matrice) and 0 <= c[1] < len(matrice[0]) and matrice[c[0]][c[1]] not in ["R","C"] and c not in coordonnees_visitees]

        # Arrêt si aucune case valide n'a été trouvée
        if not valides:
            break

        # Sélection d'une case valide aléatoire
        nouvelle_case = random.choice(valides)

        # Mise à jour des coordonnées actuelles
        x, y = nouvelle_case

        # Ajout des coordonnées visitées à la liste
        coordonnees_visitees.append(nouvelle_case)

    return coordonnees_visitees


def lire_fichier_matrice(nom_fichier):
    matrice = []
    with open(nom_fichier, 'r') as f:
        ligne = f.readline()
        while ligne:
            ligne_matrice = []
            for caractere in ligne.strip():
                if caractere.isdigit():
                    ligne_matrice.append(int(caractere))
            if ligne_matrice:
                matrice.append(ligne_matrice)
            ligne = f.readline()
    return matrice

print(lire_fichier_matrice("Cost_map.txt"))