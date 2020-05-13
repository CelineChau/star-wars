import random
import pandas as pd
import math

class Individu:
    def __init__(self, params=None):
        self.params = params if params else [random.uniform(-10, 10) for i in range(6)]
        self.dist = 0

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
        return self.dist < threshold
    
    def __str__(self):
        params = "\n ".join("p" + str(ind+1) + " : " + str(el) for ind, el in enumerate(self.params))
        return params + "\nDistance: " + str(self.dist)
    
    def displayPop(pop):
        for ind in pop:
            ind.toString()

    # Type "moyenne" ou "mediane"
    def evaluate(pop, data_arr, type="moyenne"):
        if type == "moyenne":
            for individu in pop:
                moy = 0
                for ind, el in enumerate(data_arr):
                    moy += individu.fitness(el[0], el[1], el[2])
                individu.dist = moy / len(data_arr)
        elif type == "mediane":
            for individu in pop:
                med_list = list()
                for ind, el in enumerate(data_arr):
                    med_list.append(individu.fitness(el[0], el[1], el[2]))
                med_list.sort()
                med_ind = int(math.ceil(len(med_list) / 2))
                individu.dist = med_list[med_ind]

        return sorted(pop, key=lambda x: x.dist)
    
    # Return list of individus
    def create_pop(count):
        pop = list()
        for i in range(count):
            pop.append(Individu())
        return pop

    # Return mutated individual
    def mutation(self):
        self.params[random.randint(0,5)] = random.uniform(-10, 10)
        return self

    # Return crossing individual
    def croisement(ind1, ind2):
        return Individu(ind1.params[:3] + ind2.params[3:]), Individu(ind1.params[:3] + ind2.params[3:])

    # Return sublist
    def selection(pop, ub, lb):
        return pop[:ub] + pop[-lb:]

    # Caclulate pos based on params and compare to data pos
    def calculate(data_arr, ind=None, params=None):
        print("Calculation for verification :")
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

    nbIterations =  0
    solutionTrouvee = False
    pop = Individu.create_pop(25)
    
    print("Calculating...")
    
    while not solutionTrouvee:
        nbIterations += 1
        # evaluation = Individu.evaluate(pop, data, type="moyenne")
        evaluation = Individu.evaluate(pop, data, type="mediane")
        if evaluation[0].isGood(threshold=0.1):
            solutionTrouvee = True
        else :
            select = Individu.selection(evaluation, 10, 4)
            croises = []
            for i in range(0, len(select), 2):
                croises += Individu.croisement(select[i], select[i + 1])
            mutes = []
            for s in select:
                mutes.append(s.mutation())
            # Create new pop
            newAlea = Individu.create_pop(5)
            pop = select[:] + croises[:] + mutes[:] + newAlea[:]

    # Solution found
    print("Solution found:\n", evaluation[0], "\nNombre d'iterations: ", nbIterations)
    Individu.calculate(data, ind=evaluation[0])

if __name__ == "__main__":
    main()