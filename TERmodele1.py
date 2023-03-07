
#chemin relatif vers le fichier (l'utilisation .. permet de revenir au dossier parent)
datafileName = 'data_tresor/tresor_150.dat'

#ouverture du fichier, le ferme automatiquement à la fin et gère les exceptions
with open(datafileName, "r") as file:
    # lecture de la 1ère ligne et séparation des éléments de la ligne
    # dans un tableau en utilisant l'espace comme séparateur
    line = file.readline()  
    lineTab = line.split()
    
    # la valeur de la 1ère case correspond au nombre d'objets
    # (attention de penser à convertir la chaîne de caractère en un entier)
    nb_objets = int(lineTab[0])

    # la valeur de la 2ème case correspond à la taille des sac-à-dos
    taille = int(lineTab[1])

    # création d'un tableau qui stockera les volumes des objets
    volume = []
    # création d'un tableau qui stockera les valeurs des objets
    valeur = []
    
    # pour chaque ligne contenant les informations sur les objets
    for i in range(nb_objets):
        # lecture de la ligne suivante et séparation des éléments de la ligne
        # dans un tableau en utilisant l'espace comme séparateur
        line = file.readline()
        lineTab = line.split()
        
        # ajout de l'élément de la 1ère case au tableau qui contient les volumes
        volume.append(int(lineTab[0])) 
        # ajout de l'élément de la 2ème case au tableau qui contient les valeurs
        valeur.append(float(lineTab[1]))
    
        
# Affichage des informations lues
print("Nombre d'objets = ", nb_objets)
print("Capacité des sac-à-dos = ", taille)
print("Volume des objets = ", volume)
print("Valeur des objets = ", valeur)

# Import du paquet PythonMIP et de toutes ses fonctionnalités
from turtle import end_fill
from mip import *
# Import du paquet time pour calculer le temps de résolution
import time 

# Création du modèle vide 
model = Model(name = "Tresor", solver_name="CBC")


x1=[model.add_var(name="X("+str(i)+")",lb=0,ub=1,var_type=BINARY)for i in range(nb_objets)]
x2=[model.add_var(name="X("+str(i)+")",lb=0,ub=1,var_type=BINARY)for i in range(nb_objets)]

model.objective=maximize(xsum(valeur[i]*x1[i] for i in range(nb_objets)))


model.add_constr(xsum([x1[i]*volume[i]for i in range(nb_objets)])<=taille,name="c1")
model.add_constr(xsum([x2[i]*volume[i]for i in range(nb_objets)])<=taille,name="c2")

model.add_constr(xsum([x1[i]*valeur[i] for i in range(nb_objets)])<=xsum([x2[i]*valeur[i] for i in range(nb_objets)]),name="c3")

for i in range(nb_objets):
    model.add_constr(x1[i]+x2[i]<=1)





status = model.optimize(max_seconds=120)
start = time.perf_counter()
runtime = time.perf_counter() - start








# Ecrire le modèle
model.write("tresor.lp") #à décommenter si vous le souhaitez

# Lancement du chronomètre[x[i][0]*valeur[i] for i in range(nb_objets)]<=xsum([x[i][1]*valeur[i] for i in range(nb_objets)]),name="c3")

print("\n----------------------------------")
if status == OptimizationStatus.OPTIMAL:
    print("Status de la résolution: OPTIMAL")
elif status == OptimizationStatus.FEASIBLE:
    print("Status de la résolution: TEMPS LIMITE et UNE SOLUTION REALISABLE CALCULEE")
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print("Status de la résolution: TEMPS LIMITE et AUCUNE SOLUTION CALCULEE")
elif status == OptimizationStatus.INFEASIBLE or status == OptimizationStatus.INT_INFEASIBLE:
    print("Status de la résolution: IRREALISABLE")
elif status == OptimizationStatus.UNBOUNDED:
    print("Status de la résolution: NON BORNE")
    
print("Temps de résolution (s) : ", runtime)
print("----------------------------------")

# Si le modèle a été résolu à l'optimalité ou si une solution a été trouvée dans le temps limite accordé
if model.num_solutions>0:
    print("Solution calculée")
    value = 0
    print("Objets du premier sac-dos")
    for i in range(nb_objets):
        if (x1[i].x >= 0.01):
            print("\t",i, " à ",x1[i].x*100, " %")
            value += x1[i].x * valeur[i]
    print("Valeur du sac-à-dos : ", value)
    value = 0
    print("\n Objets du second sac-dos")
    for i in range(nb_objets):
        if (x2[i].x >= 0.01):
            print("\t",i, " à ",x2[i].x*100, " %")
            value += x2[i].x * valeur[i]
    print("Valeur du sac-à-dos : ", value)
else:
    print("Pas de solution calculée")
print("----------------------------------\n")
