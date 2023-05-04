# import pandas as pd
# from read_instance import *
class solution:
     def __init__(self,objective_value,cost,centres_m,centres_f,qtt_recue_hosp,qtt_collect,stock,qtt_manquante,nom_instance,time):
        self.objective_value = objective_value
        self.cost = cost
        self.centres_m = centres_m
        self.centres_f = centres_f
        self.qtt_recue_hosp = qtt_recue_hosp
        self.qtt_collect = qtt_collect
        self.stock = stock
        self.qtt_manquante = qtt_manquante
        self.nom_instance=nom_instance
        self.time = time
     def print(self,instance):
        print("Solution trouvée")
        ###  le code suivant affiche quels centres sont placés, où et quand : 

        print("La quantite de sang manquante est ", self.objective_value, " et la solution a coute " , self.cost)
        for l in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                for m in range(instance.nb_locations):
                    if self.centres_m[m][l][p] == 1 :
                        # print("Le centre mobile {} est placé à la localisation {},{} à la période {}".format(m,instance.locations[l][0],instance.locations[l][1],p+1))
                        print("Le centre mobile {} est placé à la localisation {} à la période {}".format(m,l,p+1))
            for f in range(instance.nb_locations):
                if self.centres_f[f][l] == 1:
                        print("Le centre fixe {} est construit à la localisation {},{} ".format(f,instance.locations[l][0],instance.locations[l][1]))
        

        ### Le code suivant affiche la quantité de sang passant par le lieu l (qtt collectée et combien elle envoie à qui )

        # for p in range(instance.time_horizon):
        #     print("A la période {} : ".format(p+1))
        #     for l in range(instance.nb_locations):
        #         print("La localisation {} ".format(l))
        #         for d in range(instance.nb_donors):
        #             if self.qtt_collect[l][p][d] != 0.0:
        #                 print("reçoit {} depuis le groupe de donneurs {}".format(self.qtt_collect[l][p][d],d))
        #         for h in range(instance.nb_hospitals):
        #             if self.qtt_recue_hosp[l][h][p] != 0.0:
        #                 print("envoie {} à l'hôpital {}".format(self.qtt_recue_hosp[l][h][p],h))

        ### Le code suivant va afficher ce qui se passe au niveau de l'hôpital : 
        ### ce qui est envoyé, ce qui manque, ce qui est stocké ... 

        for p in range(instance.time_horizon): 
            print("A la période {} :".format(p+1))
            for h in range(instance.nb_hospitals):
                qtt_recue = 0
                for l in range(instance.nb_locations):
                    qtt_recue += self.qtt_recue_hosp[l][h][p]
                print("l'hôpital {} a besoin de {}, reçoit {}, stocke {} et manque {} de sang et il y avait avant {}".format(h,instance.Need_hospital[h][p],qtt_recue,self.stock[h][p+1], self.qtt_manquante[h][p],self.stock[h][p]))
  
     def write(self,inst,name,file,cas):
        fixe = ""
        mobile = ["" for per in range(inst.time_horizon)]
        for l in range(inst.nb_locations):
            for p in range(inst.time_horizon):
                for m in range(inst.nb_locations):
                    if self.centres_m[m][l][p] == 1 :
                        mobile[p] += str(l)+", "
            for f in range(inst.nb_locations):
                if self.centres_f[f][l] == 1:
                    fixe += str(l) +", "
        with open("solution" + file[8:] +"/"+ name + "_"+ str(cas), "w") as fichier:
            fichier.write("------" + "solution" + file[8:] +"/"+ name + "-------\n")
            fichier.write("\nLa quantité de sang manquante " + str(self.objective_value) + "calculée en ...\n")
            fichier.write("Le coût de ka solution est " +  str(self.cost) +" et le budjet est de ...\n")
            fichier.write("\nLes centres fixes sont positionnés aux localisations " + fixe+"\n")
            for p in range(inst.time_horizon):
                if mobile[p] == "":
                   fichier.write("\nPériode " + str(p) + ": pas de centres mobiles positionnés") 
                else : 
                    fichier.write("\nPériode " + str(p) + ": Les centres mobiles sont positionnés aux localisations " + mobile[p])