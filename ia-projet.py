import random

class Individu:
    def __init__(self, t):
        self.t = t
        self.params = [random.randint(-10,10) for i in range(6)]
        self.x, self.y = self.calcul_pos()
        
    # Check if queen has conflict
    def calcul_pos(self):
    	x = self.params[0] * math.sin(self.params[1] * t + self.params[2])
    	y = self.params[3] * math.sin(self.params[4] * t + self.params[5])
        return x, y
    
    # Return euclidien distance
    def fitness(self, x, y):
    	X = [self.x, x]
    	Y = [self.y, y]
        return np.sqrt(np.sum((Y - X)**2))


# Retrieve random position_sample row from dataset

# Algo génétique : generate individus
# mutation
# croisement

# Check individus with fitness function

# Store individus

# Use p1-p6 for the rest of position samples 

# Store difference between sample and calculated individus

# Find the more accurate value 
