# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 10:56:00 2018

@author: landaier
"""
import math
import numpy as np
from Constantes import Constante


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
        print("Mouvements possibles :", L_vide)
        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
        k = L.find(',')
        while k == -1:
            print("Erreur de synthaxe. Recommencez svp")
            L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
            k = L.find(',')
        X = int(L[0:k])
        Y = int(L[k+1:])
        while (X,Y) not in L_vide:
            print("Position hors du rayon d'action de l'unité. \n")
            L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
            k = L.find(',')
            while k == -1:
                print("Erreur de synthaxe. Recommencez svp")
                L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                k = L.find(',')
            X,Y = int(L[0:k]) , int(L[k+1:])
        self.coords = (X, Y)
        self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]
        return(self.coords)  
    
    def mvt_poss2(self):
        x,y = self.coords
        
        self.L_vide = []
        x_inf = max(0,int(-self.capmvt) + x)
        x_sup = min(self._carte.dims[0]-1, int(self.capmvt + x))
        y_inf = max(0,int(-self.capmvt) + y)
        y_sup = min(self._carte.dims[1]-1, int(self.capmvt + y))

        
        Altrs = self._carte.ss_carte[x_inf:x_sup+1,y_inf:y_sup+1]
        

        
        Coords = np.where(Altrs == ' ')

        

        
        for k in range(len(Coords[0])):
            i,j = Coords[0][k] + x_inf , Coords[1][k] + y_inf
            self.L_vide.append((i,j))
            

        return(self.L_vide)
    
    def mvt_poss(self):
        x,y = self.coords
        
        self.L_vide = []

        L_obj = []
        x_inf = max(0,int(-self.capmvt) + x)
        x_sup = min(self._carte.dims[0]-1, int(self.capmvt + x))
        y_inf = max(0,int(-self.capmvt) + y)
        y_sup = min(self._carte.dims[1]-1, int(self.capmvt + y))
        
        i = x_inf
        j = y_inf
        
        for i in range(x_inf,x_sup+1):
            for j in range(y_inf,y_sup +1):
                if self._carte.ss_carte[i,j] == ' ':
                    
# SINON : FAIRE IF MUR SUR LIGNE OU COL.
                    self.L_vide.append((i,j))
                else:
                    L_obj.append((i,j))
                    
        for k in range(len(L_obj)):
            ox,oy = L_obj[k]
            L = []
            
            if ox - x <0 and oy - y <0:
                #Diag H/G
                
                L = [(ox-1,oy-1),(ox-1,oy),(ox,oy-1)]
                
            elif ox - x <0 and oy - y >0:
                
                #Diag H/D
                
                L = [(ox-1,oy+1),(ox-1,oy),(ox,oy+1)]
                
            elif ox - x >0 and oy - y <0:
                
                #Diag B/G
                
                L = [(ox,oy-1),(ox+1,oy-1),(ox+1,oy)]
                
            elif ox - x >0 and oy - y >0:
                
                #Diag B/D
                
                L = [(ox+1,oy),(ox+1,oy+1),(ox,oy+1)]
                
            elif ox == x:
                if oy < y:
                    L = [(ox,oy-1),(ox-1,oy-1),(ox+1,oy-1)]
                elif oy > y :
                    L = [(ox,oy+1),(ox-1,oy+1),(ox+1,oy+1)]
            
            elif oy == y: 
                if ox < x:
                    L = [(ox-1,oy),(ox-1,oy-1),(ox-1,oy+1)]
                elif ox > x:
                    L = [(ox+1,oy),(ox+1,oy-1),(ox+1,oy+1)]
            if len(L) != 0:
                
                E_pos_imp = set(L)
                E_pos = set(self.L_vide)
                
                Occ = E_pos&E_pos_imp

                self.L_vide =list( E_pos - Occ)
            
            print(self.L_vide)
        
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
                role = Ennemi.T_car()
                Ennemi.disparition()
                if role[-2] + role[-1] == 'QG':
                    self._carte.V_atta = 1

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
        x_inf = max(0,int(-self.zonecbt + x))
        x_sup = min(self._carte.dims[0]-1, int(self.zonecbt + x))
        y_inf = max(0,int(-self.zonecbt + y))
        y_sup = min(self._carte.dims[1]-1, int(self.zonecbt + y))
        
        print(x_inf, x_sup)
        print(y_inf,y_sup)
        
        Ennemi = None
        R_plus_petit_unit = self.zonecbt +1
        R_plus_petit_bat = self.zonecbt + 1
        
        
        for i in range(x_inf,x_sup+1):
            for j in range(y_inf,y_sup+1):
                Obj = self._carte.ss_carte[i][j]
                if Obj != ' ' and Obj !='/' and Obj.T_car()[0] == 'D':
                    R_Obj = math.sqrt((x-i)**2 + (y-j)**2)
                    
                    print(R_Obj,Obj)
                    
                    if Obj.T_car()[2] == 'U' and R_Obj < R_plus_petit_unit:
                        R_plus_petit_unit = R_Obj
                        Ennemi = Obj
                        
                    if Obj.T_car()[2] == 'B' and R_Obj < min(R_plus_petit_bat,R_plus_petit_unit):
                        R_plus_petit_bat = R_Obj
                        Ennemi = Obj
        
        return(Ennemi)
    
    # Début de méthode pour choisir les ennemis récursivement. Mais oh
    # mon dieu qu'est-ce que c'est compliqué! Voir plutôt pour améliorer IA.
    
    
    def chx_ennemi_rec(self,A,x,y):
        if np.shape(A) == (1,1):
            v = A[0,0]
            if v == ' ' or v == '/':
                return((None,self.zonecbt+1,None,self.zonecbt+1))
            elif v.T_car()[0] == 'D':
                i,j = v.coords
                R = math.sqrt((x-i)**2+(y-j)**2)
                if v.T_car()[2] == 'B':
                    return((None,self.zonecbt+1,v,R))
                elif v.T_car()[2] == 'U':
                    return((v,R,None,self.zonecbt+1))
            else:
                return((None,self.zonecbt+1,None,self.zonecbt+1))

        elif np.shape(A) == (0,0) or A.tolist()[0] == []:
            print("OK")
            return((None,self.zonecbt+1,None,self.zonecbt+1))

        else : 
            l,c = np.shape(A)
            A1 = A[:l//2,:c//2]
            A2 = A[l//2:,c//2:]
            
            print(A1,A2)
#            print("Type A1 : ",type(A1))
#            print("Type A2 : ", type(A2))
            print(np.shape(A1))
            print(np.shape(A2))
            
            U1,ru1,B1,rb1 = self.chx_ennemi_rec(A1,x,y)
            U2,ru2,B2,rb2 = self.chx_ennemi_rec(A2,x,y)
            
            if ru1 > ru2:
                r_min_u = ru2
                umin = U2
            else:
                r_min_u = ru1
                umin = U1
            
            if rb1 > rb2:
                r_min_b = rb2
                bmin = B2
            
            else:
                r_min_b = rb1
                bmin = B1
            
            return(umin,r_min_u,bmin,r_min_b)
            
    def combat_rec(self):
        x,y = self.coords
        x_inf = max(0,int(-self.zonecbt + x))
        x_sup = min(self._carte.dims[0]-1, int(self.zonecbt + x))
        y_inf = max(0,int(-self.zonecbt + y))
        y_sup = min(self._carte.dims[1]-1, int(self.zonecbt + y))
        
        A = self._carte.ss_carte[x_inf:x_sup+1,y_inf:y_sup+1]
        
        U,r_min_u,B,r_min_b = self.chx_ennemi_rec(A,x,y)
        
        if U == None and B == None:
            print("%s n'a blessé personne"%(self.T_car()) )
        else:
            if r_min_u > r_min_b:
                Ennemi = B
            else:
                Ennemi = U
            
            print( "%s a blessé %s"%(self.T_car(), Ennemi.T_car() ) )
            Ennemi.sante = Ennemi.sante - self.capcbt
            if Ennemi.sante <= 0:
                role = Ennemi.T_car()
                Ennemi.disparition()
                if role[-2] + role[-1] == 'QG':
                    self._carte.V_atta = 1
   
        
        
        
#        
        
        
    def disparition(self):
        print("%s est mort! \n"%(self.T_car()))
        x,y = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        k = self.num_joueur
        self._carte.L_joueur[k]._liste_unite.remove(self)
        
#                Supprimer de carte; de ss_carte; de L_unite; 


class Scorpion(Unites_Humain_Attaquant):
    """
    Classe spécialisant Unites_Humain_Attaquant pour représenter une Fourmi.
    """
    Id = 0
    def __init__(self,role,carte,x,y,k, L_ennemi = [], L_autres_joueurs = []):
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
        self.num_joueur = k
        self.id = self._carte.L_joueur[k].IdU
        self._carte.L_joueur[k].IdU += 1
        self.capmvt = Constante.capmvt_S
        self.capcbt = Constante.capcbt_S
        self.zonecbt = math.sqrt(2)
    
    def car(self):
        return 'S '
    
    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "%s_U_S%i"%(self._role, self.id )
    
    def action(self):
        self.combat_rec()
        return(None)
    
