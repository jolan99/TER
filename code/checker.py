from class_model import *
from mip import *

def checker(sol,instance):
    # un seul centre par localisation 
    # un centre utilisé qu'une seule fois par période
    # qtt reçues à l'hôpital pas plus grandes que ce qui peut être reçu 
    # qtt prélevées <= donneurs 
    # stocks pas trop élevés
    # I >= Nh 
    # 