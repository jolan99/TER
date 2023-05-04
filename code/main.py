from read_instance import *
from class_model import *
# from class_model
from class_solution import *
from TERmodele1 import *
from checker import *
import pandas as pd
#import streamlit as st

# # datafileName = 'data_ter/1/1_22_22_2_18'
# datafileName = 'data_ter/1/1_22_22_2_50'
# # datafileName = 'data_ter/3/3_22_22_2_50'
# # datafileName = 'data_ter/5/5_50_50_5_18'
# Budget = 20000000
# temps_limite = 30
# sol = Modelize("CBC",False,datafileName,Budget,"best_case").solve(True,temps_limite)
# # sol = Modelize("CBC",True,datafileName,Budget,0.9).solve(True,temps_limite)

# instance = read_data(datafileName,"best_case",False,Budget,temps_limite)
# df = pd.DataFrame(instance.hospitals_locations)
# locations = pd.DataFrame(instance.locations)


# centresfixes = pd.DataFrame(columns = ["lat","lon"])
# print(centresfixes)
# for l in range(instance.nb_locations):
#     for f in range(instance.nb_locations):
#         if(sol.centres_f[f][l] == 1):
#             print("#####",instance.locations[l])
#             loc1 = pd.DataFrame([instance.locations[l][0]],columns = ["lat"])
#             print("#########",loc1)
#             loc1 = loc1.assign(lon=[instance.locations[l][1]])
#             # loc1.insert(column = "lon",value =instance.locations[l][1])
#             # print("#########",loc2)
#             # loc = pd.concat(loc1,loc2,axis=1)
#             print("#########",loc1)
#             # centresfixes = centresfixes.append(pd.concat(pd.DataFrame(instance.locations[l][0]),pd.DataFrame(instance.locations[l][1])),ignore_index=True)
#             centresfixes = centresfixes.append(loc1,ignore_index=True)



# with open('solutions.txt', 'w') as f:
#     dfAsString = df.to_string(header=False, index=False)
#     f.write(dfAsString)

# with open('centres_fixes.txt', 'w') as f:
#     dfAsString = centresfixes.to_string(header=False, index=False)
#     f.write(dfAsString)

# # with open('centres_mobiles.txt', 'w') as f:
# #     dfAsString = df.to_string(header=False, index=False)
# #     f.write(dfAsString)

# with open('localisations.txt', 'w') as f:
#     dfAsString = locations.to_string(header=False, index=False)
#     f.write(dfAsString)
# # instance = read_data(datafileName,"best_case",True,Budget,temps_limite)
# # instance = read_data(datafileName,"average_case",True,Budget,temps_limite)
# # print("checker : ",Checker(sol,instance))

# # map_data = pd.DataFrame(df,columns=['lat', 'lon'])
# # st.map(map_data)

## on veut faire tourner sur les quatre cas et afficher dans un fichier : 

fichier = open("resulats.txt", "w")
fichier.write("Nom de l'instance;best_case;average_case;worst_case;all_scenarios;999%;90%;80%;70%;60%;50%;40%;30%;20%;10%;worst_case;best_case;average_case")

#for datafileName in('data_ter/1/1_22_22_2_18','data_ter/1/1_22_22_2_50','data_ter/1/1_22_22_3_18','data_ter/1/1_22_22_3_50','data_ter/1/1_22_22_3_18','data_ter/2/2_22_22_2_18','data_ter/2/2_22_22_2_50'):
for datafileName in('data_ter/1/1_22_22_2_18','data_ter/1/1_22_22_2_50'):

    print("debug : ",datafileName)

    Budget = 20000000
    temps_limite = 30
    fichier.write("\n")
    fichier.write(datafileName[-12:])
    for cas in ("best_case","average_case","worst_case"):
        print(f"calcul de {cas} en cours ...")
        sol = Modelize("CBC",False,datafileName,Budget,cas).solve(False,30)
        fichier.write(";")
        fichier.write(str(sol.objective_value))
    sol = Modelize("CBC",False,datafileName,Budget,"all").solve(False,30)
    fichier.write(";")
    fichier.write(str(sol))
    sol = Modelize("CBC",True,datafileName,Budget,[0.999,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,"worst_case","best_case","average_case"]).solve(False,30)
    print("La sol  moyenne est " ,sol)
    for i in range(len(sol)):
        fichier.write(";")
        fichier.write(str(sol[i]))



# instance = read_data(datafileName,"best_case",False,Budget,temps_limite)

fichier.close()


# fichier = open("resulats.txt", "w")
# fichier.write("Nom de l'instance;best_case;average_case;worst_case;all_scenarios;0.999%;0.9%;0.8%;0.5%")

# datafileName='data_ter/1/1_22_22_2_18'
# print("debug : ",datafileName)

# Budget = 20000000
# temps_limite = 30
# fichier.write("\n")
# fichier.write(datafileName[-12:])
# # for cas in ("best_case","average_case","worst_case"):
# #     print(f"calcul de {cas} en cours ...")
# #     sol = Modelize("CBC",False,datafileName,Budget,cas).solve(False,30)
# #     fichier.write(";")
# #     fichier.write(str(sol.objective_value))
# # sol = Modelize("CBC",False,datafileName,Budget,"all").solve(False,30)
# # fichier.write(";")
# # fichier.write(str(sol))
# sol = Modelize("CBC",True,datafileName,Budget,["worst_case",0.9,"best_case"]).solve(False,30)
# print("La sol est " ,sol)
# for i in range(len(sol)):
#         fichier.write(";")
#         fichier.write(str(sol[i]))



# # instance = read_data(datafileName,"best_case",False,Budget,temps_limite)



