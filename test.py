import numpy as np
from collections import Counter

def has_mul(lst):
    seen= set()
    liste_counter = 0
    while liste_counter < len(lst):
        i_counter = 0   
        while 0 <= i_counter < len(lst[liste_counter]):
            print(i_counter, liste_counter,"i, list")
            print(lst)
            if lst[liste_counter][i_counter] in seen:
                del lst[liste_counter][i_counter]
                i_counter-=1
            print(lst,"after")
            print(i_counter, liste_counter,"i, list after")
            if len(lst[liste_counter]) != 0:
                seen.add(lst[liste_counter][i_counter])
            else:
                del lst[liste_counter]
                liste_counter-=1
                i_counter=len(lst[liste_counter])
            i_counter+=1
        liste_counter+=1
    return False

matrix=[["C", "R"], ["R", "R", "C"],["Y","R"]]
print(has_mul(matrix))
print(matrix)
