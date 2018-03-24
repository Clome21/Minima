from numpy.random import randint,choice
import numpy as np
import math 

class Unite_IA():
    """
    Classe décrivant les comportement par défaut de l'IA niv facile. Peut-être 
    utilisée en l'état ou sous classée pour définir des comportements de
    déplacement différents.
    """
    def __init__(self, abscisse, ordonnee, cart,capacite=10):
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
        self._cart = cart
        self.coords = abscisse, ordonnee  
        cart.ss_carte[abscisse][ordonnee] = self
        self.L=19
        self.H=15
        self.degat=2
        


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
        return "%c : position (%i, %i) etat %i/%i"%(
            self.car(), self.x, self.y,
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
        x = min(x, self._cart.dims[0]-1)
        x = max(x, 0)
        y = min(y, self._cart.dims[1]-1)
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
       
    def droite1(self,x):
        """
        Permet de séparer notre zone de jeu en 2 parties égales
        """
        return -(self._cart.dims[1]/self._cart.dims[0])*x + self._cart.dims[1]
    

    def droite2(self,x):
        """
        Permet de séparer notre zone de jeu en 2 parties égales
        """
        return (self._cart.dims[1]/self._cart.dims[0])*x
    
    
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
    
    
class Scorpion_Facile(Unite_IA):
    """
    Classe spécialisant Unite_IA pour représenter un scorpion.
    """
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.name = "Scorpion"
    
    def car(self):
        return 's'
    
    
    def bouger(self):
        """
        Mouvement aléatoire uniforme dans un rayon d'une case vers le centre ou le cotée autour
        de la position courante, mais ne peut passer a travers les cases marquées par /. Utilise les 
        zones délimité par droite1 et droite2. Le QG vers lequel les fourmis essaient de ce diriger se trouve 
        à l'ntersection de ces deux droites.
        """
        
        if ((self.y>=self.droite1(self.x)) and (self.y<=self.droite2(self.x))):
            if (self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-self.L-2)/2)) and (((self.y> (self._cart.dims[1] - self.H-2 )/2-1 and self.y< (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1)) or((self.y> (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2) and self.y< (self._cart.dims[1] - self.H-2 )/2+self.H+2)):
                self.coords = (self.x,self.y+randint(-1,2))
            elif ((self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-self.L-2)/2)) and ((self.y> (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1) and (self.y< (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2))) :
                self.coords = (self.x-randint(0,2),self.y)
            else:
                self.coords = (self.x-randint(0,2),self.y+randint(-1,2))
        
        elif ((self.y<=self.droite1(self.x)) and (self.y>=self.droite2(self.x))):
            if (self.x == self._cart.dims[0]-self.L-2-1-((self._cart.dims[0]-1-self.L-2)/2)) and (((self.y> (self._cart.dims[1] - self.H-2 )/2-1 and self.y< (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1)) or((self.y> (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2) and self.y< (self._cart.dims[1] - self.H-2 )/2+self.H+2)):
                self.coords = (self.x,self.y+randint(-1,2))
            elif ((self.x == self._cart.dims[0]-self.L-2-1-((self._cart.dims[0]-1-self.L-2)/2)) and ((self.y> (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1) and (self.y< (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2))) :
                self.coords = (self.x+randint(0,2),self.y)
            else:
                self.coords = (self.x+randint(0,2),self.y+randint(-1,2))
                
        elif ((self.y>self.droite1(self.x)) and (self.y>self.droite2(self.x))):
            if ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2-1 and self.x< (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) or((self.x> (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2) and self.x< (self._cart.dims[0] - self.L-2 )/2+self.L+2))): 
                self.coords = (self.x+randint(-1,2),self.y)
            elif ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) and (self.x< (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2))) :
                self.coords = (self.x,self.y-randint(0,2))
            else:
                self.coords = (self.x+randint(-1,2),self.y-randint(0,2))        
        
        elif ((self.y<self.droite1(self.x)) and (self.y<self.droite2(self.x))):
            if ((self.y == self._cart.dims[1]-self.H-2-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2-1 and self.x< (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) or((self.x> (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2) and self.x< (self._cart.dims[0] - self.L-2 )/2+self.L+2))): 
                self.coords = (self.x+randint(-1,2),self.y)
            elif ((self.y == self._cart.dims[1]-self.H-2-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) and (self.x< (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2))) :               
                self.coords = (self.x,self.y+randint(0,2))
            else: 
                self.coords = (self.x+randint(-1,2),self.y+randint(0,2))
    
            
class Scorpion_Moins_Facile(Unite_IA):
    """
    Classe spécialisant Unite_IA pour représenter une Fourmi.
    """
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.name = "Scorpion"
    
    def car(self):
        return 'S'
    
    
    def bouger(self):
        """
        Mouvement aléatoire uniforme dans un rayon d'une case vers le centre ou le cotée autour
        de la position courante, mais ne peut passer a travers les cases marquées par /. Utilise les 
        zones délimité par droite1 et droite2. Le QG vers lequel les fourmis essaient de ce diriger se trouve 
        à l'ntersection de ces deux droites.
        """
        
        if ((self.y>=self.droite1(self.x)) and (self.y<=self.droite2(self.x))):
            if (self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-self.L-2)/2)) and (((self.y> (self._cart.dims[1] - self.H-2 )/2-1 and self.y< (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1)) or((self.y> (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2) and self.y< (self._cart.dims[1] - self.H-2 )/2+self.H+2)):
                self.coords = (self.x,self.y+choice([-1,1]))
            elif ((self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-self.L-2)/2)) and ((self.y> (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1) and (self.y< (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2))) :
                self.coords = (self.x-1,self.y)
            else:
                self.coords = (self.x-1,self.y+choice([-1,1]))
        
        elif ((self.y<=self.droite1(self.x)) and (self.y>=self.droite2(self.x))):
            if (self.x == self._cart.dims[0]-self.L-2-1-((self._cart.dims[0]-1-self.L-2)/2)) and (((self.y> (self._cart.dims[1] - self.H-2 )/2-1 and self.y< (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1)) or((self.y> (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2) and self.y< (self._cart.dims[1] - self.H-2 )/2+self.H+2)):
                self.coords = (self.x,self.y+choice([-1,1]))
            elif ((self.x == self._cart.dims[0]-self.L-2-1-((self._cart.dims[0]-1-self.L-2)/2)) and ((self.y> (self._cart.dims[1] - self.H-2 )/2+(self.H+2)/2-1) and (self.y< (self._cart.dims[1] -self.H-2 )/2+(self.H+2)/2))) :
                self.coords = (self.x+1,self.y)
            else:
                self.coords = (self.x+1,self.y+choice([-1,1]))
                
        elif ((self.y>self.droite1(self.x)) and (self.y>self.droite2(self.x))):
            if ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2-1 and self.x< (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) or((self.x> (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2) and self.x< (self._cart.dims[0] - self.L-2 )/2+self.L+2))): 
                self.coords = (self.x+choice([-1,1]),self.y)
            elif ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) and (self.x< (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2))) :
                self.coords = (self.x,self.y-1)
            else:
                self.coords = (self.x+choice([-1,1]),self.y-1)        
        
        elif ((self.y<self.droite1(self.x)) and (self.y<self.droite2(self.x))):
            if ((self.y == self._cart.dims[1]-self.H-2-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2-1 and self.x< (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) or((self.x> (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2) and self.x< (self._cart.dims[0] - self.L-2 )/2+self.L+2))): 
                self.coords = (self.x+choice([-1,1]),self.y)
            elif ((self.y == self._cart.dims[1]-self.H-2-((self._cart.dims[1]-1-self.H)/2)) and ((self.x> (self._cart.dims[0] - self.L-2 )/2+(self.L+2)/2-1) and (self.x< (self._cart.dims[0] -self.L-2 )/2+(self.L+2)/2))) :               
                self.coords = (self.x,self.y+1)
            else: 
                self.coords = (self.x+choice([-1,1]),self.y+1)

            