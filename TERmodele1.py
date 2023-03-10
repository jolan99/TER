from read_instance import *

# from turtle import end_fill
from mip import *
import time

# Création du modèle vide
Budget = 20000000
model = Model(name="Blood_supply_chain", solver_name="CBC")


datafileName = "data_ter/1/1_22_22_2_18"
instance = read_data(datafileName)
# gamma = [
#     [
#         [
#             model.add_var(
#                 name="Gamma(" + str(m) + str(l) + str(p) + ")",
#                 lb=0,
#                 ub=1,
#                 var_type=BINARY,
#             )
#             for p in range(instance.time_horizon)
#         ]
#     ]
#     for l in range(instance.nb_locations)
#     for m in range(instance.nb_locations)
# ]
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
            lb=-max(instance.capacity_hospital),
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
    # + xsum(
    #     xsum(
    #         xsum(
    #             xsum(
    #                 instance.dist_locations[l][lbis]*(
    #                     gam[m][lbis][p + 1]
    #                     - xsum(gam[m][k][p] for k in range(instance.nb_locations))
    #                     + gam[m][l][p]
    #                 )
    #                 for lbis in range(instance.nb_locations)
    #             )
    #             for l in range(instance.nb_locations)
    #         )
    #         for m in range(instance.nb_locations)
    #     )
    #     for p in range(instance.time_horizon)
    # )
    # * instance.cost_moving_facility
    <= Budget
)


# Un seul centre par localisation à chaque période
for l in range(instance.nb_locations):
    for p in range(instance.time_horizon):
        model.add_constr(
            xsum(gam[m][l][p] for m in range(instance.nb_locations)) +
            xsum(alpha[f][l] for f in range(instance.nb_locations))
            <= 1
        )

# Un centre mobile ne peut être positionné qu'à une seule localisation
for m in range(instance.nb_locations):
    for p in range(instance.time_horizon):
        model.add_constr(
            xsum(gam[m][l][p] for l in range(instance.nb_locations)) <= 1
        )
# un centre fixe ne peut être positionné qu'à une seule localisation
for f in range(instance.nb_locations):
    model.add_constr(xsum(alpha[f][l] for l in range(instance.nb_locations)) <= 1)

# Si un centre mobile est utilisé, il l'est depuis la période 1 :
for m in range(instance.nb_locations):
    for p in range(instance.time_horizon - 1):
        model.add_constr(
            xsum(gam[m][l][p+1] for l in range(instance.nb_locations))
            == gam[m][l][p]
        )

# On ne peut pas collecter plus que ce que les donneurs peuvent donner
for d in range(instance.nb_donors):
    model.add_constr(
        xsum(
            xsum(x[l][p][d] for p in range(instance.time_horizon))
            for l in range(instance.nb_locations)
        )
        <= instance.supply_donor_group[d]
    )

# Un centre ne peut pas collecter plus que sa capacité max
for l in range(instance.nb_locations):
    for p in range(instance.time_horizon):
        model.add_constr(
            xsum(x[l][p][d] for d in range(instance.nb_donors))
            <= instance.capacity_temp_facility
            * xsum(gam[m][l][p] for m in range(instance.nb_locations))
            + instance.capacity_perm_facility
            * xsum(alpha[f][l] for f in range(instance.nb_locations))
        )

# On ne peut pas envoyer à un hôpital plus que ce qui a été collecté
for l in range(instance.nb_locations):
    for p in range(instance.time_horizon):
        model.add_constr(
            xsum(y[l][h][p] for h in range(instance.nb_hospitals))
            <= xsum(x[l][p][d] for d in range(instance.nb_donors))
        )

# on fixe le stock et la quantité de sang manquante : 
for h in range(instance.nb_hospitals):
    for p in range(instance.time_horizon):
        model.add_constr((I[h][p] + s[h][p]) == (instance.Need_hospital[h][p] - xsum(y[l][h][p] for l in range(instance.nb_locations)) - s[h][p-1]))

# le stock ne peut pas excéder le stock max des hôpitaux
for h in range(instance.nb_hospitals):
    for p in range(instance.time_horizon):
        model.add_constr(s[h][p] <= instance.capacity_hospital[h]) 

#on met à 0 le stock initial : 
for h in range(instance.nb_hospitals):
    model.add_constr(s[h][0] == 0)

status = model.optimize(max_seconds=120)
start = time.perf_counter()
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

    print("Solution calculée")
    for l in range(instance.nb_locations):
        for p in range(instance.time_horizon):
            for m in range(instance.nb_locations):
                if gam[m][l][p].x == 1 :
                  print("Un centre mobile est placé à la localisation {},{} à la période {}".format(instance.locations[l][0],instance.locations[l][0],p))
        for f in range(instance.nb_locations):
            if alpha[f][l].x == 1:
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
            instance.cost_temp_facility * gam[m][l][0].x
            for m in range(instance.nb_locations)
        )
        for l in range(instance.nb_locations)
    )
    + xsum(
        xsum(
            instance.capacity_perm_facility * alpha[f][l].x
            for f in range(instance.nb_locations)
        )
        for l in range(instance.nb_locations)
    )
    + xsum(
        (
            xsum(
                s[h][p + 1].x * instance.storage_cost
                for p in range(instance.time_horizon)
            )
        )
        for h in range(instance.nb_hospitals)
    )
    + xsum(
        xsum(
            xsum(y[l][h][p].x for l in range(instance.nb_locations))
            * instance.transportation_cost
            * instance.dis_loc_hosp[h][l]
            for h in range(instance.nb_hospitals)
        )
        for p in range(instance.time_horizon)
    )
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
    #     for p in range(instance.time_horizon)
    # )
    * instance.cost_moving_facility)

    print("Coût des décisions : ", valeur)
    print("quantité de sang manquante : ", xsum(xsum(I[h][p].x for h in range(instance.nb_hospitals))for p in range(instance.time_horizon)))
    
print("----------------------------------\n")
### à faire
