import random
import Individual
from utils import *
import copy


mapObject = Map(constructMap(), costDic)
i = 0
algo = Individual.Individual_algo_genetic(copy.copy(mapObject))
a = algo.chooseCandidate()

