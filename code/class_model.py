# from read_instance import *
from read_instance import *
from modele_avec_sol_ini import *
from TERmodele1 import *
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
                    sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                    # Checker(sol,instance)
                    # print("checker : ",Checker(sol,instance))
                    if affichage == True :
                        sol.print(instance)
                    return sol
               elif self.sol_init == True:
                    instance, centres_fixes_initiaux = read_data(self.datafileName,self.cas,self.sol_init,self.Budget,temps_limite)
                    sol, runtime = Model2_CBC_sol_ini(instance,self.Budget,temps_limite,centres_fixes_initiaux)
                    if affichage == True :
                        sol.print(instance)
                    return sol
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
