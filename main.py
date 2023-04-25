import random
from algo_genetic import *
import Individual
from utils import *
from PrometheeII import *


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

lire_fichier_matrice("./donnes_V3/Cost_map.txt")
Matrix = returnMatrix()
Instance_Map = Map(readMapFile(mapfile))
#Instance_Map.posInit()
#print(Instance_Map.returnGrid())

#algo = Individual.Individual_algo_genetic(Matrix, Instance_Map, 0)
test = Algo_genetic(1,1000,0.80,0.20,Matrix,Instance_Map,utils.costDic)
liste_pop =test.genetic_algorithm()
print(liste_pop)

promethe = PrometheeII([1,2])
print(promethe.build_matrix(liste_pop))
promethe.normalize_matrix()
promethe.calculate_concordance_and_discordance_matrices()
promethe.upgrade_id()
promethe.find_pareto_border()
promethe.show_3d_graph()

# algo.returnNbParcel()
#a = algo.chooseCandidate()
#print(a)
#matrix[0][90]

#print(a)
# print(len(a))
#algo.putParcel()
#algo.objectDistance((-10,10))