class solution:
     def __init__(self,objective_value,cost,centres_m,centres_f,qtt_transf,qtt_collect,stock,qtt_manquante):
        self.objective_value = objective_value
        self.cost = cost
        self.centres_m = centres_m
        self.centres_f = centres_f
        self.qtt_transf = qtt_transf
        self.qtt_collect = qtt_collect
        self.stock = stock
        self.qtt_manquante = qtt_manquante
     def print(self,instance):
        print("Solution trouvée")
        print("La quantite de sang manquante est ", self.objective_value, " et la solution a coute " , self.cost)
        for l in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                for m in range(instance.nb_locations):
                    if self.centres_m[m][l][p] == 1 :
                        print("Un centre mobile est placé à la localisation {},{} à la période {}".format(instance.locations[l][0],instance.locations[l][0],p+1))
            for f in range(instance.nb_locations):
                if self.centres_f[f][l] == 1:
                        print("Un centre fixe est construit à la localisation {},{} ".format(instance.locations[l][0],instance.locations[l][0]))
