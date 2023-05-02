import streamlit as st
import pandas as pd


# Charger le fichier dans un dataframe pandas
df = pd.read_csv('solutions.txt', sep='\s+', header=None,names=["lat","lon"])
localisations = pd.read_csv('localisations.txt', sep='\s+', header=None,names=["lat","lon"])
centres_fixes=pd.read_csv('centres_fixes.txt', sep='\s+', header=None,names=["lat","lon"])
# map_data = pd.DataFrame(df,columns=['lat', 'lon'])
# Supprimer la première colonne (index)
# df = df.drop(columns=[0])


# Extraire les valeurs de lat et lon dans un nouveau dataframe
# nouveau_df = pd.DataFrame({'lat': [df.iloc[0,1]], 'lon': [df.iloc[0,2]]})

st.write(df)
# df["lat"] = df["lat"].astype(float)
# df["lon"] = df["lon"].astype(float)
# map_data = pd.DataFrame(df)
# essai = pd.concat([localisations,centres_fixes],axis=1,keys =["lat","lon"])
st.map(df)
st.map(localisations)
st.map(centres_fixes)
# st.write(essai)
# st.map(essai)





# import pandas as pd
# import sys 
# # sys.path.insert(0,"C:\\Users\\Anna\\Documents\\M1 ROAD\\S8\\TER\\code")
# # import read_instance

# # set PYTHONPATH = "C:\\Users\\Anna\\Documents\\M1 ROAD\\S8\\TER\\code"
# # from code.read_instance import *



# datafileName = 'data_ter/1/1_22_22_2_18'
# Budget = 200000
# temps_limite = 30
# # instance = read_data(datafileName,"average_case",True,Budget,temps_limite)

# st.write("st map :")
# map_data = pd.DataFrame(
#     instance.hospitals_locations)
# # map_data = pd.DataFrame(
# #     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
# #     columns=['lat', 'lon'])
# # map_data = pd.DataFrame([[44.1868 ,-0.42867],[45.5558,-1.08882],[44.5241,1.53281]],columns=['lat', 'lon'])
# st.map(map_data)