# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 21:17:38 2018

@author: Clément.SAWCZUK
"""

class Constante:
    
#----------------------------------------Constantes map    
    xmax = 26
    ymax = 18
    if xmax%2 == 0:
        L_Z_Constructible= int(xmax/2)+1
    else : 
        L_Z_Constructible= int(xmax/2)
    if ymax%2 == 0:
        H_Z_Constructible= int(ymax/2)+1
    else:
        H_Z_Constructible= int(ymax/2)+1
    
#    L_Z_Constructible = 9
#    H_Z_Constructible = 11
        
    L_app = L_Z_Constructible + 2
    H_app = H_Z_Constructible + 2
    Ep_app = int(max(xmax,ymax)/20)
    
#----------------------------------------Constantes ressources de départ    
    metal_tot=4
    energie_tot=4
    nbt= 2
    spawn_ress=2
#----------------------------------------Constantes Batiments
#----------------------------------Foreuse    
    cout_M_F=2
    cout_E_F=3    
    prod_M_F=3
#----------------------------------Panneau solaire
    cout_M_P=2  
    cout_E_P=2  
    prod_E_P=3

#----------------------------------QG
    
    prod_E_QG = 1
    prod_M_QG = 1
    
    nbe_unite_ajoute = 1 #0.5
    
#----------------------------------------Constantes Unites
#-------------------------------Robot combat
    
    capmvt_RC = 0
    cout_M_RC = 3
    cout_E_RC = 3
    capcbt_RC = 0

#------------------------------Scorpion0

    capmvt_S0 = 10
    capcbt_S0 = 10
    
#-----------------------------Scorpion

    capmvt_S = 10
    capcbt_S = 30
    
