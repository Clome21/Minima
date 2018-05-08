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
from Un_Tour_Hn import Un_Tour_Joueur_Hn
from Un_Tour_IA import Un_Tour_Joueur_IA
from Ressource import metal
from Joueur import Joueur
from unites_IA_facile import Scorpion0
from unites_IA_Moyenne import Scorpion1
from Constantes import Constante
from Unites_Hn_Defenseur import Robot_combat, Robot_Ouvrier
from Unites_Hn_Attaquant import Scorpion

class Save():
    """
    Classe gérant le processus de sauvegarde d'une partie.
    """
    def __init__(self,name,carte):
        """
        Initialise la création de la sauvegarde. Les informations nécessaires pour recréer la partie 
        sauvegardée sont stockées dans un fichier .txt, dont le nom est choisi par l'utilisateur. Le
        programme vérifie avant si le nom est déjà employé par une autre sauvegarde, puis écrit/modifie
        le fichier .txt avec les informations.
        
        Paramètres : 
        ------------
        
        name : str
            Le nom de la sauvegarde choisi par l'utilisateur.
            
        carte : objet Carte.
            L'objet Carte de la partie devant être sauvegardée.
            
        Renvoie :
        -----------
        Rien.
        
        """
        
        
        # Sauvegarder également le joueur en cours, la variable tour_en_crs, et la variable tour_jr_en_cours.
        # (pas forcément les deux dernières : si la sauvegarde a pu avoir lieu, ça devait forcément être pendant un tour
        # de jeu d'un joueur humain; donc les deux seraient égales à 1.
        # Sauvegarder aussi les capacités de mouvement des unités pour le joueur humain en cours (uniquement).
        # Voir si une option est nécessaire pour quitter (si un objet partie va forcément rester en arrière plan ou non).
        
        self.Nme = self.Test_nom(name)
        Save = open(self.Nme,"w+")
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
        Save.write(str(carte.TrIA.unite_disp_par_tour))
        Save.write(" \n")
        for k in range(len(carte)):
            if carte[k].car() == 'M ':
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
        """
        Contrôle le nom de la sauvegarde choisie par l'utilisateur. Si le nom correspond à une 
        sauvegarde déjà existante, la méthode demande une confirmation auprès de l'utilisateur 
        pour l'écraser. Si l'utilisateur refuse, elle invite alors celui-ci à entrer un autre nom.
        Sinon, la sauvegarde est directement écrite avec le nom choisi.
        
        Paramètres : 
        -------------
        name : str
            Le nom de la sauvegarde choisi par l'utilisateur.
            
        Renvoie : 
        ------------
        name : str
            Le nom de la sauvegarde, choisi par l'utilisateur et confirmé par la méthode.
        """
        try:
            f = open(name,"r")
        except FileNotFoundError:
            return(name)

        L = input("Sauvegarde déjà existante. L'effacer? (Y/N)")
        if L == "Y":
            name = name+ ".txt"
            return(name)
        else:
            name = input("Entrez un nouveau nom de sauvegarde")
            name = name + ".txt"
            self.Test_nom(name)
            return(name)
    
class Load():
    """
    Classe gérant le processus de chargement d'une partie.
    """
    def __init__(self,name):
        """
        Permet d'initialiser le chargement de la partie. La méthode vérifie d'abord que le nom entré
        est correct; ensuite, il rassemble toutes les lignes de caractères de la sauvegarde dans une
        liste L. Il recrée ensuite la partie grâce à la méthode process(L).
        
        Paramètres : 
        ------------
        name : str
            Le nom de la sauvegarde devant être chargée
        
        Renvoie :
        ----------
        Rien.
        
        """
        self.Nme = self.Test_save(name)
        if self.Nme != 'Q':
            with open(self.Nme, 'r') as f:
                self.Load = [line.strip() for line in f]
            self.process(self.Load)
            print("Chargement terminé! \n")

        
    def Test_save(self,name):
        """
        Teste le nom de la sauvegarde entré par l'utilisateur. Si ce nom est faux, la méthode le
        signale à l'utilisateur, et l'invite à entrer un nouveau nom ou à quitter le processus de
        sauvegarde. Sinon, il confirme le nom entré par l'utilisateur.
        
        Paramètres :
        -------------
        name : str
            Le nom de la sauvegarde devant être chargée, entré par l'utilisateur.
        
        Renvoie : 
        ------------
        name : str
            Le nom de la sauvegarde devant être chargée, choisi par l'utilisateur et confirmé par la méthode.
        """
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
        """
        Effectue le processus de chargement de la partie, en testant les différentes chaînes de caractères de
        la liste L.
        
        Paramètres:
        ------------
        L : list
            Liste contenant toutes les chaînes de caractères de la sauvegarde; chaque élément de
            la liste correspond à une ligne de la sauvegarde.
            
        Renvoie : 
        ----------
        Rien.
        
        """
        Tst = ['S','R']
        while len(L) !=0:
            if L[0] == 'Carte':
                # Processus de recréation de la carte sauvegardée.
                Dims = L[2]
                Nbta = L[4]
                Nbt = L[6]
                U_disp = L[7]
                L = L[8:]
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
                U_disp = int(U_disp)
                self.Lcarte = Map.Map([],1)
                self.Lcarte.TrIA.unite_disp_par_tour = U_disp
                
            while L[0] == 'Ressource':
                #Processus de chargement des ressources sauvegardées sur la carte.
                Val = L[1]
                Pos = L[2]
                L = L[4:]
                
                Pos = Pos[1:-1]
                k = Pos.find(',')
                X = int(Pos[0:k])
                Y = int(Pos[k+1:])
                
                Val = int(Val)
                
                metal(X,Y,self.Lcarte,Val)

            while L[0] == 'Joueur':
                # Processus de chargement des joueurs de la partie, et de leurs caractéristiques principales.
                Role = L[1]
                Metal_tot = int(L[2])
                Energie_tot = int(L[3])
                Ur = int(L[4])
                self.Jr = Joueur(Role)
                self.Lcarte.L_joueur.append(self.Jr)
                self.Jr.metal_tot = Metal_tot
                self.Jr.energie_tot = Energie_tot
                self.Jr.nbe_unite_restantes = Ur                
                L = L[6:]
                while L[0] == 'Bat':
                # Processus de chargement des batiments du joueur actuel.
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
                    # Processus de chargement des unités du joueur actuel.
                    k = -2
                    Typ = L[1]
                    Num_joueur = L[2]
                    Sante = L[3]
                    Pos = L[4]
                    L = L[5:]
                    tTyp = Typ[k:]
                    while tTyp[0] not in Tst:
                         k = k- 1
                         tTyp = Typ[k:]
                    Typ = tTyp
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
                        
                    elif Typ[0:2] == "RO":
                        Id = int(Typ[2])
                        U = Robot_Ouvrier(Role,self.Lcarte,X,Y)
                        U.sante = Sante
                        self.Jr._liste_unite.append(U)

                    elif Typ[0] == "S":
                            if Typ[1] == "0":
                                Id = int(Typ[2:])
                                U = Scorpion0(Role,self.Lcarte,X,Y, Num_joueur)
                                U.sante = Sante
                                U.id = Id
                                self.Jr._liste_unite.append(U)
                            
                            elif Typ[1] == "1":
                                Id = int(Typ[2:])
                                U = Scorpion1(Role,self.Lcarte,X,Y, Num_joueur)
                                U.sante = Sante
                                U.id = Id
                                self.Jr._liste_unite.append(U)
                            
                    elif Typ[1] == "S":
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
