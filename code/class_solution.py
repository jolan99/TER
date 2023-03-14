class solution:
     def __init__(self,objective_value,cost,centres_m,centres_f):
          self.objective_value = objective_value
          self.cost = cost
          self.centres_m = centres_m
          self.centres_f = centres_f
     def print(self,instance):
        print("Solution trouvée")
        for l in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                for m in range(instance.nb_locations):
                    if self.centres_m[m][l][p] == 1 :
                        print("Un centre mobile est placé à la localisation {},{} à la période {}".format(instance.locations[l][0],instance.locations[l][0],p))
            for f in range(instance.nb_locations):
                if self.centres_f[f][l] == 1:
                        print("Un centre fixe est construit à la localisation {},{} ".format(instance.locations[l][0],instance.locations[l][0]))
