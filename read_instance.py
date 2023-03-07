import numpy as np
from math import *

class data : 
    def __init__(self,nb_hospitals,nb_locations,nb_donors,time_horizon,capacity_perm_facility, capacity_temp_facility, capacity_hospital,cost_perm_facility,cost_temp_facility, cost_moving_facility, collection_cost, storage_cost, transportation_cost, supply_donor_group, locations, hospitals_locations) :
        self.nb_hospitals = nb_hospitals
        self.nb_locations = nb_locations
        self.nb_donors = nb_donors
        self.time_horizon = time_horizon
        self.capacity_perm_facility = capacity_perm_facility
        self.capacity_temp_facility = capacity_temp_facility
        self.capacity_hospital = capacity_hospital
        self.cost_perm_facility = cost_perm_facility
        self.cost_temp_facility = cost_temp_facility
        self.cost_moving_facility = cost_moving_facility
        self.collection_cost = collection_cost
        self.storage_cost = storage_cost
        self.transportation_cost = transportation_cost
        self.supply_donor_group = supply_donor_group
        self.locations = locations 
        self.hospitals_locations = hospitals_locations

        # ici on calcule la matrice des distances entre les localisations
        dist_locations = np.zeros((self.nb_locations,self.nb_locations))
        for locationA in range(self.nb_locations):
            for locationB in range(self.nb_locations):
                dist_locations[locationA][locationB] = LatLongToKm(self.locations[locationA][0],self.locations[locationA][1],self.locations[locationB][0],self.locations[locationB][1])
        # et ici la matrice des distances entre les localisations et les hôpitaux 
        dist_loc_hosp = np.zeros((nb_hospitals,nb_locations))
        for h in range(self.nb_hospitals):
            for L in range(self.nb_locations):
                dist_loc_hosp[h][L] = LatLongToKm(self.locations[L][0],self.locations[L][1],self.hospitals_locations[h][0],self.hospitals_locations[h][1])

        self.dist_locations = dist_locations
        self.dis_loc_hosp = dist_loc_hosp



    def print(self):
        print("########## Blood supply chain instance ##########")
        print("nb hôpitaux : ", self.nb_hospitals, "nb localisations : ", self.nb_locations, "nb periodes :", self.time_horizon)
        print("capacité centres temporaires : ",self.capacity_temp_facility ,"capacité centres fixes : ",self.capacity_perm_facility)
        print("capacité stockage hôpitaux : ",self.capacity_hospital)
        print("coût du transport : ", self.transportation_cost, "storage_cost : ", self.storage_cost, "collection cost : ", self.collection_cost)
        print("capacité groupes de donneurs : ", self.supply_donor_group)
        print("localisations : ", self.locations)
        print("localisatoins hôpitaux", self.hospitals_locations)
        print("matrice des distances entre les localisations : " )
        print(self.dist_locations)
        print("matrice des distances entre les hôpitaux et les localisations : " )
        print(self.dis_loc_hosp)





#print(LatLongToKm(44.0335, -0.90008,43.4569, 1.27299))
# on obtient 243.304017164605 alors que par les routes c'est 213 km
#print(LatLongToKm(43.4569, 1.27299,43.4569, 1.27299))

def LatLongToKm(LatitudeA,LongitudeA,LatitudeB,LongitudeB):
    x = (LongitudeB - LongitudeA) * cos ((LatitudeA + LatitudeB)/2)
    y = LatitudeB- LatitudeA 
    z = sqrt(x**2 + y**2)
    #print("z: ",z)
    dist = 1.852 * 60 * z 
    return dist 

def read_data(datafileName):
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
        #2eme ligne
        line = file.readline()  
        lineTab = line.split()
        capacity_perm_facility = lineTab[0]
        capacity_temp_facility = lineTab[1]
        #3eme ligne 
        line = file.readline()  
        lineTab = line.split()
        capacity_hospital = []
        for h in range(nb_hospitals):
            capacity_hospital.append(int(lineTab[h])) 
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
        # 6 eme ligne : 
        supply_donor_group = []
        for d in range(nb_donors):
            line = file.readline()  
            lineTab = line.split()
            supply_donor_group.append(float(lineTab[0])) 
        # 7eme étape :
        locations = np.zeros((nb_locations,2))
        for l in range(nb_locations):
            line = file.readline()  
            lineTab = line.split()
            locations[l][0] = float(lineTab[0])
            locations[l][1] = float(lineTab[1])
        # 8eme étape : 
        hospitals_locations = np.zeros((nb_hospitals,2))
        for l in range(nb_hospitals):
            line = file.readline()  
            lineTab = line.split()
            hospitals_locations[l][0] = float(lineTab[0])
            hospitals_locations[l][1] = float(lineTab[1])
    instance = data(nb_hospitals,nb_locations,nb_donors,time_horizon,capacity_perm_facility, capacity_temp_facility, capacity_hospital,cost_perm_facility,cost_temp_facility, cost_moving_facility, collection_cost, storage_cost, transportation_cost, supply_donor_group, locations, hospitals_locations)
    return instance 

# datafileName = 'data_ter/1/1_22_22_2_18/deterministic.txt'
# instance = read_data(datafileName)
# instance.print()
