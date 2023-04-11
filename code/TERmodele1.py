from read_instance import *
from class_solution import *
from mip import *
import time



def Model1_CBC(instance,Budget,temps_limite):
    model = Model(name="Blood_supply_chain", solver_name="CBC")
    model.verbose = False # on ne veut pas de détails 

    # b = [[model.add_var(name="b(" + str(h) + str(p)+")", lb = 0, ub=0,var_type=BINARY) for p in range(instance.time_horizon)]for h in range(instance.nb_hospitals)]
    if instance.valid == True :
        gam = [[
            [
                model.add_var(
                    name="Gamma(" + str(m) + str(l) +str(p)+ ")", lb=0, ub=1, var_type=BINARY
                )
                for p in range(instance.time_horizon)
            ]
            for l in range(instance.nb_locations)
        ]for m in range(instance.nb_locations)]

        alpha = [
            [
                model.add_var(
                    name="Alpha(" + str(f) + str(l) + ")", lb=0, ub=1, var_type=BINARY
                )
                for l in range(instance.nb_locations)
            ]
            for f in range(instance.nb_locations)
        ]
        y = [
            [
                [
                    model.add_var(
                        name="Y(" + str(l) + str(h) + str(p) + ")", lb=0, var_type=CONTINUOUS
                    )
                    for p in range(instance.time_horizon)
                ]
                for h in range(instance.nb_hospitals)
            ]
            for l in range(instance.nb_locations)
        ]
        x = [
            [
                [
                    model.add_var(
                        name="X(" + str(l) + str(p) + str(d) + ")", lb=0, var_type=CONTINUOUS
                    )
                    for d in range(instance.nb_donors)
                ]
                for p in range(instance.time_horizon)
            ]
            for l in range(instance.nb_locations)
        ]
        s = [
            [
                model.add_var(name="S(" + str(h) + str(p) + ")", lb=0, var_type=CONTINUOUS)
                for p in range(instance.time_horizon + 1)
            ]
            for h in range(instance.nb_donors)
        ]
        I = [
            [
                model.add_var(
                    name="I(" + str(h) + str(p) + ")",
                    lb=0,
                    var_type=CONTINUOUS,
                )
                for p in range(instance.time_horizon)
            ]
            for h in range(instance.nb_donors)
        ]

        model.objective = minimize(
            xsum(
                xsum(I[h][p] for p in range(instance.time_horizon))
                for h in range(instance.nb_hospitals)
            )
        )

        # coût :

        model.add_constr(
            xsum(
                instance.collection_cost
                * xsum(
                    xsum(x[l][p][d] for d in range(instance.nb_donors))
                    for l in range(instance.nb_locations)
                )
                for p in range(instance.time_horizon)
            )
            + xsum(
                xsum(
                    instance.cost_temp_facility * gam[m][l][0]
                    for m in range(instance.nb_locations)
                )
                for l in range(instance.nb_locations)
            )
            + xsum(
                xsum(
                    instance.cost_perm_facility * alpha[f][l]
                    for f in range(instance.nb_locations)
                )
                for l in range(instance.nb_locations)
            )
            + xsum(
                    xsum(
                        s[h][p + 1] * instance.storage_cost
                        for p in range(instance.time_horizon)
                    )
                for h in range(instance.nb_hospitals)
            )
            + xsum(
                xsum(
                    xsum((y[l][h][p]* instance.dis_loc_hosp[h][l]* instance.transportation_cost) for l in range(instance.nb_locations))
                    for h in range(instance.nb_hospitals)
                )
                for p in range(instance.time_horizon)
            )
            + xsum(
                xsum(
                    xsum(
                        xsum(
                            instance.dist_locations[l][lbis]*(
                                gam[m][lbis][p + 1]
                                - xsum(gam[m][k][p] for k in range(instance.nb_locations))
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
            <= Budget
        ,name="contrainte_budget")


        # Un seul centre par localisation à chaque période
        for l in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                model.add_constr(
                    xsum(gam[m][l][p] for m in range(instance.nb_locations)) +
                    xsum(alpha[f][l] for f in range(instance.nb_locations))
                    <= 1
                ,name="c1(" +str(l) + str(p)+")")

        # Un centre mobile ne peut être positionné qu'à une seule localisation
        for m in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                model.add_constr(
                    xsum(gam[m][l][p] for l in range(instance.nb_locations)) <= 1
                ,name="c2(" +str(m) + str(p)+")")

        # un centre fixe ne peut être positionné qu'à une seule localisation
        for f in range(instance.nb_locations):
            model.add_constr(xsum(alpha[f][l] for l in range(instance.nb_locations)) <= 1,name="c3(" +str(f)+")")

        # Si un centre mobile est utilisé, il l'est depuis la période 1 :
        for m in range(instance.nb_locations):
            for p in range(instance.time_horizon - 1):
                model.add_constr(
                    xsum(gam[m][l][p+1] for l in range(instance.nb_locations))
                    <= gam[m][l][p]
                ,name="c4(" +str(m) + str(p)+")")

        # On ne peut pas collecter plus que ce que les donneurs peuvent donner
        for d in range(instance.nb_donors):
            model.add_constr(
                xsum(
                    xsum(x[l][p][d] for p in range(instance.time_horizon))
                    for l in range(instance.nb_locations)
                )
                <= instance.supply_donor_group[d]
            ,name="c5(" + str(d)+")")

        # Un centre ne peut pas collecter plus que sa capacité max
        for l in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                model.add_constr(
                    xsum(x[l][p][d] for d in range(instance.nb_donors))
                    <= instance.capacity_temp_facility
                    * xsum(gam[m][l][p] for m in range(instance.nb_locations))
                    + instance.capacity_perm_facility
                    * xsum(alpha[f][l] for f in range(instance.nb_locations))
                ,name="c6(" +str(l) + str(p)+")")

        # On ne peut pas envoyer à un hôpital plus que ce qui a été collecté
        for l in range(instance.nb_locations):
            for p in range(instance.time_horizon):
                model.add_constr(
                    xsum(y[l][h][p] for h in range(instance.nb_hospitals))
                    == xsum(x[l][p][d] for d in range(instance.nb_donors))
                ,name="c7(" +str(l) + str(p)+")")

        # on fixe le stock et la quantité de sang manquante : 
        for h in range(instance.nb_hospitals):
            for p in range(instance.time_horizon):
                model.add_constr((I[h][p] - s[h][p+1] -instance.Need_hospital[h][p] + xsum(y[l][h][p] for l in range(instance.nb_locations)) + s[h][p]) == 0,name="c8(" +str(h) + str(p)+")")

        # on ne peut pas stocker plus que ce qu'on reçoit à l'hôpital
        for h in range(instance.nb_hospitals):
            for p in range(instance.time_horizon):
                model.add_constr(s[h][p+1] <= xsum(y[l][h][p] for l in range(instance.nb_locations))) 
        # le stock ne peut pas excéder le stock max des hôpitaux
        for h in range(instance.nb_hospitals):
            for p in range(instance.time_horizon+1):
                model.add_constr(s[h][p] <= instance.capacity_hospital[h],name="c9(" +str(h) + str(p)+")") 

        #on met à 0 le stock initial : 
        for h in range(instance.nb_hospitals):
            model.add_constr(s[h][0] == 0,name="c2(" + str(h)+")")

        #essais : 
        # for h in range(instance.nb_hospitals):
        #     for p in range(instance.time_horizon):
        #         model.add_constr(I[h][p] >= 0)
        #         model.add_constr(I[h][p] >= instance.Need_hospital[h][p] - xsum(y[l][h][p] for l in range(instance.nb_locations)) - s[h][p])
        #         model.add_constr(I[h][p] <= instance.Need_hospital[h][p]*(1-b[h][p]))
        #         model.add_constr(I[h][p] <= instance.Need_hospital[h][p] - xsum(y[l][h][p] for l in range(instance.nb_locations)) - s[h][p]+instance.Need_hospital[h][p]*b[h][p])

        start = time.perf_counter()
        status = model.optimize(max_seconds=temps_limite)
        runtime = time.perf_counter() - start


        # Ecrire le modèle
        model.write("Blood_supply_chain.lp")  # à décommenter si vous le souhaitez

        # Lancement du chronomètre[x[i][0]*valeur[i] for i in range(nb_objets)]<=xsum([x[i][1]*valeur[i] for i in range(nb_objets)]),name="c3")

        print("\n----------------------------------")
        if status == OptimizationStatus.OPTIMAL:
            print("Status de la résolution: OPTIMAL")
        elif status == OptimizationStatus.FEASIBLE:
            print("Status de la résolution: TEMPS LIMITE et UNE SOLUTION REALISABLE CALCULEE")
        elif status == OptimizationStatus.NO_SOLUTION_FOUND:
            print("Status de la résolution: TEMPS LIMITE et AUCUNE SOLUTION CALCULEE")
        elif (
            status == OptimizationStatus.INFEASIBLE
            or status == OptimizationStatus.INT_INFEASIBLE
        ):
            print("Status de la résolution: IRREALISABLE")
        elif status == OptimizationStatus.UNBOUNDED:
            print("Status de la résolution: NON BORNE")

        print("Temps de résolution (s) : ", runtime)
        print("----------------------------------")

        # Si le modèle a été résolu à l'optimalité ou si une solution a été trouvée dans le temps limite accordé
        if model.num_solutions > 0:
            # cost = (sum(
            #     instance.collection_cost
            #     * sum(
            #         sum(x[l][p][d].x for d in range(instance.nb_donors))
            #         for l in range(instance.nb_locations)
            #     )
            #     for p in range(instance.time_horizon)
            # )
            # + sum(
            #     sum(
            #         instance.cost_temp_facility * gam[m][l][0].x
            #         for m in range(instance.nb_locations)
            #     )
            #     for l in range(instance.nb_locations)
            # )
            # + xsum(
            #     xsum(
            #         instance.capacity_perm_facility * alpha[f][l].x
            #         for f in range(instance.nb_locations)
            #     )
            #     for l in range(instance.nb_locations)
            # )
            # + xsum(
            #     (
            #         xsum(
            #             s[h][p + 1].x * instance.storage_cost
            #             for p in range(instance.time_horizon)
            #         )
            #     )
            #     for h in range(instance.nb_hospitals)
            # )
            # + xsum(
            #     xsum(
            #         xsum(y[l][h][p].x for l in range(instance.nb_locations))
            #         * instance.transportation_cost
            #         * instance.dis_loc_hosp[h][l]
            #         for h in range(instance.nb_hospitals)
            #     )
            #     for p in range(instance.time_horizon)
            # )
            # + xsum(
            #     xsum(
            #         xsum(
            #             xsum(
            #                 instance.dist_locations[l][lbis]*(
            #                     gam[lbis][m][p + 1].x
            #                     - xsum(gam[k][m][p].x for k in range(instance.nb_locations))
            #                     + gam[l][m][p].x
            #                 )
            #                 for lbis in range(instance.nb_locations)
            #             )
            #             for l in range(instance.nb_locations)
            #         )
            #         for m in range(instance.nb_locations)
            #     )
            #     for p in range(instance.time_horizon-1)
            # )
            # * instance.cost_moving_facility)

            cost = (sum(instance.collection_cost* sum(sum(x[l][p][d].x for d in range(instance.nb_donors))for l in range(instance.nb_locations))for p in range(instance.time_horizon)) + sum(sum((instance.cost_temp_facility * gam[m][l][0].x) for m in range(instance.nb_locations))for l in range(instance.nb_locations))
            + sum(
                sum(
                    instance.cost_perm_facility * alpha[f][l].x
                    for f in range(instance.nb_locations)
                )
                for l in range(instance.nb_locations)
            )
            + sum(
                    sum(
                        s[h][p + 1].x * instance.storage_cost
                        for p in range(instance.time_horizon)
                    )
                for h in range(instance.nb_hospitals)
            )
            + sum(
                sum(
                    sum((y[l][h][p].x* instance.dis_loc_hosp[h][l]* instance.transportation_cost) for l in range(instance.nb_locations))
                    for h in range(instance.nb_hospitals)
                )
                for p in range(instance.time_horizon)
            )
            + sum(
                sum(
                    sum(
                        sum(
                            instance.dist_locations[l][lbis]*(
                                gam[m][lbis][p + 1].x
                                - sum(gam[m][k][p].x for k in range(instance.nb_locations))
                                + gam[m][l][p].x
                            )
                            for lbis in range(instance.nb_locations)
                        )
                        for l in range(instance.nb_locations)
                    )
                    for m in range(instance.nb_locations)
                )
                for p in range(instance.time_horizon-1)
            ) * instance.cost_moving_facility)

            print("Coût des décisions : ", cost)
            objective_value = xsum(xsum(I[h][p].x for h in range(instance.nb_hospitals))for p in range(instance.time_horizon))
            print("quantité de sang manquante : ", objective_value)
            
        print("----------------------------------\n")
        ### On sauvegarde les résultats : 
        centres_f = np.zeros((instance.nb_locations,instance.nb_locations))
        centres_m = np.zeros((instance.nb_locations,instance.nb_locations,instance.time_horizon))
        qtt_recue_hosp = np.zeros((instance.nb_locations,instance.nb_hospitals,instance.time_horizon))
        qtt_collect = np.zeros((instance.nb_locations,instance.time_horizon,instance.nb_donors))
        stock = np.zeros((instance.nb_hospitals,instance.time_horizon+1))
        qtt_manquante = np.zeros((instance.nb_hospitals,instance.time_horizon+1))
        # les centres utilisés, quand et où :
        for l in range(instance.nb_locations):
            for f in range(instance.nb_locations):
                centres_f[f][l] = alpha[f][l].x
            for p in range(instance.time_horizon):
                for m in range(instance.nb_locations):
                    centres_m[m][l][p] = gam[m][l][p].x
        # la quantité transférée vers les hôpitaux
        
        for p in range(instance.time_horizon):
            for l in range(instance.nb_locations):
                for h in range(instance.nb_hospitals):
                    qtt_recue_hosp[l][h][p] = y[l][h][p].x
                for d in range(instance.nb_donors):
                    qtt_collect[l][p][d] = x[l][p][d].x
        
        # le stock à la fin de chaque période : 
        for p in range(instance.time_horizon):
            for h in range(instance.nb_hospitals):
                stock[h][p] = s[h][p].x
            
        # la qtt manquante à la fin de chaque mois : 
        for p in range(instance.time_horizon):
            for h in range(instance.nb_hospitals):
                qtt_manquante[h][p] = I[h][p]
        sol = solution(objective_value,cost,centres_m,centres_f,qtt_recue_hosp,qtt_collect,stock,qtt_manquante)
        # for h in range(instance.nb_hospitals):
        #     for p in range(instance.time_horizon):
        #         # print("debugggg : ")
                # print("l'hôpital {} a besoin de {}, reçoit {}, stocke {} et manque {} de sang et il y avait avant {}".format(h,instance.Need_hospital[h][p],xsum(y[l][h][p].x for l in range(instance.nb_locations)),s[h][p+1].x,I[h][p].x,s[h][p].x))
                # print("qtt manquante :")
                # print(I[h][p].x + s[h][p+1].x -instance.Need_hospital[h][p] + xsum(y[l][h][p].x for l in range(instance.nb_locations)) + s[h][p].x)
        return sol,runtime
    
    else :
        print("Le modèle n'a pas tourné car l'instance n'est pas bonne")
        # sol = solution(0,0,np.zeros((instance.nb_locations,instance.nb_locations,instance.time_horizon)),np.zeros((instance.nb_locations,instance.nb_locations)))
        # runtime = -1
    
