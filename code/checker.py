from class_model import *
from read_instance import *
from class_solution import *


def checker(sol,instance):
    # un seul centre par localisation 
    for p in range(instance.time_horizon):
        for l in range(instance.nb_locations):
            nb_centres = 0
            for m in range(instance.nb_locations):
                if sol.centres_m[m][l][p] == 1 :
                    nb_centres += 1
            for f in range(instance.nb_locations):
                if sol.centres_f[f][l] == 1 :
                    nb_centres += 1
            if nb_centres >= 2 : 
                print("ERREUR : Plusieurs centres sont dans mis à la même localisation : ", instance.locations[l])
                return False
    
    
    # un centre n'est utilisé qu'une seule fois par période
    for m in range(instance.nb_locations):
        
        for p in range(instance.time_horizon):
            
            nb_utilisation = 0
            for l in range(instance.nb_locations):
                if sol.centres_m[m][l][p] == 1 :
                    nb_utilisation += 1
            if nb_utilisation >= 2 : 
                print("ERREUR : Le centre mobile {} est utilisé {} fois à la période {}".format(m,nb_utilisation,p+1))
                return False

    # un centre ne peut pas être à différentes localisations : 
    for p in range(instance.time_horizon):
        for m in range(instance.nb_locations):
            nb_loca = 0
            for l in range(instance.nb_locations):
                if sol.centres_m[m][l][p] == 1 :
                    nb_loca += 1
            if nb_loca >= 2:
                print("ERREUR : Le centre mobile {} est utilisé dans {} localisations différentes".format(m,nb_loca))
                return False
    for f in range(instance.nb_locations):
        nb_loca = 0
        for l in range(instance.nb_locations):
            if sol.centres_f[f][l] == 1 :
                nb_loca += 1
        if nb_loca >= 2:
            print("ERREUR : Le centre fixe {} est utilisé dans {} localisations différentes".format(f,nb_loca))
            return False

    # qtt envoyées depuis une localisation égales à ce qui y a été collecté 
   
    for p in range(instance.time_horizon):
        qtt_recue = 0 # qtt envoyée depuis l
        qtt_coll = 0 # qtt collectée à l
        for l in range(instance.nb_locations):
            for h in range(instance.nb_hospitals):
                qtt_recue += sol.qtt_recue_hosp[l][h][p] 
            for d in range(instance.nb_donors):
                qtt_coll += sol.qtt_collect[l][p][d]
            if ((qtt_coll - qtt_recue) >0.00001)or ((qtt_coll - qtt_recue) <-0.00001): #on met un epsilon car on travaille avec des float, on accepte un écart
                # print("qtt coll" , qtt_coll, " qtt recue ", qtt_recue, qtt_recue-qtt_coll)
                print("ERREUR : La localisation {} n'envoie pas la bonne quantité de sang à la période {}".format(l,p+1))
                return False

    # qtt prélevées <= ce que les donneurs peuvent donner 
    for d in range(instance.nb_donors):
        qtt_coll = 0
        for p in range(instance.time_horizon):
            for l in range(instance.nb_locations):
                qtt_coll += sol.qtt_collect[l][p][d]
        if qtt_coll > instance.supply_donor_group[d] + 0.0000001: #on met un epsilon car on travaille avec des float, on accepte un écart
            print("ERREUR : il a été trop prélevé du groupe de donneurs {}".format(d))
            return False
        
    
    # stocks pas trop élevés
    for h in range(instance.nb_hospitals):
        for p in range(instance.time_horizon+1):
            if sol.stock[h][p] > instance.capacity_hospital[h] + 0.0000001 :
                print("ERREUR : Le stock de l'hôpital {} à la période {} est trop élevé".format(h,p))
                return False

    # on vérifie que Ihp est bien la quantité de sang manquante. 
    qtt_totale = 0
    besoin_total = 0
    for p in range(instance.time_horizon):
        for h in range(instance.nb_hospitals):
            for l in range(instance.nb_locations):
                qtt_totale += sol.qtt_recue_hosp[l][h][p]
            qtt_totale += sol.stock[h][0] # il sera en fait à 0 dans nos expérimentations 
            besoin_total += instance.Need_hospital[h][p]
    if besoin_total - qtt_totale > 0 : # == s'il n'y a pas eu assez de sang
        if (float(sol.objective_value) <= (besoin_total - qtt_totale)-0.0001 )or(float(sol.objective_value) >= (besoin_total - qtt_totale)+0.0001 ) :
            print("ERREUR : la valeur de l'objectif est de {} mais devrait être de {}".format(sol.objective_value,(besoin_total - qtt_totale)))
            return False 

        

    return True
    

datafileName = 'data_ter/1/1_22_22_2_50'

sol = model("CBC",False,datafileName,Budget,"worst_case").solve(True,30)
instance = read_data(datafileName,"worst_case")
print("######################")
print("checker : ",checker(sol,instance))
##model( solveur, solu initiale, instance, budget, cas).solve(afficher solutions, temps limite)