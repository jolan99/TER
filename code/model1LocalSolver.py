from read_instance import *
import localsolver
import sys
import time

with localsolver .LocalSolver() as ls:
    m = ls.model

    Budget = 20000000
    datafileName = "data_ter/1/1_22_22_2_50"
    instance = read_data(datafileName,"average_case")

    #### déclaration des variables : 

    #gam[instance.nb_locations][instance.nb_locations][instance.time_horizon] = bool()
    gam1 = [[m.bool() for p in range(instance.time_horizon)]for l in range(instance.nb_locations)]
    gam = [[[m.bool() for p in range(instance.time_horizon)] for l in range(instance.nb_locations)] for m in range(instance.nb_locations)]

    alpha = [[m.int(0,1) for l in range(instance.nb_locations)]for f in range(instance.nb_locations)]

    y = [[[m.int(0,1)for d in range(instance.nb_donors)]for p in range(instance.time_horizon)]for l in range(instance.nb_locations)]
    
    s = [[m.int(0,1) for p in range(instance.time_horizon + 1)]for h in range(instance.nb_hospitals)]

    I = [[m.int(0,1) for p in range(instance.time_horizon)]for h in range(instance.nb_hospitals)]

    #### contraintes

    #coût : 
    m.constraint(m.sum(
        instance.collection_cost
        * m.sum(
            m.sum(x[l][p][d] for d in range(instance.nb_donors))
            for l in range(instance.nb_locations)
        )
        for p in range(instance.time_horizon)
    )
    + m.sum(
        m.sum(
            instance.cost_temp_facility * gam[m][l][0]
            for m in range(instance.nb_locations)
        )
        for l in range(instance.nb_locations)
    )
    + m.sum(
        m.sum(
            instance.cost_perm_facility * alpha[f][l]
            for f in range(instance.nb_locations)
        )
        for l in range(instance.nb_locations)
    )
    + m.sum(
            m.sum(
                s[h][p + 1] * instance.storage_cost
                for p in range(instance.time_horizon)
            )
        for h in range(instance.nb_hospitals)
    )
    + m.sum(
        m.sum(
            m.sum((y[l][h][p]* instance.dis_loc_hosp[h][l]* instance.transportation_cost) for l in range(instance.nb_locations))
            for h in range(instance.nb_hospitals)
        )
        for p in range(instance.time_horizon)
    )
    + m.sum(
        m.sum(
            m.sum(
                m.sum(
                    instance.dist_locations[l][lbis]*(
                        gam[m][lbis][p + 1]
                        - m.sum(gam[m][k][p] for k in range(instance.nb_locations))
                        + gam[m][l][p]
                    )
                    for lbis in range(instance.nb_locations)
                )
                for l in range(instance.nb_locations)
            )
            for m in range(instance.nb_locations)
        )
        for p in range(instance.time_horizon-1)
    )
    * instance.cost_moving_facility
    <= Budget)

    # Un seul centre par localisation à chaque période
