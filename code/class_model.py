# from read_instance import *
from read_instance import *
from modele_avec_sol_ini import *
from TERmodele1 import *
import pandas as pd
from checker import *



# import time
class Modelize:
    def __init__(self,solveur,sol_init,datafileName,Budget,cas):
          self.solveur = solveur
          self.sol_init = sol_init
          self.datafileName = datafileName
          self.Budget = Budget
          self.cas = cas ## soit "worst_case, best_case" pour les cas avec uncertain.txt et un epsilon d'acceptation pour training.test
    def solve(self,affichage,temps_limite): 
          
          
          if self.solveur == "CBC" :
               if self.sol_init == False:
                    instance = read_data(self.datafileName,self.cas,self.sol_init,self.Budget,temps_limite)
                    if(instance.valid == True):
                         if(self.cas == "all"):
                              with open(self.datafileName +"/uncertain.txt", "r") as file:
                                   # print("debug 1 ")
                                   
                                   line = file.readline()
                                   lineTab = line.split()
                                   nb_scenarios = int(lineTab[1])
                                   # print("nb_scenarios = ",nb_scenarios)
                                   #worst_case = float('inf')
                                   if int(lineTab[0]) == instance.nb_hospitals : 
                                        if int(lineTab[2]) == instance.time_horizon : #on vérifie qu'on soit bien dans le même cas que le déterministic
                                             # if cas == "average_case":
                                             qtt_manquante__moyenne = 0
                                             for scenario in range(nb_scenarios):
                                                  Need_hospital = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                                  
                                                  line = file.readline()
                                                  lineTab = line.split()
                                                  for p in range(instance.time_horizon):
                                                       for h in range(instance.nb_hospitals):
                                                            Need_hospital[h][p] += float(lineTab[h+p])
                                                            
                                                  # print("debug 2 : ",Need_hospital)
                                                  # Need_hospital = Need_hospital / nb_scenarios
                                                  instance.Need_hospital = Need_hospital
                                                  sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                                                  # sol.print(instance)
                                                  # print("Budget1 : ",self.Budget)
                                                  qtt_manquante__moyenne += sol.objective_value
                                                  # print(" qtt manquante totale : ",qtt_manquante__moyenne)
                              # print("nb scenarios : ",nb_scenarios)
                              qtt_manquante__moyenne = qtt_manquante__moyenne/nb_scenarios
                              # print("La quantité manquante moyenne est : ", qtt_manquante__moyenne)
                              return qtt_manquante__moyenne
                         else : 
                              sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)

                         # On écrit dans un fichier la solution des centres fixes sous forme de coordonnées  : 
                         centresfixes = pd.DataFrame(columns = ["lat","lon"])
                         for l in range(instance.nb_locations):
                              for f in range(instance.nb_locations):
                                   if(sol.centres_f[f][l] == 1):
                                        loc1 = pd.DataFrame([instance.locations[l][0]],columns = ["lat"])
                                        loc1 = loc1.assign(lon=[instance.locations[l][1]])
                                        
                                        centresfixes = centresfixes.append(loc1,ignore_index=True)

                         with open("sol_cf_"+instance.datafileName[-12:]+".txt", 'w') as f:
                              dfAsString = centresfixes.to_string(header=False, index=False)
                              f.write(dfAsString)

                         # On vérifie que la solution trouvée est valide : 
                         Checker(sol,instance)
                         print("checker : ",Checker(sol,instance))

                         if affichage == True :
                              sol.print(instance)
                         return sol
               elif self.sol_init == True:
                    instance = read_data(self.datafileName,self.cas,self.sol_init,self.Budget,temps_limite)
                    with open(self.datafileName +"/training.txt", "r") as file:
                                   # print("debug 1 ")
                                   
                         line = file.readline()
                         lineTab = line.split()
                         nb_scenarios = int(lineTab[1])
                         # print("nb_scenarios = ",nb_scenarios)
                         #worst_case = float('inf')
                         if int(lineTab[0]) == instance.nb_hospitals : 
                              if int(lineTab[2]) == instance.time_horizon : #on vérifie qu'on soit bien dans le même cas que le déterministic
                                   
                                   count = np.zeros(instance.nb_locations) # va nous servir pour le critère de choix plus tard
                                   for scenario in range(nb_scenarios):
                                        Need_hospital = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                        Need_hospital_bestC = np.ones((instance.nb_hospitals,instance.time_horizon))*1000000
                                        Need_hospital_worstC = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                        Need_hospital_averageC = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                                  
                                        line = file.readline()
                                        lineTab = line.split()
                                        for p in range(instance.time_horizon):
                                             for h in range(instance.nb_hospitals):
                                                  Need_hospital[h][p] += float(lineTab[h+p])
                                                  
                                                  ## on sauvegarde les cas aux cas où : 
                                                  if "best_case" in self.cas :
                                                       if Need_hospital_bestC[h][p] >= float(lineTab[h+p]) : 
                                                            Need_hospital_bestC[h][p] = float(lineTab[h+p])
                                                  if "worst_case" in self.cas :
                                                       if Need_hospital_worstC[h][p] <= float(lineTab[h+p]) : 
                                                            Need_hospital_bestC[h][p] = float(lineTab[h+p])
                                                  if "worst_case" in self.cas :
                                                       Need_hospital_averageC[h][p] += float(lineTab[h+p])
                                                  
                                                  # print("debug 2 : ",Need_hospital)
                                                  # Need_hospital = Need_hospital / nb_scenarios
                                        instance.Need_hospital = Need_hospital
                                        sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                                        for centre in range(instance.nb_locations):
                                             for loc in range(instance.nb_locations):
                                                  if sol.centres_f[centre][loc] == 1:
                                                       count[loc] += 1
                                   Need_hospital_averageC = Need_hospital_averageC / nb_scenarios
                                   # on boucle sur les différents cas demandés
                                   qtt_manquante__moyenne = np.zeros(len(self.cas))
                                   iterateur = 0
                                   #res = []
                                   for c in self.cas:
                                        # if(float(c)): # on vérifie si c'est bien un float, ça pourrait être best_case ou worst_case ou average_case 
                                        try :
                                             essai = float(c)
                                             # on crée l'instance de départ : 
                                             centres_fixes_initiaux = np.zeros(instance.nb_locations)
                                             for i in range(instance.nb_locations):
                                                  if count[i] >= c*(nb_scenarios):
                                                       centres_fixes_initiaux[i] += 1
                                                  
                                             # rajouté : 
                                             with open(self.datafileName +"/test.txt", "r") as file2:
                                             # print("debug 1 ")
                                             # qtt_manquante__moyenne = np.zeros(len(self.cas))
                                                  line = file2.readline()
                                                  lineTab = line.split()
                                                  nb_scenarios2 = int(lineTab[1])
                                                  # print("nb_scenarios = ",nb_scenarios)
                                                  if int(lineTab[0]) == instance.nb_hospitals : 
                                                       if int(lineTab[2]) == instance.time_horizon : #on vérifie qu'on soit bien dans le même cas que le déterministic
                                                            # if cas == "average_case":
                                                            # qtt_manquante__moyenne = 0
                                                            
                                                            for scenario in range(nb_scenarios2):
                                                                 #res.append([self.datafileName + "test" + str(scenario)])
                                                                 Need_hospital = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                                                 
                                                                 line = file2.readline()
                                                                 lineTab = line.split()
                                                                 for p in range(instance.time_horizon):
                                                                      for h in range(instance.nb_hospitals):
                                                                           Need_hospital[h][p] += float(lineTab[h+p])
                                                                           
                                                                 # print("debug 2 : ",Need_hospital)
                                                                 # Need_hospital = Need_hospital / nb_scenarios
                                                                 instance.Need_hospital = Need_hospital
                                                                 sol2, runtime = Model2_CBC_sol_ini(instance,self.Budget,temps_limite,centres_fixes_initiaux)
                                                                 #print(sol2)
                                                                 sol2.write(instance, "Pourcentages" + str(scenario),self.datafileName,c)
                                                                 #res[scenario].append(sol2.objective_value.getValue())
                                                                 #print(res)
                                                                 # sol.print(instance)
                                                                 # print("Budget1 : ",self.Budget)
                                                                 qtt_manquante__moyenne[iterateur] += sol2.objective_value
                                                                 # print(" qtt manquante totale : ",qtt_manquante__moyenne)
                                             # print("nb scenarios : ",nb_scenarios)
                                             qtt_manquante__moyenne[iterateur] = qtt_manquante__moyenne[iterateur]/nb_scenarios2
                                             iterateur += 1
                                             Checker(sol,instance)
                                             print("checker : ",Checker(sol,instance))
                                        except ValueError:
                                             if c == "worst_case" :
                                                  instance.Need_hospital = Need_hospital_worstC
                                                  sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                                                  sol.write(instance, "worst_case",self.datafileName,c)
                                                  #res.append(sol.objective_value)
                                                  # centres_fixes_initiaux = np.zeros(instance.nb_locations)
                                                  # for centre in range(instance.nb_locations):
                                                  #      for loc in range(instance.nb_locations):
                                                  #           if sol.centres_f[centre][loc] == 1:
                                                  #                centres_fixes_initiaux[loc] = 1

                                                  
                                                  
                                                  # with open(self.datafileName +"/test.txt", "r") as file2:
                                                  #      # print("###########debug##########")
                                                  #      # print("debug 1 ")
                                                  #      # qtt_manquante__moyenne = np.zeros(len(self.cas))
                                                  #      line = file2.readline()
                                                  #      lineTab = line.split()
                                                  #      nb_scenarios2 = int(lineTab[1])
                                                  #           # print("nb_scenarios = ",nb_scenarios)
                                                  #           #worst_case = float('inf')
                                                            
                                                  #      if int(lineTab[0]) == instance.nb_hospitals : 
                                                  #           if int(lineTab[2]) == instance.time_horizon : #on vérifie qu'on soit bien dans le même cas que le déterministic
                                                  #                     # if cas == "average_case":
                                                  #                     # qtt_manquante__moyenne = 0
                                                                      
                                                  #                for scenario in range(nb_scenarios2):
                                                  #                     Need_hospital = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                                                           
                                                  #                     line = file2.readline()
                                                  #                     lineTab = line.split()
                                                  #                     for p in range(instance.time_horizon):
                                                  #                          for h in range(instance.nb_hospitals):
                                                  #                               Need_hospital[h][p] += float(lineTab[h+p])
                                                                                     
                                                  #                          # print("debug 2 : ",Need_hospital)
                                                  #                          # Need_hospital = Need_hospital / nb_scenarios
                                                  #                     instance.Need_hospital = Need_hospital
                                                  #                     sol2, runtime = Model2_CBC_sol_ini(instance,self.Budget,temps_limite,centres_fixes_initiaux)
                                                  #                          # sol.print(instance)
                                                  #                          # print("Budget1 : ",self.Budget)
                                                  #                     qtt_manquante__moyenne[iterateur] += sol2.objective_value
                                                  #                          # print(" qtt manquante totale : ",qtt_manquante__moyenne)
                                                  #      # print("nb scenarios : ",nb_scenarios)
                                                  # qtt_manquante__moyenne[iterateur] = qtt_manquante__moyenne[iterateur]/nb_scenarios2
                                                  # iterateur += 1
                                                  # # Checker(sol,instance)
                                                  # # print("checker : ",Checker(sol,instance))
                                             elif c== "best_case" :
                                                  instance.Need_hospital = Need_hospital_bestC
                                                  sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                                                  sol.write(instance, "best_case",self.datafileName,c)
                                                  #res.append(sol.objective_value)
                                                  
                                             elif c == "average_case" : 
                                                  instance.Need_hospital = Need_hospital_averageC
                                                  sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                                                  sol.write(instance, "average_case",self.datafileName,c)
                                                  #res.append(sol.objective_value)
                                             else : 
                                                  print("Le cas '", c," ' n'est pas reconnu. Le choix est entre average_case, worst_case, et  best_case")
                                                  break
                                             centres_fixes_initiaux = np.zeros(instance.nb_locations)
                                             for centre in range(instance.nb_locations):
                                                  for loc in range(instance.nb_locations):
                                                       if sol.centres_f[centre][loc] == 1:
                                                            centres_fixes_initiaux[loc] = 1

                                                  
                                                  
                                             with open(self.datafileName +"/test.txt", "r") as file2:
                                                       # print("###########debug##########")
                                                       # print("debug 1 ")
                                                       # qtt_manquante__moyenne = np.zeros(len(self.cas))
                                                  line = file2.readline()
                                                  lineTab = line.split()
                                                  nb_scenarios2 = int(lineTab[1])
                                                            # print("nb_scenarios = ",nb_scenarios)
                                                            #worst_case = float('inf')
                                                            
                                                  if int(lineTab[0]) == instance.nb_hospitals : 
                                                       if int(lineTab[2]) == instance.time_horizon : #on vérifie qu'on soit bien dans le même cas que le déterministic
                                                                      # if cas == "average_case":
                                                                      # qtt_manquante__moyenne = 0
                                                                      
                                                            for scenario in range(nb_scenarios2):
                                                                 Need_hospital = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                                                           
                                                                 line = file2.readline()
                                                                 lineTab = line.split()
                                                                 for p in range(instance.time_horizon):
                                                                      for h in range(instance.nb_hospitals):
                                                                           Need_hospital[h][p] += float(lineTab[h+p])
                                                                                     
                                                                           # print("debug 2 : ",Need_hospital)
                                                                           # Need_hospital = Need_hospital / nb_scenarios
                                                                 instance.Need_hospital = Need_hospital
                                                                 sol2, runtime = Model2_CBC_sol_ini(instance,self.Budget,temps_limite,centres_fixes_initiaux)
                                                                 sol2.write(instance,"test", self.datafileName,c)
                                                                 #res.append(sol2.objective_value)
                                                                           # sol.print(instance)
                                                                           # print("Budget1 : ",self.Budget)
                                                                 qtt_manquante__moyenne[iterateur] += sol2.objective_value
                                                                           # print(" qtt manquante totale : ",qtt_manquante__moyenne)
                                                       # print("nb scenarios : ",nb_scenarios)
                                             qtt_manquante__moyenne[iterateur] = qtt_manquante__moyenne[iterateur]/nb_scenarios2
                                             iterateur += 1
                                                  # Checker(sol,instance)
                                                  # print("checker : ",Checker(sol,instance))
                                        # print("La quantité manquante moyenne est : ", qtt_manquante__moyenne)
                    file.close()

                    ## maintenant qu'on a la solution initiale, on fait tourner sur les scénarios. Et on regarde la qtt de sang manquante moyenne
                    # if(instance.valid == True):
                         
                              # with open(self.datafileName +"/test.txt", "r") as file:
                              #      # print("debug 1 ")
                              #      # qtt_manquante__moyenne = np.zeros(len(self.cas))
                              #      line = file.readline()
                              #      lineTab = line.split()
                              #      nb_scenarios = int(lineTab[1])
                              #      # print("nb_scenarios = ",nb_scenarios)
                              #      #worst_case = float('inf')
                                   
                              #      if int(lineTab[0]) == instance.nb_hospitals : 
                              #           if int(lineTab[2]) == instance.time_horizon : #on vérifie qu'on soit bien dans le même cas que le déterministic
                              #                # if cas == "average_case":
                              #                qtt_manquante__moyenne = 0
                                             
                              #                for scenario in range(nb_scenarios):
                              #                     Need_hospital = np.zeros((instance.nb_hospitals,instance.time_horizon))
                                                  
                              #                     line = file.readline()
                              #                     lineTab = line.split()
                              #                     for p in range(instance.time_horizon):
                              #                          for h in range(instance.nb_hospitals):
                              #                               Need_hospital[h][p] += float(lineTab[h+p])
                                                            
                              #                     # print("debug 2 : ",Need_hospital)
                              #                     # Need_hospital = Need_hospital / nb_scenarios
                              #                     instance.Need_hospital = Need_hospital
                              #                     sol, runtime = Model2_CBC_sol_ini(instance,self.Budget,temps_limite,centres_fixes_initiaux)
                              #                     # sol.print(instance)
                              #                     # print("Budget1 : ",self.Budget)
                              #                     qtt_manquante__moyenne += sol.objective_value
                              #                     # print(" qtt manquante totale : ",qtt_manquante__moyenne)
                              # # print("nb scenarios : ",nb_scenarios)
                              # qtt_manquante__moyenne = qtt_manquante__moyenne/nb_scenarios
                              # # print("La quantité manquante moyenne est : ", qtt_manquante__moyenne)
                         
                    # if affichage == True :
                    #     sol.print(instance)
                    return qtt_manquante__moyenne
               else :
                    print("ERREUR : {} n'est pas compris. il faut écrire True ou False".format(self.sol_init)) # ici c'est si on met une solution initiale avec des centres fixes déjà construits
          elif self.solveur == "GUROBI" :
               print("pas encore fait")
          elif self.solveur == "LocalSolver" :
               print("pas encore fait")
          elif self.solveur == "CPLEX" :
               print("pas encore fait")
          else :
               print("Le solver n'est pas reconnu. Essayer avec les solvers CBC, GUROBI, LocalSolver, ou CPLEX")

         




    
                

