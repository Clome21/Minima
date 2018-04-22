from numpy.random import randint,choice
from Constantes import Constante
import numpy as np
import math





class Unite_IA_Facile():
    """
    Classe décrivant les comportement par défaut de l'IA niv facile. Peut-être 
    utilisée en l'état ou sous classée pour définir des comportements de
    déplacement différents.
    """
    def __init__(self, abscisse, ordonnee, carte,capacite=10):
        """
        Crée une Unite_IA aux coordonnées désirées.
        
        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles l'Unite_IA sera créé.
            
        capacité: int
            niveau de santé maximal de l'Unite_IA. Vaut 10 par défaut.
        """
        self._max = capacite
        self.__sante = 10
        self._carte = carte
        self.coords = abscisse, ordonnee  
        self._carte.ss_carte[abscisse][ordonnee] = self


        self._carte.append(self)


    def __str__(self):
        """
        Affiche l'état courant de l'Unite_IA générée.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        s: str
            La chaîne de caractères qui sera affichée via ''print''
        """
        return "%s : position (%i, %i) etat %i/%i "%(
            self.T_car(), self.x, self.y,
            self.sante, self._max )
    
    def car(self):
        """
        Renvoie l'identifiant de l'Unite_IA.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        c: str
            Le caractère représentant l'Unite_IA.
        """
        return 'U'    

    @property
    def coords(self):
        """
        coords: tuple
            Les coordonnées de l'Unite_IA sur le plateau de jeu
        """
        return self.__coords

    @property
    def x(self):
        """
        x: nombre entier
            Abscisse de l'Unite_IA
        """
        return self.coords[0]

    @property
    def y(self):
        """
        y: nombre entier
            Abscisse de l'Unite_IA
        """
        return self.coords[1]

    @coords.setter
    def coords(self, nouv_coords):
        """
        Met à jour les coordonnées de l'Unite_IA.
        Garantit qu'elles arrivent dans la zone définie par
        la zone de jeu self._cart.
    
        Paramètres
        ----------
        nouv_coords : tuple représentant les coordonnées auquelles 
                      l'Unite_IA essaie de se rendre.
        """
        x, y = nouv_coords
        x = min(x, self._carte.dims[0]-1)
        x = max(x, 0)
        y = min(y, self._carte.dims[1]-1)
        y = max(y, 0)
        self.__coords = (x, y)

    @property
    def sante(self):
        """
        sante: float
            Le niveau de santé de lUnite_IA. Si ce niveau arrive à 0 l'animal
            est marqué comme mort et sera retiré du plateau de jeu
        """
        return self.__sante
    
    @sante.setter
    def sante(self, value):
        """
        Met à jour le niveau de santé de lUnite_IA. Garantit que la valeur arrive 
        dans l'intervalle [0, self._max]. Met à 0 les valeurs négatives, ne
        fait rien pour les valeurs trop grandes.
        """
        if value <= self._max:
            self.__sante = value
        if value <= 0:  # <= car certaines cases enlèvent plus de 1 en santé
            value = 0   # ce qui gèrera les décès plus tard

    def affichage(self):
        print(str(self))
              
            
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
            print("%r n'a blessé personne"%(self.T_car()) )
    
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

        
        return(self.L_vide)        
    
    def disparition(self):
        print("%s est mort! \n"%(self.T_car()))
        (x,y) = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        k = self.num_joueur
        self._carte.L_joueur[k]._liste_unite.remove(self)
        
        
class Scorpion0(Unite_IA_Facile):

    
    def __init__(self, role, cart, x, y, k):
        super().__init__(x, y, cart)
#        self.name = "Scorpion"
        self.id =  self._carte.L_joueur[k].IdU 
        self._role = role
        self.num_joueur = k
        self._carte.L_joueur[k].IdU += 1
        self.capmvt = Constante.capmvt_S0
        
        self.capcbt = Constante.capcbt_S0
        self.zonecbt = math.sqrt(2)

    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "%s_U_S0%i"%(self._role, self.id )
    
    def car(self):
        return 's '
       
    
    def bouger(self):
        """
        Mouvement aléatoire uniforme dans un rayon d'une case vers le centre ou le cotée autour
        de la position courante, mais ne peut passer a travers les cases marquées par /. Utilise les 
        zones délimité par droite1 et droite2. Le QG vers lequel les fourmis essaient de ce diriger se trouve 
        à l'ntersection de ces deux droites.
        """
        L_dep_poss  = self.mvt_poss()
        print(L_dep_poss)
        if L_dep_poss != []:
            xi, yi = self.coords
            k = randint(len(L_dep_poss))
            X,Y = L_dep_poss[k]
            self.coords = (X,Y)
            self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]
        return(self.coords)
    
    def action(self):
        self.combat()
        return(None)
        
        




 


            
