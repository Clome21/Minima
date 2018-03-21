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

from Unites_Hn_Attaquant import Fourmi
from Unites_Hn_Defenseur import Robot_combat

# from dprint import dprint

class Partie():
    """
    Classe mère, contenant l'ensemble des propriétés des objets intervenant dans
    le jeu.
    """

    def __init__(self, nb_ia , nb_hn = 1):
        """
        Permet de débuter la partie. La méthode fixe la position 
        des joueurs attaquants.
            
    Paramètres
    ----------
        nb_ia: int
            Le nombre de joueurs IA.
        
        nb_hn : int
            Le nombre de joueurs humains.
        """
        self.L_joueur = [Joueur('DH')]
        Posdisp = [ str(range(nb_ia))]
        nb_hn = nb_hn -1
        while nb_hn > 0:
            self.L_joueur.append(Joueur('AH'+Posdisp[0]))
            Posdisp = Posdisp[1:]
            nb_hn -= 1
        while nb_ia > 0:
            self.L_joueur.append(Joueur('AI'+Posdisp[0]))

            Posdisp = Posdisp[1:]
            nb_ia -= 1
        self.mise_en_place()
    
    def mise_en_place(self):
        """
        Fixe les listes des ennemis de chaque joueur.
        Fixe également quels sont les autres joueurs dans la partie pour
        chaque joueur.
        """
        n = len( self.L_joueur )
        for k in range(n):
            J_vu = self.L_joueur[k]
            role = J_vu._role
            if role[0:1] == 'A':
                J_vu.L_ennemi = [self.L_joueur[0] ]
            else : 
                J_vu.L_ennemi = self.L_joueur[1:n] 
            J_vu.L_autres_joueurs = self.L_joueur[0:k] + self.L_joueur[k+1:n]



if __name__ == "__main__":
    carte = Map.Map(40,30,6,4)
    Game = Partie(0,2)
    Game.L_joueur[1]._liste_unite.append( Fourmi('AHN',carte,0,1, Game.L_joueur[1].L_ennemi, Game.L_joueur[1].L_autres_joueurs ) )
    Game.L_joueur[0]._liste_unite.append( Robot_combat('DH',carte,1,1, Game.L_joueur[0].L_ennemi) )
    Game.L_joueur[0]._liste_unite.append( Robot_combat('DH',carte,1,0, Game.L_joueur[0].L_ennemi) )

    
    


# RAISONNER VIA UNE LISTE, ET NON UNE SOUS-MAP ! BEAUCOUP MOINS LOURD!