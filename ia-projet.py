import random, math, time
import pandas as pd

class Individu:
    def __init__(self, params=None):
        self.params = params if params else [random.uniform(-10, 10) for i in range(6)]
        self.dist = 0

    def __str__(self):
        params = "\n ".join("p" + str(ind+1) + " : " + str(el) for ind, el in enumerate(self.params))
        return params + "\nDistance: " + str(self.dist)

    # Calculate position based on time (with formula)
    def calcul_pos(self, t):
        self.x = self.params[0] * math.sin(self.params[1] * t + self.params[2])
        self.y = self.params[3] * math.sin(self.params[4] * t + self.params[5])

    # Calculate fitness of individu (median or average distance)
    def fitness(self, data_arr, type="mediane"):
        if type == "moyenne":
            moy = 0
            for ind, el in enumerate(data_arr):
                self.calcul_pos(el[0])
                moy += self.euc_dist(el[1], el[2])
            self.dist = moy / len(data_arr)
        elif type == "mediane":
            med_list = list()
            for ind, el in enumerate(data_arr):
                self.calcul_pos(el[0])
                med_list.append(self.euc_dist(el[1], el[2]))
            med_list.sort()
            med_ind = int(math.ceil(len(med_list) / 2))
            self.dist = med_list[med_ind]

    # Calculate euclidean distance between individual pos and data pos
    def euc_dist(self, x, y):
        res = math.pow(self.x - x, 2) + math.pow(self.y - y, 2)
        return math.sqrt(res)

    # Evaluate individual as a solution for data set based on threshold
    def isGood(self, threshold=5):
        return self.dist < threshold

    # Type "moyenne" ou "mediane"
    def evaluate(pop, data_arr, type="moyenne"):
        for individu in pop:
            individu.fitness(data_arr, type)
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
        return Individu(ind1.params[:3] + ind2.params[3:]), Individu(ind2.params[:3] + ind1.params[3:])

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

    # Initialize variables and population
    print("Searching for solution...")
    pop = Individu.create_pop(100)
    type = "mediane"  # ou moyenne
    threshold = 0.1
    nbIterations =  0
    solutionTrouvee = False

    while not solutionTrouvee:
        nbIterations += 1
        evaluation = Individu.evaluate(pop, data, type=type)
        if evaluation[0].isGood(threshold=threshold):
            solutionTrouvee = True
        else :
            # Selection
            select = Individu.selection(evaluation, 75, 25)
            # Croisement
            croises = []
            for i in range(0, len(select), 2):
                croises += Individu.croisement(select[i], select[i + 1])
            # Mutation
            mutes = []
            for s in select:
                mutes.append(s.mutation())
            # Nouvelle population
            newAlea = Individu.create_pop(100)
            pop = select[:] + croises[:] + mutes[:] + newAlea[:]

    # Solution found
    print("Solution found:\n", evaluation[0], "\nNombre d'iterations: ", nbIterations)
    evals = [round(p, 2) for p in evaluation[0].params]
    Individu.calculate(data, params=evals)

    # Format noms et solution
    et = ["Aumand", "Chau", "Donato"]
    fileName = "_".join(et)
    sol = ";".join(str(param) for param in evals)

    # Ecriture dans un fichier
    f = open(fileName + ".txt", "w")
    f.write(sol)
    f.close()
    print(fileName, sol, sep="\n")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))