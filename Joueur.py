# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:34:28 2018

@author: landaier
"""

from Constantes import Constante

class Joueur(object):
    def __init__(self, role):
        """ 
        Crée la liste des bâtiments et des unités pour chaque joueur.
        Fixe également l'ensemble des variables qu'un joueur peut posséder.
        (sachant que selon le rôle du joueur, certaines ne seront jamais 
        modifiées).
    
    Paramètres
    ----------
        role: str
            Le rôle du joueur dans la partie.
        """
        self._role = role
        self._liste_unite = []
        self._liste_bat = [[],[],[]]
        self.metal_tot = 0
        self.energie_tot = 0
        self.nbe_unite_restantes = 0
        self.IdU = 0

    


      

