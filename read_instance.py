import numpy as np
datafileName = 'data_ter/1/1_22_22_2_18/deterministic.txt'
with open(datafileName, "r") as file:
    # lecture de la 1ère ligne et séparation des éléments de la ligne
    # dans un tableau en utilisant l'espace comme séparateur
    #1ere ligne
    line = file.readline()  
    lineTab = line.split()
    nb_hospitals = int(lineTab[0])
    nb_locations = int(lineTab[1])
    nb_donors = int(lineTab[2])
    time_horizon = int(lineTab[3])
    print("nb hôpitaux : ", nb_hospitals, "nb localisations : ", nb_locations, "nb periodes :", time_horizon)
    #2eme ligne
    line = file.readline()  
    lineTab = line.split()
    capacity_perm_facility = lineTab[0]
    capacity_temp_facility = lineTab[1]
    print("capacité centres temporaires : ",capacity_temp_facility ,"capacité centres fixes : ",capacity_perm_facility)
    #3eme ligne 
    line = file.readline()  
    lineTab = line.split()
    Capacity_hospital = []
    for h in range(nb_hospitals):
        Capacity_hospital.append(int(lineTab[h])) 
    print("capacité stockage hôpitaux : ",Capacity_hospital)
    #4eme ligne 
    line = file.readline()  
    lineTab = line.split()
    cost_perm_facility = float(lineTab[0])
    cost_temp_facility = float(lineTab[1])
    cost_moving_facility = float(lineTab[2])
    # 5eme ligne 
    line = file.readline()  
    lineTab = line.split()
    collection_cost = float(lineTab[0])
    storage_cost = float(lineTab[1])
    transportation_cost = float(lineTab[2])
    print("coût du transport : ", transportation_cost, "storage_cost : ", storage_cost, "collection cost : ", collection_cost)
    # 6 eme ligne : 
    supply_donor_group = []
    for d in range(nb_donors):
        line = file.readline()  
        lineTab = line.split()
        supply_donor_group.append(float(lineTab[0])) 
    print("capacité groupes de donneurs : ", supply_donor_group)
    # 7eme étape :
    locations = np.zeros((nb_locations,2))
    for l in range(nb_locations):
        line = file.readline()  
        lineTab = line.split()
        locations[l][0] = float(lineTab[0])
        locations[l][1] = float(lineTab[1])
    print("localisations : ", locations)
    # 8eme étape : 
    locations_hospitals = np.zeros((nb_hospitals,2))
    for l in range(nb_hospitals):
        line = file.readline()  
        lineTab = line.split()
        locations_hospitals[l][0] = float(lineTab[0])
        locations_hospitals[l][1] = float(lineTab[1])
    print("localisatoins hôpitaux", locations_hospitals)