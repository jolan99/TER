from read_instance import *
from TERmodele1 import *
from mip import *
import time
class model:
    def __init__(self,solveur,sol_init,datafileName,Budget,cas):
            self.solveur = solveur
            self.sol_init = sol_init
            self.datafileName = datafileName
            self.Budget = Budget
            self.cas = cas
    def solve(self):
          if self.solveur == "CBC" :
               if self.sol_init == False:
                    return Model1_CBC(self.datafileName,self.Budget,self.cas)


    
                

Budget = 20000000
datafileName = 'data_ter/1/1_22_22_2_50'
#instance = read_data(datafileName,)
modele = model("CBC",False,datafileName,Budget,"worst_case")
sol = modele.solve()
#sol.print(instance)