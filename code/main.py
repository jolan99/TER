from read_instance import *
from class_model import *
# from class_model
from class_solution import *
from TERmodele1 import *
from checker import *

datafileName = 'data_ter/1/1_22_22_2_18'
# datafileName = 'data_ter/5/5_50_50_5_18'
Budget = 20000000
temps_limite = 30
sol = Modelize("CBC",False,datafileName,Budget,"best_case").solve(True,temps_limite)
instance = read_data(datafileName,"best_case",False,Budget,temps_limite)
# instance = read_data(datafileName,"average_case",True,Budget,temps_limite)
print("checker : ",Checker(sol,instance))