# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:38:35 2018

@author: landaier
"""

import math 
import numpy as np
from Constantes import Constante

class Unites_Humain_Defenseur():
    """
    Classe décrivant les comportements des unités humaines, lorsque celui-ci est
    un attaquant.
    """
    def __init__(self, abscisse, ordonnee, carte, role, sante):
        """
        Crée une unité aux coordonnées désirées.
        
        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles l'unité sera créé.
            
        carte : classe Map
            La carte sur laquelle évolue l'unité.
        
        role : str
            Le rôle du joueur possédant l'unité : attaquant ou défenseur.
        
        sante : int
            La santé de l'unité sélectionnée.
        """

        self._role = role
        self.__sante = sante

        self._max = sante
        self._carte = carte
        self._carte.ss_carte[abscisse][ordonnee] = self
        self._carte.append(self)
        self.coords = abscisse, ordonnee


    def __str__(self):
        """
        Affiche l'état courant de l'unité.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        s: str
            La chaîne de caractères qui sera affichée via ''print''; elle comprend 
            les caractéristiques les plus importantes de l'unité sélectionnée.
        """
        return "%r : position (%i, %i) etat %i/%i"%(
            self.T_car(), self.x, self.y,
            self.sante, self._max
            )
    
    
    def car(self):
        """
        Renvoie l'identifiant de l'unité en question
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        'U' : str
            Le caractère représentant l'unité.
        """
        return 'U'    
    
    def affichage(self):
        print(str(self))


    def bouger(self):
        """
        Mouvement de l'unité, choisie par l'utilisateur. Elle a lieu dans un rayon correspondant 
        à la capacité de mouvement autour de la position courante. Utilise l'accesseur coords.
        """

        L_vide = self.mvt_poss()
        xi, yi = self.coords
        if len(L_vide) == 0:
            print("Aucun mouvement possible pour l'unité, étape suivante")
            return(None)
        print("Mouvements possibles :", L_vide)
        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
        k = L.find(',')
        X = int(L[0:k])
        Y = int(L[k+1:])
        while (X,Y) not in L_vide:
            print("Position hors du rayon d'action de l'unité. \n")
            L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
            k = L.find(',')
            X,Y = int(L[0:k]) , int(L[k+1:])
        self.coords = (X, Y)
        self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]
        return(self.coords)  
    
    def mvt_poss(self):
        x,y = self.coords
        
        self.L_vide = []
        x_inf = max(0,int(-self.capmvt) + x)
        x_sup = min(self._carte.dims[0]-1, int(self.capmvt + x))
        y_inf = max(0,int(-self.capmvt) + y)
        y_sup = min(self._carte.dims[1]-1, int(self.capmvt + y))
        
        print(x_inf, x_sup)
        print(y_inf,y_sup)
        
        
        Altrs = self._carte.ss_carte[x_inf:x_sup+1,y_inf:y_sup+1]

        
        Coords = np.where(Altrs == ' ')

        
        for k in range(len(Coords[0])):
            i,j = Coords[0][k]+ x_inf,Coords[1][k] + y_inf
            self.L_vide.append((i,j))

        return(self.L_vide)
        

    @property
    def coords(self):
        """
       coords: tuple
           Les coordonnées de l'unité sur le plateau de jeu
           """

        return self.__coords


    @property
    def x(self):
        """
        x: nombre entier
            Abscisse de l'unité
        """
        return self.coords[0]

    @property
    def y(self):
        """
        y: nombre entier
            Ordonnée de l'unité
        """
        return self.coords[1]   

    @coords.setter
    def coords(self, nouv_coords):
        """
        Met à jour les coordonnées de l'unité.
        Garantit qu'elles arrivent dans la zone définie par
        la carte.
    
        Paramètres
        ----------
        nouv_coords : tuple représentant les coordonnées auquelles 
                      l'unité essaie de se rendre.
        """
        x, y = nouv_coords
        XM,YM = self._carte.dims
        x = min(x, XM-1)
        x = max(x,0)
        y = min(y, YM-1)
        y = max(y,0)

        self.__coords = (x, y)

    @property
    def sante(self):
        """
        sante: float
            Le niveau de santé de l'unité. Si ce niveau arrive à 0 l'unité
            est marqué comme mort et sera retiré du plateau de jeu
        """
        return self.__sante
    
    @sante.setter
    def sante(self, value):
        """
        Met à jour le niveau de santé de l'Unité. Garantit que la valeur arrive 
        dans l'intervalle [0, self._max]. Met à 0 les valeurs négatives, ne
        fait rien pour les valeurs trop grandes.
        """
        if value <= self._max:
            self.__sante = value
        if value <= 0:  
            value = 0
    

    def combat(self):
        """
        Méthode permettant à l'unité de combattre, si un objet ennemi se trouve 
        dans sa zone d'attaque.
        L'unité recherche les ennemis dans sa zone de combat et sélectionne 
        l'objet le plus proche grâce à la méthode chx_ennemi.
        Si il y a bien un objet, celui-ci perd de la vie.
        """

        Ennemi = self.chx_ennemi()
        if Ennemi != None:
            print( "%s a blessé %s"%(self.T_car(), Ennemi.T_car() ) )
            Ennemi.sante = Ennemi.sante - self.capcbt
            if Ennemi.sante <= 0:
                Ennemi.disparition()
        else :
            print("%s n'a blessé personne"%(self.T_car()) )
 
    
    def chx_ennemi(self):
        """
        Méthode sélectionnant l'objet le plus proche de l'unité.
        Elle parcourt pour chaque joueur ennemi l'ensemble des unités qu'elle
        possède, et sélectionne le plus proche.
        Elle vérifie ensuite si il n'y a pas un bâtiment plus proche.
        
        Paramètres
        ----------
        L_ennemis : liste
        Contient l'ensemble des joueurs ennemis de l'unité.

        """
        
        
        x,y = self.coords
        x_inf = max(0, int(-self.zonecbt) + x)
        x_sup = min(self._carte.dims[0]-1, int(self.zonecbt + x))
        y_inf = max(0,int(-self.zonecbt) + y)
        y_sup = min(self._carte.dims[1]-1, int(self.zonecbt + y))
        

        Ennemi = None
        R_plus_petit_unit = self.zonecbt +1
       
        
        for i in range(x_inf,x_sup+1):
            for j in range(y_inf,y_sup+1):
                Obj = self._carte.ss_carte[i][j]
                if Obj != ' ' and Obj !='/' and Obj.T_car()[0] == 'A':
                    R_Obj = math.sqrt((x-i)**2 + (y-j)**2)
                    print(R_Obj,Obj)

                    if  R_Obj < R_plus_petit_unit:
                        R_plus_petit_unit = R_Obj
                        Ennemi = Obj

        return(Ennemi)

    def disparition(self):
        print("%s est mort! \n"%(self.T_car()))
        x,y = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        self._carte.L_joueur[0]._liste_unite.remove(self)
    
    
class Robot_combat(Unites_Humain_Defenseur):
    """
    Classe spécialisant Unites_Humain_Defenseur pour représenter un Robot
    de combat.
    """
    Id = 0
    def __init__(self, role, carte,x,y, L_ennemi = []):
        """Permet d'initialiser l'unité.
            
    Paramètres
    ----------
    
    role : str
    Le rôle du joueur possèdant l'unité
            
    carte : classe Map
    La carte sur laquelle évolue l'unité.

    x, y : int
    Les coordonnées de l'unité en abscisse et en ordonnée

    L_ennemis : liste
    Contient l'ensemble des joueurs ennemis de l'unité.
    
        """
        self.__sante = 20
        super().__init__(x,y,carte,role,self.__sante)
        self.id = Robot_combat.Id
        Robot_combat.Id += 1
        self.L_ennemi = L_ennemi

        self.capmvt = Constante.capmvt_RC
        self.capcbt = Constante.capcbt_RC
        self.zonecbt = math.sqrt(2)
    
    
    def car(self):
        return "RC"

    
    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "D_U_RC%i"%( self.id )