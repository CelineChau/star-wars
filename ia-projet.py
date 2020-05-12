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
        return math.sqrt(res)

    # Evaluate individual as a solution for data set based on threshold
    def isGood(self, threshold=5):
        return (self.dist != None and self.dist < threshold)
    
    def toString(self):
        dist = self.dist if self.dist else " "
        print("params: ", self.params, " distance: ", dist)
    
    def displayPop(pop):
        for ind in pop:
            ind.toString()
    
    def evaluate(pop, data_arr):
        median = 0
        for individu in pop:
            for ind, el in enumerate(data_arr):
                print(type(individu))
                median += individu.fitness(el[0], el[1], el[2])
            individu.dist = median / len(data_arr)
            
        return sorted(pop, key=lambda x: x.dist)
    
    # Return list of individus
    def create_pop(count):
        pop = []
        for i in range(count):
            pop.append(Individu())
               
        return pop

    # Return mutated individual
    def mutation(self):
        self.params[random.randint(0,5)] = random.uniform(-10, 10)

    # Return crossing individual
    def croisement(pop):
        inds = random.choices(pop, k=2)
        return Individu(inds[0].params[:4] + inds[1].params[4:]), Individu(inds[1].params[:4] + inds[0].params[4:])

    # Return sublist
    def selection(pop, ub, lb):
        subarr = []
        subarr.extend(pop[:ub])
        subarr.extend(pop[-lb:])
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

    # TODO Generate a population
    nbIterations =  0
    solutionTrouvee = False
    pop = Individu.create_pop(25)
    
    # TODO Generic algorithm
    print("Calculating...")
#    while True:
#        ind = Individu()
#        if ind.isGood(data):
#            break
    
    while not solutionTrouvee:
        nbIterations += 1
        evaluation = Individu.evaluate(pop, data)
        if evaluation[0].isGood():
            print("evaluation", evaluation[0].toString())
            solutionTrouvee = True;
        else :
            select = Individu.selection(evaluation, 10, 4)
            croises = []
            croises.append(Individu.croisement(select))
            mutes = []
            for s in select:
                mutes.append(Individu.mutation(s))
            # Create new pop
            newAlea = Individu.create_pop(5)
            pop = select[:] + croises[:] + mutes[:] + newAlea[:]


    # Solution found
    print("Solution found: ", evaluation[0].toString(), ", nbIterations: ", nbIterations)

    # Separate calculation (params found before)
#    params = [-2.5484, -8.3355, -4.2711, 3.7503, 9.4722, 2.0302]
#    Individu.calculate(data, params=params)
#
#    Individu.calculate(data, ind=ind)

if __name__ == "__main__":
    main()