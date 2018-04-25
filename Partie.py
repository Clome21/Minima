# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
import Map

import numpy as np
from numpy.random import randint
import sys
import math
from Joueur import Joueur
from Constantes import Constante

from Unites_Hn_Attaquant import Scorpion
from Unites_Hn_Defenseur import Robot_combat

# from dprint import dprint

class Partie():
    """
    Classe mère, contenant l'ensemble des propriétés des objets intervenant dans
    le jeu.
    """

    def __init__(self, nb_ia , nb_hn = 1):
        
        """
        Permet de débuter la partie. 
            
    Paramètres
    ----------
        nb_ia: int
            Le nombre de joueurs IA.
        
        nb_hn : int
            Le nombre de joueurs humains.
        """
        
        self.L_joueur = [Joueur('DH')]
        self.nb_hn = nb_hn - 1
        Posdisp = [ str(k) for k in range(self.nb_hn+nb_ia)]
        while self.nb_hn > 0:
            self.L_joueur.append(Joueur('AH'+Posdisp[0]))
            Posdisp = Posdisp[1:]
            self.nb_hn -= 1
        
        nb_ia_0, nb_ia_1, nb_ia_2 = self.choix_niveau(nb_ia)
        
        while nb_ia_0 > 0:
            self.L_joueur.append(Joueur('AI_0_'+Posdisp[0]))
            Posdisp = Posdisp[1:]
            nb_ia_0 -= 1
            
        while nb_ia_1 > 0:
            self.L_joueur.append(Joueur('AI_1_'+Posdisp[0]))
            Posdisp = Posdisp[1:]
            nb_ia_1 -= 1
            
        while nb_ia_2 > 0:
            self.L_joueur.append(Joueur('AI_2_'+Posdisp[0]))
            Posdisp = Posdisp[1:]
            nb_ia_2 -= 1
            
        self.mise_en_place()
        self.carte = Map.Map(self.L_joueur)
    
    def mise_en_place(self):
        """
        Méthode exécutant les ajustements de base pour débuter la partie, sur chaque
        joueur.
#        """

#        n = len( self.L_joueur )
#        for k in range(n):
#            J_vu = self.L_joueur[k]
#            role = J_vu._role
#            if role[0:1] == 'A':
#                J_vu.L_ennemi = [self.L_joueur[0] ]
#            else : 
#                J_vu.L_ennemi = self.L_joueur[1:n] 
#            J_vu.L_autres_joueurs = self.L_joueur[0:k] + self.L_joueur[k+1:n]
        self.L_joueur[0].metal_tot, self.L_joueur[0].energie_tot = Constante.metal_tot, Constante.energie_tot
    
    def choix_niveau(self,nb_ia):
        """
        Permet au joueur humain de choisir le niveau de difficulté de l'IA.
        
        Paramètres
        ----------
        Entrée :
        
        nb_ia: int
            Le nombre de joueurs IA.
        
        Sortie : 
            
        nb_ia_i (i entre 0 et 2) : le nombre d'IA de niveau i, choisies par le 
        joueur humain.         
        
    
                """
        nb_ia_0 = 0
        nb_ia_1 = 0
        nb_ia_2 = 0
        for k in range(nb_ia):
            self.lvl = False
            print("Difficulté IA %i \n"%k )
            self.niveau=input("Quel niveau voulez-vous lui donner ? 0 / 1 / 2")
            if self.niveau=='0' or self.niveau=='1' or self.niveau=='2':
                self.lvl=True
            else:
                while self.lvl==False:
                    self.niveau=input("Erreur. Quel niveau voulez vous lui donner ? 0 / 1 / 2")                    
                    if self.niveau=='0' or self.niveau=='1' or self.niveau=='2':
                        self.lvl=True
            if self.niveau == '0':
                nb_ia_0 +=1
            elif self.niveau == '1':
                nb_ia_1 +=1
            else:
                nb_ia_2 +=1
                
        return(nb_ia_0, nb_ia_1, nb_ia_2)
            




if __name__ == "__main__":
    Game = Partie(0,2)
#    Game.L_joueur[1]._liste_unite.append( Scorpion('AH0',Game.carte,0,1, Game.L_joueur[1].L_ennemi, Game.L_joueur[1].L_autres_joueurs ) )
 #   Game.L_joueur[0]._liste_unite.append( Robot_combat('DH',Game.carte,1,1, Game.L_joueur[0].L_ennemi) )
  #  Game.L_joueur[0]._liste_unite.append( Robot_combat('DH', Game.carte,1,0, Game.L_joueur[0].L_ennemi) )
    Game.carte.simuler()

    
    


