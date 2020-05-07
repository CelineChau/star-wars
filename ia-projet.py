import random
import pandas as pd
import math

class Individu:
    def __init__(self, t, x, y, params=None):
        self.t = t
        self.params = params if params else [random.randint(-10, 10) for i in range(6)]
        print(self.params)
        self.x, self.y = self.calcul_pos()
        self.dist = self.fitness(x, y)

    # Check if queen has conflict
    def calcul_pos(self):
        x = self.params[0] * math.sin(self.params[1] * self.t + self.params[2])
        y = self.params[3] * math.sin(self.params[4] * self.t + self.params[5])
        return x, y

    # Return euclidien distance
    def fitness(self, x, y):
        res = 0
        res += math.pow(self.x - x, 2)
        res += math.pow(self.y - y, 2)
        return math.sqrt(res)


def main(csv_path):
    df = pd.read_csv(csv_path, sep=";")
    # Retrieve random position_sample row from dataset
    data = df.sample().to_numpy()[0]
    print(data)
    ind1 = Individu(data[0], data[1], data[2])
    print(ind1.dist)
    params = ind1.params
    data = df.sample().to_numpy()[0]
    print(data)
    ind2 = Individu(data[0], data[1], data[2], params)
    print(ind2.dist)

# Algo génétique : generate individus
# mutation
# croisement

# Check individus with fitness function

# Store individus

# Use p1-p6 for the rest of position samples

# Store distance between sample and calculated individus

# Find the more accurate value


if __name__ == "__main__":
    # test()

    main("position_sample.csv")

    # allSols = algoLoop()
    # print(*allSols, sep="\n")
