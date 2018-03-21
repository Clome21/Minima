# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:34:28 2018

@author: landaier
"""


class Joueur(object):
    def __init__(self, role):
        """ 
        Crée la liste des bâtiments, des unités, ainsi que des joueurs ennemis 
        et des autres joueurs en jeu pour chaque joueur.
    
    Paramètres
    ----------
        role: str
            Le rôle du joueur dans la partie.
        """
        self.L_autres_joueurs = []
        self._role = role
        self._liste_unite = []
        self._liste_bat = []
        self.L_ennemi = []
      

