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
        self._carte = carte
        self._max = sante
        carte.ss_carte[abscisse][ordonnee] = self
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
    

    def combat(self,carte):
        """
        Méthode permettant à l'unité de combattre, si un objet ennemi se trouve 
        dans sa zone d'attaque.
        L'unité recherche les ennemis dans sa zone de combat et sélectionne 
        l'objet le plus proche grâce à la méthode chx_ennemi.
        Si il y a bien un objet, celui-ci perd de la vie.
        """

        Ennemi = self.chx_ennemi(carte)
        if Ennemi != None:
            Ennemi.sante = Ennemi.sante - self.capcbt
        print(Ennemi)
 
    
    def chx_ennemi(self,carte):
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
        x_inf = max(0,int(-self.zonecbt + x))
        x_sup = min(self._carte.dims[0], int(self.zonecbt + x))
        y_inf = max(0,int(-self.zonecbt + y))
        y_sup = min(self._carte.dims[1], int(self.zonecbt + y))
        
        print(x_inf, x_sup)
        print(y_inf,y_sup)
        
        Ennemi = None
        R_plus_petit_unit = self.zonecbt +1
        R_plus_petit_bat = self.zonecbt + 1
        
        
        for i in range(x_inf,x_sup+1):
            for j in range(y_inf,y_sup+1):
                Obj = carte.ss_carte[i][j]
                if Obj != ' ' and Obj.T_car()[0] == 'D':
                    R_Obj = math.sqrt((x-i)**2 + (y-j)**2)
                    
                    print(R_Obj,Obj)
                    
                    if Obj.T_car()[2] == 'U' and R_Obj < R_plus_petit_unit:
                        R_plus_petit_unit = R_Obj
                        Ennemi = Obj
                        
                    if Obj.T_car()[2] == 'B' and R_Obj < min(R_plus_petit_bat,R_plus_petit_unit):
                        R_plus_petit_bat = R_Obj
                        Ennemi = Obj
        
        return(Ennemi)
#                

class Scorpion(Unites_Humain_Attaquant):
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
        self.id = Scorpion.Id 
        Scorpion.Id += 1
        self.capmvt = 1
        self.capcbt = 2
        self.zonecbt = math.sqrt(2)
    
    def car(self):
        return 'S'
    
    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "%r_U_S%i"%(self._role, self.id )
    