for l in range(instance.nb_locations):
    for p in range(instance.time_horizon):
        m.constraint(
            m.sum(gam[m][l][p] for m in range(instance.nb_locations)) +
            m.sum(alpha[f][l] for f in range(instance.nb_locations))
            <= 1
        )

    # Un centre mobile ne peut être positionné qu'à une seule localisation
    for m in range(instance.nb_locations):
        for p in range(instance.time_horizon):
            m.constraint(
                m.sum(gam[m][l][p] for l in range(instance.nb_locations)) <= 1
            )
    # un centre fixe ne peut être positionné qu'à une seule localisation
    for f in range(instance.nb_locations):
        m.constraint(m.sum(alpha[f][l] for l in range(instance.nb_locations)) <= 1)

    # Si un centre mobile est utilisé, il l'est depuis la période 1 :
    for m in range(instance.nb_locations):
        for p in range(instance.time_horizon - 1):
            m.constraint(
                m.sum(gam[m][l][p+1] for l in range(instance.nb_locations))
                == gam[m][l][p]
            )

    # On ne peut pas collecter plus que ce que les donneurs peuvent donner
    for d in range(instance.nb_donors):
        m.constraint(
            m.sum(
                m.sum(x[l][p][d] for p in range(instance.time_horizon))
                for l in range(instance.nb_locations)
            )
            <= instance.supply_donor_group[d]
        )

    # Un centre ne peut pas collecter plus que sa capacité max
    for l in range(instance.nb_locations):
        for p in range(instance.time_horizon):
            m.constraint(
                m.sum(x[l][p][d] for d in range(instance.nb_donors))
                <= instance.capacity_temp_facility
                * m.sum(gam[m][l][p] for m in range(instance.nb_locations))
                + instance.capacity_perm_facility
                * m.sum(alpha[f][l] for f in range(instance.nb_locations))
            )

    # On ne peut pas envoyer à un hôpital plus que ce qui a été collecté
    for l in range(instance.nb_locations):
        for p in range(instance.time_horizon):
            m.constraint(
                m.sum(y[l][h][p] for h in range(instance.nb_hospitals))
                <= m.sum(x[l][p][d] for d in range(instance.nb_donors))
            )

    # on fixe le stock et la quantité de sang manquante : 
    for h in range(instance.nb_hospitals):
        for p in range(instance.time_horizon):
            m.constraint((I[h][p] - s[h][p]) >= (instance.Need_hospital[h][p] - m.sum(y[l][h][p] for l in range(instance.nb_locations)) - s[h][p-1]))

    # le stock ne peut pas excéder le stock max des hôpitaux
    for h in range(instance.nb_hospitals):
        for p in range(instance.time_horizon):
            m.constraint(s[h][p] <= instance.capacity_hospital[h]) 

    #on met à 0 le stock initial : 
    for h in range(instance.nb_hospitals):
        m.constraint(s[h][0] == 0)
    
    
    ####  objectif 

    m.minimize(m.sum(m.sum(I[h][p] for p in range(instance.time_horizon)))for h in range(instance.nb_hospitals))

    m.close()
    start = time.perf_counter()
    runtime = time.perf_counter() - start
    if len(sys.argv) >= 3:
        ls.param.time_limit = int(sys.argv[2])
    else:
        ls.param.time_limit = 2
    ls.solve()
    print("Solution calculée")
    for l in range(instance.nb_locations):
        for p in range(instance.time_horizon):
            for m in range(instance.nb_locations):
                if gam[m][l][p].value == 1 :
                  print("Un centre mobile est placé à la localisation {},{} à la période {}".format(instance.locations[l][0],instance.locations[l][0],p))
        for f in range(instance.nb_locations):
            if alpha[f][l].value == 1:
                    print("Un centre fixe est construit à la localisation {},{} ".format(instance.locations[l][0],instance.locations[l][0]))

    valeur = (sum(
        instance.collection_cost
        * sum(
            sum(x[l][p][d].x for d in range(instance.nb_donors))
            for l in range(instance.nb_locations)
        )
        for p in range(instance.time_horizon)
    )
    + sum(
        sum(
            instance.cost_temp_facility * gam[m][l][0].value
            for m in range(instance.nb_locations)
        )
        for l in range(instance.nb_locations)
    )
    + sum(
        sum(
            instance.capacity_perm_facility * alpha[f][l].value
            for f in range(instance.nb_locations)
        )
        for l in range(instance.nb_locations)
    )
    + sum(
        (
            sum(
                s[h][p + 1].value * instance.storage_cost
                for p in range(instance.time_horizon)
            )
        )
        for h in range(instance.nb_hospitals)
    )
    + sum(
        sum(
            sum(y[l][h][p].value for l in range(instance.nb_locations))
            * instance.transportation_cost
            * instance.dis_loc_hosp[h][l]
            for h in range(instance.nb_hospitals)
        )
        for p in range(instance.time_horizon)
    )
    + sum(
        sum(
            sum(
                sum(
                    instance.dist_locations[l][lbis]*(
                        gam[lbis][m][p + 1].value
                        - sum(gam[k][m][p].value for k in range(instance.nb_locations))
                        + gam[l][m][p].value
                    )
                    for lbis in range(instance.nb_locations)
                )
                for l in range(instance.nb_locations)
            )
            for m in range(instance.nb_locations)
        )
        for p in range(instance.time_horizon-1)
    )
    * instance.cost_moving_facility)

    print("Coût des décisions : ", valeur)
    print("quantité de sang manquante : ", ls.solution.get_objective_bound(0))
    



