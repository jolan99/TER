from read_instance import *
from class_model import *
# from class_model
from class_solution import *
from TERmodele1 import *
from checker import *
import pandas as pd
import streamlit as st

datafileName = 'data_ter/1/1_22_22_2_18'
# datafileName = 'data_ter/3/3_22_22_2_50'
# datafileName = 'data_ter/5/5_50_50_5_18'
Budget = 20000000
temps_limite = 30
sol = Modelize("CBC",False,datafileName,Budget,"best_case").solve(True,temps_limite)
# sol = Modelize("CBC",True,datafileName,Budget,0.9).solve(True,temps_limite)

instance = read_data(datafileName,"best_case",False,Budget,temps_limite)
df = pd.DataFrame(instance.hospitals_locations)
locations = pd.DataFrame(instance.locations)


centresfixes = pd.DataFrame(columns = ["lat","lon"])
print(centresfixes)
for l in range(instance.nb_locations):
    for f in range(instance.nb_locations):
        if(sol.centres_f[f][l] == 1):
            print("#####",instance.locations[l])
            loc1 = pd.DataFrame([instance.locations[l][0]],columns = ["lat"])
            print("#########",loc1)
            loc1 = loc1.assign(lon=[instance.locations[l][1]])
            # loc1.insert(column = "lon",value =instance.locations[l][1])
            # print("#########",loc2)
            # loc = pd.concat(loc1,loc2,axis=1)
            print("#########",loc1)
            # centresfixes = centresfixes.append(pd.concat(pd.DataFrame(instance.locations[l][0]),pd.DataFrame(instance.locations[l][1])),ignore_index=True)
            centresfixes = centresfixes.append(loc1,ignore_index=True)



with open('solutions.txt', 'w') as f:
    dfAsString = df.to_string(header=False, index=False)
    f.write(dfAsString)

with open('centres_fixes.txt', 'w') as f:
    dfAsString = centresfixes.to_string(header=False, index=False)
    f.write(dfAsString)

# with open('centres_mobiles.txt', 'w') as f:
#     dfAsString = df.to_string(header=False, index=False)
#     f.write(dfAsString)

with open('localisations.txt', 'w') as f:
    dfAsString = locations.to_string(header=False, index=False)
    f.write(dfAsString)
# instance = read_data(datafileName,"best_case",True,Budget,temps_limite)
# instance = read_data(datafileName,"average_case",True,Budget,temps_limite)
# print("checker : ",Checker(sol,instance))

# map_data = pd.DataFrame(df,columns=['lat', 'lon'])
# st.map(map_data)

