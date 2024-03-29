# # from class_model import *
# from read_instance import *
# from class_solution import *


def Checker(sol,instance):
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
        # print("il a été prélevé {} du groupe {} et de capacité {}".format(qtt_coll,d,instance.supply_donor_group[d]))
        if qtt_coll > instance.supply_donor_group[d] + 0.0000001: #on met un epsilon car on travaille avec des float, on accepte un écart
            print("ERREUR : il a été trop prélevé du groupe de donneurs {}".format(d))
            return False
        
    
    # stocks pas trop élevés
    for h in range(instance.nb_hospitals):
        for p in range(instance.time_horizon+1):
            if sol.stock[h][p] > instance.capacity_hospital[h] + 0.0000001 :
                print("ERREUR : Le stock de l'hôpital {} à la période {} est trop élevé".format(h,p))
                return False
    if float(sol.cost) > 20000000:
        print("ERREUR : le cout dépasse de {} le budget donné".format(float(sol.cost)-20000000))
        return False
    # on vérifie que Ihp est bien la quantité de sang manquante. 
    qtt_totale = 0
    besoin_total = 0
    for p in range(instance.time_horizon):
        for h in range(instance.nb_hospitals):
            for l in range(instance.nb_locations):
                qtt_totale += sol.qtt_recue_hosp[l][h][p]
            
            qtt_totale += sol.stock[h][0] # il sera en fait à 0 dans nos expérimentations 
            # print("qtt totale créée ",qtt_totale)
            besoin_total += instance.Need_hospital[h][p]
            
            # print("besoin total créé ",besoin_total)
    if besoin_total - qtt_totale > 0 : # == s'il n'y a pas eu assez de sang
        # print("sol.valeur_obj : ",sol.valeur_obj,"(besoin_total - qtt_totale)*1.1 : ",(besoin_total - qtt_totale)*1.1)
        # print("sol.valeur_obj : ",sol.valeur_obj,"(besoin_total - qtt_totale)*0.9 : ",(besoin_total - qtt_totale)*0.9)

        if (float(sol.valeur_obj) <= (besoin_total - qtt_totale)*0.09)or(float(sol.valeur_obj) >= (besoin_total - qtt_totale)*1.01 ) :
            print("ERREUR : la valeur de l'objectif est de {} mais devrait être de {}".format(sol.valeur_obj,(besoin_total - qtt_totale)))
            return False 
    
    # faire un checker : on ne peut pas envoyer de sang s'il n'y a pas de centre, et ça ne doit pas dépasser la capacité max
    
    
   

    return True
    
# # on n'utilise pas les centres mobiles à la deuxième période, pk ? regarder si c pcq que on a utilisé toute la capacité donneurs
# # #on positionne des centres mobiles mais on ne les utilise pas tous : pk ? est ce qu'on force à mettre un centre à chaque localisation?
# datafileName = 'data_ter/1/1_22_22_2_18'
# # # datafileName = 'data_ter/5/5_50_50_5_18'
# Budget = 20000000
# temps_limite = 30
# sol = Modelize("CBC",False,datafileName,Budget,"best_case").solve(False,30)

# instance = read_data(datafileName,"best_case",False,Budget,temps_limite)
# # (datafileName,cas,sol_init,Budget,temps_limite)
# # # print("######################")
# print("checker : ",Checker(sol,instance))
# # #model( solveur, solu initiale, instance, budget, cas).solve(afficher solutions, temps limite)