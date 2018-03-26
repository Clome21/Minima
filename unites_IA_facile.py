from numpy.random import randint,choice
from Constantes import Constante
import numpy as np
import math





class Unite_IA():
    """
    Classe décrivant les comportement par défaut de l'IA niv facile. Peut-être 
    utilisée en l'état ou sous classée pour définir des comportements de
    déplacement différents.
    """
    def __init__(self, abscisse, ordonnee, cart,unite_IA,capacite=10):
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
        self._carte.ss_carte[abscisse][ordonnee] = self


        self.degat=2
        self.rayon_hit_box=0,5
        self._unite_IA=unite_IA


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
        return "%c : position (%i, %i) etat %i/%i "%(
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
   
    
    def distance (self,x1,y1,x2,y2):
        Xdistance = x2-x1
        Ydistance = y2-y1        
        return (math.sqrt(Xdistance**2+Ydistance**2))
    
#    def collision_unite_IA (self,a,c):
#            for b in self._unite_IA:
#                #d=self.distance(a,c,b.x,b.y)           
#                if (a==b.x and c==b.y):
#                    print("collision",a,c)
#                else:
#                    return False

        def mvt_poss(self):
            x,y = self.coords
        
            self.L_vide = []
            x_inf = max(0,int(-self.capmvt + x))
            x_sup = min(self._carte.dims[0], int(self.capmvt + x))
            y_inf = max(0,int(-self.capmvt + y))
            y_sup = min(self._carte.dims[1], int(self.capmvt + y))
        
            for i in range(x_inf,x_sup+1):
                for j in range(y_inf,y_sup+1):
                    Obj = self._carte.ss_carte[i][j]
                    if Obj == ' ' :
                        self.L_vide.append((i,j))
            return(self.L_vide)

    
class Scorpion1(Unite_IA):
    """
    Classe spécialisant Unite_IA pour représenter une Fourmi.
    """
    Id=0
    
    def __init__(self, x, y, cart,unite_IA,identifiant):
        super().__init__(x, y, cart,unite_IA)
        self.name = "Scorpion"
        self.id = Scorpion1.Id 
        Scorpion1.Id += 1
        self.capmvt = 1

    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "A_U_S1%i"%( self.id )
    
    def car(self):
        return 's'
       
    
    
    def bouger(self):
        """
        Mouvement aléatoire uniforme dans un rayon d'une case vers le centre ou le cotée autour
        de la position courante, mais ne peut passer a travers les cases marquées par /. Utilise les 
        zones délimité par droite1 et droite2. Le QG vers lequel les fourmis essaient de ce diriger se trouve 
        à l'ntersection de ces deux droites.
        """
        L_vide = self.mvt_poss()
        xi, yi = self.coords
        
#-------------------Zone Est-----------------------------
        if ((Constante.ymax>=self.droite1(Constante.xmax)) and (Constante.ymax<=self.droite2(Constante.xmax))):
            X = xi + randint(-1,2)
            Y = yi + randint(0,2)
        
            if (X,Y) not in L_vide :
                pass
                
            else:                
                if (xi == self._cart.dims[0]-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and (((yi> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2-1 and yi< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1)) or((yi> (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2) and yi< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+Constante.H_Z_Constructible+2)):
                    while (X,Y) not in L_vide:
                        Y = yi + randint(-1,2)
                    self.coords = (X,Y)
                elif ((self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and ((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1) and (self.y< (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2))) :
                    while (X,Y) not in L_vide:
                        X = xi - randint(0,2)
                    self.coords = (X,Y)                        
                else:
                    while (X,Y) not in L_vide:
                        X = xi + randint(0,2)
                        Y = yi + randint(-1,2)
                    self.coords = (X,Y)

#-------------------Zone Ouest-----------------------------                                 
        elif ((self.y<=self.droite1(self.x)) and (self.y>=self.droite2(self.x))):
            X = xi + randint(-1,2)
            Y = yi + randint(0,2)
        
            if (X,Y) not in L_vide :
                pass
            
            else:
                if (self.x == self._cart.dims[0]-Constante.L_Z_Constructible-2-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and (((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2-1 and self.y< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1)) or((self.y> (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2) and self.y< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+Constante.H_Z_Constructible+2)):
                    while (X,Y) not in L_vide:
                        Y = yi + randint(-1,2)
                    self.coords = (X,Y)
                elif ((self.x == self._cart.dims[0]-Constante.L_Z_Constructible-2-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and ((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1) and (self.y< (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2))) :
                    while (X,Y) not in L_vide:
                        X = xi + randint(0,2)
                    self.coords = (self.x+randint(0,2),self.y)
                else:
                    X = xi + randint(0,2)
                    Y = yi + randint(-1,2)
                    self.coords = (X,Y)

#-------------------Zone Sud-----------------------------                                    
        elif ((self.y>self.droite1(self.x)) and (self.y>self.droite2(self.x))):
            X = xi + randint(-1,2)
            Y = yi + randint(0,2)
        
            if (X,Y) not in L_vide :
                pass
            
            else:
                if ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2-1 and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) or((self.x> (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2) and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+Constante.L_Z_Constructible+2))): 
                    while (X,Y) not in L_vide:
                        X = xi + randint(1,2)
                    self.coords = (X,Y)
                elif ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) and (self.x< (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2))) :
                    while (X,Y) not in L_vide:
                        Y = yi - randint(0,2)
                    self.coords = (X,Y)
#            else:
#                self.coords = (self.x+randint(-1,2),self.y-randint(0,2))        
# 
#-------------------Zone Nord-----------------------------
#        elif ((self.y<self.droite1(self.x)) and (self.y<self.droite2(self.x))):
#            if ((self.y == self._cart.dims[1]-Constante.H_Z_Constructible-2-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2-1 and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) or((self.x> (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2) and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+Constante.L_Z_Constructible+2))): 
#                self.coords = (self.x+randint(-1,2),self.y)
#            elif ((self.y == self._cart.dims[1]-Constante.H_Z_Constructible-2-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) and (self.x< (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2))) :               
#                self.coords = (self.x,self.y+randint(0,2))
#            else: 
#                self.coords = (self.x+randint(-1,2),self.y+randint(0,2))
#        X,Y = self.coords
#        self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]
#        for b in self._unite_IA: 
#            if self.id==b.id:
#                continue
#            elif ((self.x==b.x) and (self.y==b.y)):
#                print("collision",self.x,self.y)
        
        self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]
        return(self.coords)
                
class Scorpion2(Unite_IA):
    
    Id=0
    """
    Classe spécialisant Unite_IA pour représenter une Fourmi.
    """
    def __init__(self, x, y, cart, unite_IA):
        super().__init__(x, y, cart, unite_IA)
        self.name = "Scorpion"
        self.id = Scorpion2.Id 
        Scorpion2.Id += 1
        self.capmvt = 1

    def T_car(self):
        """ Renvoie l'ensemble des caractéristiques de l'objet étudié """
        return "A_U_S2%i"%( self.id )
    
    def car(self):
        return 'S'
    
    def bouger(self):
        """
        Mouvement aléatoire uniforme dans un rayon d'une case vers le centre ou le cotée autour
        de la position courante, mais ne peut passer a travers les cases marquées par /. Utilise les 
        zones délimité par droite1 et droite2. Le QG vers lequel les fourmis essaient de ce diriger se trouve 
        à l'ntersection de ces deux droites.
        """

        L_vide = self.mvt_poss()
        xi, yi = self.coords
        
        X_dep = choice([-1,1])
        Y_dep = choice([0,1])
        X = xi + X_dep
        Y = yi + Y_dep
        
        if (X,Y) not in L_vide :
            pass
        else:
            while (X,Y) not in L_vide:
#        while self.capmvt < math.sqrt((X -self.x)**2 + (Y-self.y)**2) :
                X_dep = randint(-1,2)
                Y_dep = randint(-1,2)
                X = xi + X_dep
                Y = yi + Y_dep
                self.coords = (X, Y)
                
        self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]
        return(self.coords)
#        if ((self.y>=self.droite1(self.x)) and (self.y<=self.droite2(self.x))):
#            if (self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and (((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2-1 and self.y< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1)) or((self.y> (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2) and self.y< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+Constante.H_Z_Constructible+2)):
#                self.coords = (self.x,self.y+choice([-1,1]))
#            elif ((self.x == self._cart.dims[0]-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and ((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1) and (self.y< (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2))) :
#                self.coords = (self.x-1,self.y)
#            else:
#                self.coords = (self.x-1,self.y+choice([-1,1]))
#        
#        elif ((self.y<=self.droite1(self.x)) and (self.y>=self.droite2(self.x))):
#            if (self.x == self._cart.dims[0]-Constante.L_Z_Constructible-2-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and (((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2-1 and self.y< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1)) or((self.y> (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2) and self.y< (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+Constante.H_Z_Constructible+2)):
#                self.coords = (self.x,self.y+choice([-1,1]))
#            elif ((self.x == self._cart.dims[0]-Constante.L_Z_Constructible-2-1-((self._cart.dims[0]-1-Constante.L_Z_Constructible-2)/2)) and ((self.y> (self._cart.dims[1] - Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2-1) and (self.y< (self._cart.dims[1] -Constante.H_Z_Constructible-2 )/2+(Constante.H_Z_Constructible+2)/2))) :
#                self.coords = (self.x+1,self.y)
#            else:
#                self.coords = (self.x+1,self.y+choice([-1,1]))
#                
#        elif ((self.y>self.droite1(self.x)) and (self.y>self.droite2(self.x))):
#            if ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2-1 and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) or((self.x> (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2) and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+Constante.L_Z_Constructible+2))): 
#                self.coords = (self.x+choice([-1,1]),self.y)
#            elif ((self.y == self._cart.dims[1]-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) and (self.x< (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2))) :
#                self.coords = (self.x,self.y-1)
#            else:
#                self.coords = (self.x+choice([-1,1]),self.y-1)        
#        
#        elif ((self.y<self.droite1(self.x)) and (self.y<self.droite2(self.x))):
#            if ((self.y == self._cart.dims[1]-Constante.H_Z_Constructible-2-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2-1 and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) or((self.x> (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2) and self.x< (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+Constante.L_Z_Constructible+2))): 
#                self.coords = (self.x+choice([-1,1]),self.y)
#            elif ((self.y == self._cart.dims[1]-Constante.H_Z_Constructible-2-((self._cart.dims[1]-1-Constante.H_Z_Constructible)/2)) and ((self.x> (self._cart.dims[0] - Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2-1) and (self.x< (self._cart.dims[0] -Constante.L_Z_Constructible-2 )/2+(Constante.L_Z_Constructible+2)/2))) :               
#                self.coords = (self.x,self.y+1)
#            else: 
#                self.coords = (self.x+choice([-1,1]),self.y+1)
#                
        X,Y = self.coords
        self._carte.ss_carte[xi][yi], self._carte.ss_carte[X][Y] = self._carte.ss_carte[X][Y], self._carte.ss_carte[xi][yi]


            