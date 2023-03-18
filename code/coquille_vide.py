from class_model import *
from checker import *
#dans un premier temps, on considère : 
    # qu'il n'y a qu'un seul hôpital 
    # Qu'une seule période ( donc deux en comptant la période 0)
    # 1 seule localisation 
    # l'hôpital a besoin de 1000 unités de sang à la période 1 
    # les centres fixes peuvent collecter 800 et les mobiles 400, il devrait rester 200  : 
    # le budget est de 1000, cout de centre fixe = 300, cout centre mobile = 100
    # tous les autrs coûts sont mis à 0 

    #on s'attend à avoir un centre fixe placé à l'unique localisation, et à manquer de 200 d'unités de sang
nb_hospitals = 1
nb_locations = 1
time_horizon = 1
nb_donors = 1
capacity_perm_facility = 800
capacity_temp_facility = 400
capacity_hospital = [0]
cost_perm_facility = 300
cost_temp_facility = 100
cost_moving_facility = 0
collection_cost = 0
storage_cost = 0
transportation_cost = 0
supply_donor_group = [1000]
locations = [[1,1]]
hospitals_locations = [[1,2]]
Need_hospital = [[1000]]
valid = True


instance = data(
        nb_hospitals,
        nb_locations,
        nb_donors,
        time_horizon,
        capacity_perm_facility,
        capacity_temp_facility,
        capacity_hospital,
        cost_perm_facility,
        cost_temp_facility,
        cost_moving_facility,
        collection_cost,
        storage_cost,
        transportation_cost,
        supply_donor_group,
        locations,
        hospitals_locations,
        Need_hospital,
        valid
    )
sol,runtime = Model1_CBC(instance,1000,30)
sol.print(instance)
print("checker : ",checker(sol,instance))