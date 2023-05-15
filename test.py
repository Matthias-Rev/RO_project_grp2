import numpy as np
from collections import Counter

def has_mul(lst):
    seen= set()
    counter = 0
    for item in lst:
        if item in seen:
            del lst[counter]
            return True
        seen.add(item)
        counter+=1
    return False

matrix=["C", "R", "R"]
print(has_mul(matrix))
print(matrix)
