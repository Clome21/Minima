# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:56:00 2018

@author: landaier
"""
import math

class Unites_Humain_Attaquant():
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


    def bouger(self):
        """
        Mouvement de l'unité, choisie par l'utilisateur. Elle a lieu dans un rayon correspondant 
        à la capacité de mouvement autour de la position courante. Utilise l'accesseur coords.
        """
        X = int(input('Envoyez la nouvelle position en x. \n'))
        Y = int(input('Envoyez la nouvelle position en y. \n'))
        while self.capmvt < math.sqrt((X -self.x)**2 + (Y-self.y)**2) :
            print("Position hors du rayon d'action de l'unité. \n")
            X = int(input('Envoyez la nouvelle position en x. \n'))
            Y = int(input('Envoyez la nouvelle position en y. \n'))
        self.coords = (X, Y)
        return(self.coords)  

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

        Ennemi = self.chx_ennemi(self.L_ennemi)
        if Ennemi != None:
            Ennemi.sante = Ennemi.sante - self.capcbt
        print(Ennemi)
 
    
    def chx_ennemi(self, L_ennemis):
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
        R_plus_petit = self.zonecbt + 1
        print(L_ennemis)
        Ennemi = None
        for J in L_ennemis:
            L_unites = J._list_unit

            for j in range( len(L_unites)):
                x,y = L_unites[j].coords
                R_unite = math.sqrt((x-self.x)**2 + (y-self.y)**2)
                if R_unite < min(R_plus_petit,self.zonecbt):
                    Ennemi = L_unites[j]
                    R_plus_petit = R_unite
        if R_plus_petit > self.zonecbt:
            for i in range(len(L_ennemis)):
                L_bat = L_ennemis[i]._list_bat
                for l in range( len(L_bat)):
                    x,y = L_bat[l].coords
                    R_bat = math.sqrt((x-self.x)**2 + (y-self.y)**2)
                    if R_bat < min(R_plus_petit,self.zonecbt):
                        Ennemi = L_bat[l]
                        R_plus_petit = R_bat
        if R_plus_petit > self.zonecbt:
            return (None)
        return(Ennemi)
                

class Fourmi(Unites_Humain_Attaquant):
    """
    Classe spécialisant Unites_Humain_Attaquant pour représenter une Fourmi.
    """
    Id = 0
    def __init__(self,role,carte,x,y, L_ennemi, L_autres_joueurs):
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
        self.__sante = 10
        super().__init__(x, y, carte, role, self.__sante)
        self.L_ennemi = L_ennemi
        self.L_autres_joueurs = L_autres_joueurs
        self.id = Fourmi.Id 
        Fourmi.Id += 1
        self.capmvt = 1
        self.capcbt = 2
        self.zonecbt = math.sqrt(2)
    
    def car(self):
        return 'F'
    
    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "%r_U_F%i"%(self._role, self.id )
    
