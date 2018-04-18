# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 23:20:47 2018

@author: Erwann Landais
"""

import Map
import Partie
from Constantes import Constante
from Batiments import Foreuse,QG,Panneau_solaire
from numpy.random import randint
from numpy.random import choice
import time
from Un_Tour_Joueur import Un_Tour_Du_Joueur
from Ressource import metal

from Joueur import Joueur

from unites_IA_facile import Scorpion0
from unites_IA_Moyenne import Scorpion1
from Constantes import Constante

from Unites_Hn_Defenseur import Robot_combat
from Unites_Hn_Attaquant import Scorpion

class Save():
    def __init__(self,name,carte):
        
        Nme = self.Test_nom(name)
        Save = open(Nme,"w+")
        
                    
        Save.write("Carte \n")
        Save.write("Dimensions \n")
        Save.write(str(carte.dims))
        Save.write(" \n")
        Save.write("Tr actuel \n")
        Save.write(str(carte.tr_actuel))
        Save.write(" \n")
        Save.write("Nbe de tours totaux \n")
        Save.write(str(carte.nbtour))
        Save.write(" \n")
        
        
        for k in range(len(carte)):
            if carte[k].car() == 'M':
                R = carte[k]
                Save.write("Ressource \n")
                Save.write(str(R.valeur))
                Save.write(" \n")
                Save.write(str(R.coords))
                Save.write(" \n")
        Save.write("Fin ressources \n")
        
        
        L_joueur = carte.L_joueur

        for k in range(len(L_joueur)):
            Save.write("Joueur \n")
            Jr = L_joueur[k]
            Save.write(str(Jr._role))
            Save.write(" \n")
            Save.write(str(Jr.metal_tot))
            Save.write(" \n")
            Save.write(str(Jr.energie_tot))
            Save.write(" \n")
            Save.write(str(Jr.nbe_unite_restantes))
            Save.write(" \n")
            Save.write(str(Jr.IdU))
            Save.write(" \n")
            L_bat = Jr._liste_bat
            if len(L_bat[0]) != 0:
                Save.write("Batiments du joueur \n")
                for k in range(len(L_bat)):
                    L = L_bat[k]
                    for j in range(len(L)):
                        Save.write("Bat \n")
                        Save.write(str(L[j].T_car()))
                        Save.write(" \n")
                        Save.write(str(L[j].sante))
                        Save.write(" \n")
                        Save.write(str(L[j].coords))
                        Save.write(" \n")
                Save.write("Fin bat \n")
            L_unite = Jr._liste_unite
            if len(L_unite) !=0:
                Save.write("Unites du joueur \n")
                for j in range(len(L_unite)):
                    Save.write("Unite \n")
                    Save.write(str(L_unite[j].T_car()))
                    Save.write(" \n")
                    Save.write(str(L_unite[j].num_joueur))
                    Save.write(" \n")
                    Save.write(str(L_unite[j].sante))
                    Save.write(" \n")
                    Save.write(str(L_unite[j].coords))
                    Save.write(" \n")
                Save.write("Fin unite \n")
            Save.write("Fin joueur \n")

        Save.write("Fin sauvegarde")

        print("Sauvegarde effectuée!")

        
    
    def Test_nom(self,name):
        try:
            f = open(name,"r")
        except FileNotFoundError:
            return(name)

        L = input("Sauvegarde déjà existante. L'effacer? (Y/N)")
        if L == "Y":
            return(name)
        else:
            name = input("Entrez un nouveau nom de sauvegarde")
            name = name + ".txt"
            self.Test_nom(name)
            return(name)
    
class Load():
    def __init__(self,name):
        Nme = self.Test_save(name)
        if Nme != 'Q':
            with open(Nme, 'r') as f:
                Load = [line.strip() for line in f]
            self.process(Load)
            print("Chargement terminé! \n")
            self.Lcarte.simuler()

        
    def Test_save(self,name):
        try:
            f = open(name,"r")
        except FileNotFoundError:
            print("Sauvegarde introuvable \n")
            name = input("Entrez un autre nom de sauvegarde; ou quittez (Q) \n")
            if name != 'Q':
                name = name + '.txt'
                self.Test_save(name)
        return(name)
                
    def process(self,L):
        while len(L) !=0:

            if L[0] == 'Carte':

                Dims = L[2]
                Nbta = L[4]
                Nbt = L[6]
                L = L[7:]
                
                Dims = Dims[1:-1]
                k = Dims.find(',')
                X = int(Dims[0:k])
                Y = int(Dims[k+1:])
                Constante.xL = X
                Constante.yL = Y
                if int(X/2)%2 == 0:
                    LL = int(X/2)+1
                else : 
                    LL = int(X/2)
                if int(Y/2)%2 == 0:
                    LH = int(Y/2)+1
                else:
                    LH = int(Y/2)
                LEp = int(max(X,Y)/20)
                Constante.LL_Z_Constructible = LL
                Constante.LH_Z_Constructible = LH
                Constante.LEp_app = LEp
                    
                Constante.Lnbta = int(Nbta)
                
                Constante.Lnbt = int(Nbt)
                self.Lcarte = Map.Map([],1)
            
            while L[0] == 'Ressource':
                print("Ressource")
                Val = L[1]
                Pos = L[2]
                L = L[4:]
                
                Pos = Pos[1:-1]
                k = Pos.find(',')
                X = int(Pos[0:k])
                Y = int(Pos[k+1:])
                
                Val = int(Val)
                
                self.Lcarte.append(metal(X,Y,self.Lcarte,Val))
            print(L[0])
            while L[0] == 'Joueur':

                Role = L[1]
                Metal_tot = int(L[2])
                Energie_tot = int(L[3])
                Ur = int(L[4])
                Idu = int(L[5])
                self.Jr = Joueur(Role)
                self.Lcarte.L_joueur.append(self.Jr)
                self.Jr.metal_tot = Metal_tot
                self.Jr.energie_tot = Energie_tot
                self.Jr.IdU = Idu
                self.Jr.nbe_unite_restantes = Ur                
                L = L[7:]
                while L[0] == 'Bat':
                    Typ = L[1]
                    Sante = L[2]
                    Pos = L[3]
                    L = L[4:]
                    Sante = int(Sante)
                    Typ = Typ[-2:]
                    Pos = Pos[1:-1]
                    k = Pos.find(',')
                    X = int(Pos[0:k])
                    Y = int(Pos[k+1:])
                    if Typ == "QG":
                        B = QG(X,Y,self.Lcarte)
                        B.sante = Sante
                        self.Jr._liste_bat[0].append(B)
                    elif Typ[0] == "P":
                        Id = int(Typ[1])
                        B = Panneau_solaire(X,Y,self.Lcarte)
                        B.sante = Sante
                        B.id = Id
                        self.Jr._liste_bat[1].append(B)
                    elif Typ[0] == "F":
                        Id = int(Typ[1])
                        B = Foreuse(X,Y,self.Lcarte)
                        B.sante = Sante
                        B.id = Id
                        self.Jr._liste_bat[2].append(B)
                if L[0] == "Fin bat":
                    L = L[2:]
                
                while L[0] == "Unite":
                    
                    Typ = L[1]
                    Num_joueur = L[2]
                    Sante = L[3]
                    Pos = L[4]
                    L = L[5:]
                    Typ = Typ[-3:]
                    Num_joueur = int(Num_joueur)
                    Sante = int(Sante)
                    Pos = Pos[1:-1]
                    k = Pos.find(',')
                    X = int(Pos[0:k])
                    Y = int(Pos[k+1:])
                    if Typ[0:2] == "RC":
                        Id = int(Typ[2])
                        U = Robot_combat(Role,self.Lcarte,X,Y)
                        U.sante = Sante
                        self.Jr._liste_unite.append(U)
                    
                    elif Typ[1] == "S":
                        if len(Typ) >= 4:
                            if Typ[3] == "0":
                                Id = int(Typ[3:])
                                U = Scorpion0(Role,self.Lcarte,X,Y, Num_joueur)
                                U.sante = Sante
                                U.id = Id
                                self.Jr._liste_unite.append(U)
                            
                            elif Typ[3] == "1":
                                Id = int(Typ[3:])
                                U = Scorpion1(Role,self.Lcarte,X,Y, Num_joueur)
                                U.sante = Sante
                                U.id = Id
                                self.Jr._liste_unite.append(U)
                            
                        else:
                                Id = int(Typ[2:])
                                U = Scorpion(Role,self.Lcarte,X,Y, Num_joueur)
                                U.sante = Sante
                                U.id = Id
                                self.Jr._liste_unite.append(U)
                if L[0] == "Fin unite":
                    L = L[1:]
            if L[0] == "Fin sauvegarde":
                L = []
            else: 
                L = L[1:]    
                
            
    
                            
                    
                
                    
                    
                
                
        
            
                
    def process2(self,line,carac):
        line = line[:-2]
        
        if line == "Joueur":
            carac = "jr"
            self.Jr = Joueur.Joueur("Load")
            return(carac)
        if carac[0] == "j":
            if carac == "jr":
                self.Jr._role = line
                carac = "None"
            if carac[0:2] == "jb":
                if line == "Bat":
                    carac = "jbr"
                    return(carac)
                if carac == "jbr":
                    line = line[-2:]
                    if line == "QG":
                        B = Batiments.QG(0,0,carte)
                    elif line[0] == "P":
                        return(None)
                        
                
        
        if line == "Batiments du joueur":
            carac = "jb"
        
        
        
#VOIR QUI ON CREE EN PREMIER : MAP OU LISTE?

# A NOTER : TOUS LES BATIMENTS ET TOUS LES UNITES ONT BESOIN 
# D'UNE MAP EN PARAMETRES.
#SEMBLE MIEUX DE COMMENCER PAR MAP, PUIS D'AJOUTER A MAP LA LISTE DES JOUEURS.
        
        
        
        
        if line == "Carte":
            carac = "c"
        if carac[0] == "c":
            if line == "Dimensions":
                carac = "cd"
                return(carac)
            if carac == "cd":
                line = line[1:-1]
                k = line.find(',')
                X = int(line[0:k])
                Y = int(line[k+1:])
                Constante.xL = X
                Constante.yL = Y

            if line == "Tr actuel":
                carac = "cta"
                return(carac)
            if carac == "cta":
                Constante.Lnbta = int(line)
            
            if line == "Nbe de tours totaux":
                carac = "ct"
                return(carac)
            
            if carac == "ct":
                Constante.Lnbt = int(line)
                self.Lcarte = Map.Map([],1)
                return("None")
        
        if line == "Ressources":
            carac = "r"
            self.M = Ressources.metal(0,0,self.Lcarte,0)
        
        if carac[0] == "r":
            return(None)
            
                
                
        return(carac)
        
    

    
if __name__ == "__main__":
    f = open("Text1.txt","w+")

    L=  []
    V = []
    Load = open('Test1.txt')
    for line in Load:
        print(line)
        u = line
        L.append(u)
    with open('Test1.txt', 'r') as f:
        myNames = [line.strip() for line in f]
    V = Load.readlines()
