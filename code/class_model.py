from read_instance import *
from TERmodele1 import *
from checker import *

# import time
class model:
    def __init__(self,solveur,sol_init,datafileName,Budget,cas):
          self.solveur = solveur
          self.sol_init = sol_init
          self.datafileName = datafileName
          self.Budget = Budget
          self.cas = cas
    def solve(self,affichage,temps_limite): 
          instance = read_data(self.datafileName,self.cas)
          if self.solveur == "CBC" :
               if self.sol_init == False:
                    sol, runtime = Model1_CBC(instance,self.Budget,temps_limite)
                    # Checker(sol,instance)
                    # print("checker : ",Checker(sol,instance))
                    if affichage == True :
                        sol.print(instance)
                    return sol
               else :
                    print("pas encore fait") # ici c'est si on met une solution initiale avec des centres fixes déjà construits
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

#model("CBC",False,datafileName,Budget,"worst_case").solve(True,30)
#model( solveur, solu initiale, instance, budget, cas).solve(afficher solutions, temps limite)