# Budget = 20000000
# datafileName = 'data_ter/1/1_22_22_2_50'

# sol = Modelize("CBC",False,datafileName,Budget,"worst_case").solve(True,30)
# #model( solveur, solu initiale, instance, budget, cas).solve(afficher solutions, temps limite)

# datafileName = 'data_ter/1/1_22_22_2_18'
# Budget = 200000
# temps_limite = 30
# instance = read_data(datafileName,"average_case",True,Budget,temps_limite)
# read_data(datafileName,"average_case",True,Budget,temps_limite)
# datafileName,cas,sol_init,Budget,temps_limite
# instance.print()


# on n'utilise pas les centres mobiles à la deuxième période, pk ? regarder si c pcq que on a utilisé toute la capacité donneurs
# #on positionne des centres mobiles mais on ne les utilise pas tous : pk ? est ce qu'on force à mettre un centre à chaque localisation?
# datafileName = 'data_ter/1/1_22_22_2_18'
# # # datafileName = 'data_ter/5/5_50_50_5_18'
# Budget = 20000000
# temps_limite = 30
# sol = Modelize("CBC",False,datafileName,Budget,"all").solve(False,30)

# instance = read_data(datafileName,"best_case",False,Budget,temps_limite)
# (datafileName,cas,sol_init,Budget,temps_limite)
# # print("######################")
# print("checker : ",Checker(sol,instance))
# #model( solveur, solu initiale, instance, budget, cas).solve(afficher solutions, temps limite)