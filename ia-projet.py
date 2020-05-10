import random
import pandas as pd
import math

class Individu:
    def __init__(self, params=None):
        self.params = params if params else [random.uniform(-10, 10) for i in range(6)]

    # Calculate position based on time (with formula)
    def calcul_pos(self, t):
        self.x = self.params[0] * math.sin(self.params[1] * t + self.params[2])
        self.y = self.params[3] * math.sin(self.params[4] * t + self.params[5])

    # Calculate euclidean distance between individual pos and data pos
    def fitness(self, t, x, y):
        self.calcul_pos(t)
        res = math.pow(self.x - x, 2) + math.pow(self.y - y, 2)
        self.dist = math.sqrt(res)

    # Evaluate individual as a solution for data set based on threshold
    def isGood(self, data_arr, threshold=5):
        for ind, el in enumerate(data_arr):
            self.fitness(el[0], el[1], el[2]) # Use t, x, y from data
            if self.dist > threshold:
                return False
        return True

    # Return mutated individual
    def mutation(self):
        self.params[random.randit(0, 5)] = random.uniform(-10, 10)

    # Return crossing individual
    def croisement(ind_arr):
        inds = random.choices(ind_arr, k=2)
        return Individu(inds.params[:4] + inds.params[4:]), Individu(inds.params[:4] + inds.params[4:])

    # Return sublist
    def selection(ind_arr, ub, lb):
        subarr = []
        subarr.extend(ind_arr[:ub])
        subarr.extend(ind_arr[-lb:])
        return subarr

    # Caclulate pos based on params and compare to data pos
    def calculate(data_arr, ind=None, params=None):
        params = ind.params if ind else params
        for ind, el in enumerate(data_arr):
            x = params[0] * math.sin(params[1] * el[0] + params[2])
            y = params[3] * math.sin(params[4] * el[0] + params[5])
            print("data x : ", "%.2f" % el[1], "\ncalc x : ", "%.2f" % x)
            print("data y : ", "%.2f" % el[2], "\ncalc y : ", "%.2f\n" % y)
            
def main():
    # Read csv file and transform to numpy array
    csv_path = "position_sample.csv"
    df = pd.read_csv(csv_path, sep=";")
    data = df.to_numpy()

    # TODO Generate a population ?
    
    # TODO Generic algorithm
    print("Calculating...")
    while True:
        ind = Individu()
        if ind.isGood(data):
            break

    # Solution found
    print("Parameters found: ", ind.params)

    # Separate calculation (params found before)
    params = [-2.5484, -8.3355, -4.2711, 3.7503, 9.4722, 2.0302]
    Individu.calculate(data, params=params)

    Individu.calculate(data, ind=ind)

if __name__ == "__main__":
    main()