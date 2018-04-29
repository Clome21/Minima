# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 18:28:55 2018

@author: Erwann Landais
"""


from Constantes import Constante

from numpy.random import randint
from unites_IA_facile import Scorpion0

import numpy as np


class Un_Tour_Joueur_IA():
"""
Classe gérant l'ensemble des méthodes et des variables consacrées à l'exécution d'un tour de jeu, pour
un joueur IA.
"""
    
    def __init__(self,carte):
                """
        Initialise les variables utilisées pour le déroulement des tours de jeu, pour un joueur
        IA.
        
        Paramètres :
        ------------
        carte : Objet Map
            L'objet Map utilisé pour la partie.
        
        """
        self._carte = carte
        self.L_joueur = self._carte.L_joueur
        self.unite_disp_par_tour = 0
        
        self.__xmax = Constante.xmax
        self.__ymax = Constante.ymax  
        self.Epp = Constante.Ep_app

        self.H=Constante.H_Z_Constructible
        self.L=Constante.L_Z_Constructible


        
    def placement_pos(self,x_inf,x_sup,y_inf,y_sup,typ):
         """
        Indique quelles sont les cases de la carte sur lesquelles l'objet typ est présent.
        Attention : x_sup et y_sup doivent valoir la dernière ligne/ colonne que l'on souhaite contrôler + 1.
        Ici, elle est régulièrement utilisée pour déterminer les positions où un placement d'unité est possible.
        
        Paramètres : 
        ------------
        x_inf : int
            La 1e ligne de la partie de la carte dont on veut contrôler la présence de l'objet typ.
        
        x_sup : int
            La ligne juste après la fin de la partie de la carte dont on veut contrôler la présence de l'objet typ.
        
        y_inf : int
            La 1e colonne de la partie de la carte dont on veut contrôler la présence de l'objet typ.
        
        y_sup : int
            La colonne juste après la fin de la partie de la carte dont on veut contrôler la présence de l'objet typ.
        
        typ : objet (souvent string ici)
            L'objet dont on veut contrôler la présence sur une portion de la carte.
        
        Renvoie :
        ----------
        L_pos : list
            L'ensemble des coordonnées sur lesquelles se trouve l'objet typ, dans la portion de carte étudiée.
        """
        A = self._carte.ss_carte[x_inf : x_sup , y_inf : y_sup]
        L_pos = []

        Coords = np.where( A == typ)
        for k in range(len(Coords[0])):
            i,j = Coords[0][k]+ x_inf , Coords[1][k] + y_inf
            L_pos.append((i,j))
        return(L_pos)
        
 
        
    def production_unite_attaque_IA(self,role,k):
        """
        Choisit la méthode de production d'unités d'attaque à sélectionner, selon le niveau
        de l'IA exécutant cette méthode.
        
        Paramètres :
        ------------
        role : str
            Le rôle du joueur exécutant la méthode.
        
        k : int
            La position du joueur dans la liste L_joueur.
        
        Renvoie :
        ---------
        Rien.
        """
        if role[3] == '0':
            self.production_unite_attaque_0(k)
        elif role[3] == '1':
            self.production_unite_attaque_1(k)
        else:
            self.production_unite_attaque_2(k)
 

    def production_unite_attaque_IA_0(self,k):
        """ 
        Produit des unités de combat pour l'attaquant IA de niveau 0.
        Celui-ci placera toutes ses unités au hasard parmi les positions possibles.
        
        Paramètres :
        ------------
        k : int
            La position du joueur exécutant la méthode dans la liste L_joueur.
        
        Renvoie :
        ----------
        Rien.
        
        """
        
        Jr = self.L_joueur[k]
        unite_disp = self.unite_disp_par_tour + Jr.nbe_unite_restantes
        
        if unite_disp < 1:
            print("Aucune unité à placer pour ce tour. \n")
        
        else:
        
            L_Ht = self.placement_pos(0,self.Epp + 1,(self.__ymax -self.H)//2,(self.__ymax + self.H )//2,' ')
            
            L_Bas = self.placement_pos(self.__xmax-1-self.Epp,self.__xmax,(self.__ymax -self.H)//2,(self.__ymax + self.H )//2,' ')
        
            L_Gche = self.placement_pos((self.__xmax - self.L )//2 , (self.__xmax + self.L )//2,0,self.Epp+1,' ')
        
            L_Dte = self.placement_pos((self.__xmax - self.L )//2, (self.__xmax + self.L )//2,self.__ymax -1-self.Epp,self.__ymax,' ')
        
            #Sélectionne les 4 zones d'apparitions
        
            L_pos = L_Ht + L_Bas + L_Gche + L_Dte 
        
        #Sélectionne les emplacements disponibles
            if len(L_pos) == 0:
                print("Aucune zone d'apparition d'unité disponible, étape suivante. \n")
        
            else : 

                while len(L_pos) != 0 and unite_disp >= 1 :
                
                    c = randint(len(L_pos))
                    X,Y = L_pos[c]
                    L_pos.remove((X,Y))
                    U = Scorpion0(Jr._role,self._carte,X,Y,k)
                    Jr._liste_unite.append(U)
                    unite_disp-=1
                
                    if unite_disp <1:
                        print("Plus d'unité disponible, étape suivante \n")
                        break
                
                    if len(L_pos) == 0:
                        print("Aucune zone d'apparition d'unité disponible, étape suivante. \n")
                        break

        
    def unTourIA(self):

        """
        Effectue toutes les actions liées à un tour de jeu, pour les joueurs IA.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        Rien
        """

        n = len(self.L_joueur)
        for k in range(1,n):
            if self._carte.V_atta == 1:
                break
            role = self.L_joueur[k]._role
            if role[1] == 'I':
                print("\\\ Tour du joueur %r ///"%(role))
    
                self.production_unite_attaque_IA(role,k)
    
                L_unite = self.L_joueur[k]._liste_unite
                for c in L_unite:
                    if self._carte.V_atta == 1:
                        break
    
                    print("Tour de %r \n"%(c.T_car()))
                    c.bouger()
                    c.action()

        self.unite_disp_par_tour += Constante.nbe_unite_ajoute
        if self.unite_disp_par_tour > min(self.L,self.H):
            self.unite_disp_par_tour = min(self.L,self.H)

            
    
