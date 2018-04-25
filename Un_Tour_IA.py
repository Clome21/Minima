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

    
    def __init__(self,carte):
        self._carte = carte
        self.L_joueur = self._carte.L_joueur
        self.unite_disp_par_tour = 0
        
        self.__xmax = Constante.xmax
        self.__ymax = Constante.ymax  
        self.Epp = Constante.Ep_app

        self.H=Constante.H_Z_Constructible
        self.L=Constante.L_Z_Constructible


        
    def placement_pos(self,x_inf,x_sup,y_inf,y_sup,typ):
        A = self._carte.ss_carte[x_inf : x_sup , y_inf : y_sup]
        L_pos = []

        Coords = np.where( A == typ)
        for k in range(len(Coords[0])):
            i,j = Coords[0][k]+ x_inf , Coords[1][k] + y_inf
            L_pos.append((i,j))
        return(L_pos)
        
 
        
    def production_unite(self,role,k):
        if role[0] == 'D':
            self.production_unite_defense()
        elif role[0] == 'A':
            self.production_unite_attaque(role,k)


        
    def production_unite_attaque(self,role,k):
        if role[0:2] == 'AI':
            if role[3] == '0':
                self.production_unite_attaque_IA_0(k)
        elif role[0:2] == 'AH' :
            self.production_unite_attaque_Hn(k)
 

    def production_unite_attaque_IA_0(self,k):
        """ IA 0 : place toutes ses unités à chaque tour"""
        
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
        Effectue toutes les actions liées à un tour de jeu.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        Rien
        """
        # rnd.shuffle(self)    Utile si gestion des collisions

        n = len(self.L_joueur)
        for k in range(1,n):
            if self._carte.V_atta == 1:
                break
            role = self.L_joueur[k]._role
            if role[1] == 'I':
                print("\\\ Tour du joueur %r ///"%(role))
    
                self.production_unite_attaque_IA_0(k)
    
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

            
    