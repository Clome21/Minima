from numpy.random import randint,choice
from Constantes import Constante
import numpy as np
import math





class Unite_IA_Facile():
    """
    Classe décrivant les comportement par défaut de l'IA de niveau 0 (ou facile). 
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
        """ Affiche l'unité, selon la méthode str.
        """
        print(str(self))
              
            
    def combat(self):
        """
        Méthode permettant à l'unité de combattre, si un objet ennemi se trouve 
        dans sa zone d'attaque.
        L'unité recherche les ennemis dans sa zone de combat et sélectionne 
        l'objet le plus proche grâce à la méthode chx_ennemi.
        Si il n'y a pas d'objet à attaquer, la méthode le signale.
        Si il y a bien un objet, la méthode signale quel est l'objet blessé par l'unité.
        Cet objet perd alors de la vie, et est supprimé si sa santé devient nulle 
        ou négative.
        Si cet objet détruit est le QG, la variable V_atta, désignant la victoire ou non
        des attaquants, passe à 1. Les attaquants gagnent alors.
        
        Paramètres : 
        ------------
        Aucun.
        
        Renvoie :
        ----------
        Rien.
        
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
        Méthode sélectionnant l'objet ennemi le plus proche de l'unité.
        Elle parcourt les cases dans le rayon d'attaque de l'unité, et sélectionne
        les objets ennemis dans ce rayon.
        Elle sélectionne en priorité les unités ennemis les plus proches; mais si
        un batiment ennemi est plus proche de l'unité que les autres unités ennemis, 
        l'unité en train de combattre attaquera alors le batiment.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie :
        ----------
        Ennemi : Objet (Unité ou Batiment)
            L'ennemi le plus proche de l'unité en train de combattre.
        
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
    
    def chx_ennemi_rec(self,A,x,y):
        """
        Méthode sélectionnant l'objet ennemi le plus proche de l'unité, de façon
        récursive.
        Cette méthode se base sur la technique de "Diviser pour régner". Elle sélectionne
        la sous-carte contenant les cases dans le rayon de combat de l'unité.
        Elle coupe ensuite cette sous-carte en quatres carrés plus petits, jusqu'à
        ce que ce carré soit de taille (1,1).
        Elle détermine alors si l'unité sur cette case est un batiment, ou une unité,
        et renvoie alors sa distance par rapport à l'unité combattante.
        
        Elle compare ensuite les distances des unités (et des batiments) par rapport
        à l'unité combattante, et renvoie l'unité ennemie la plus proche, sa distance
        par rapport à l'unité combattante, le batiment ennemi le plus proche, et sa
        distance par rapport à l'unité combattante.
        
        Paramètres
        ----------
        A : array
            Sous-carte contenant une partie (la totalité au départ) des cases 
            dans le rayon de combat de l'unité combattante.
            
        x,y : int
            Abscisse et ordonnée de l'unité combattante.
        
        Renvoie :
        ----------
        umin : Objet Unité 
            L'unité ennemie la plus proche de l'unité combattante.
            
        r_min_u : float
            La distance entre l'unité ennemie la plus proche de l'unité
            combattante et l'unité combattante.
        
        bmin : Objet Batiment
            Le batiment ennemi le plus proche de l'unité combattante.
        
        r_min_b : float
            La distance entre le batiment ennemi le plus proche de l'unité
            combattante et l'unité combattante.
        
        """
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

        elif np.shape(A) == (0,0) or A.tolist() == [] or A.tolist()[0] == []:
            print("OK")
            return((None,self.zonecbt+1,None,self.zonecbt+1))

        else : 
            l,c = np.shape(A)
            A1 = A[l//2:,c//2:]
            A2 = A[l//2:,:c//2]
            A3 = A[:l//2,c//2:]
            A4 = A[:l//2,:c//2]

            print(A1,A2,A3,A4)
            print(np.shape(A1))
            print(np.shape(A2))
            print(np.shape(A3))
            print(np.shape(A4))
            
            U1,ru1,B1,rb1 = self.chx_ennemi_rec(A1,x,y)
            U2,ru2,B2,rb2 = self.chx_ennemi_rec(A2,x,y)
            U3,ru3,B3,rb3 = self.chx_ennemi_rec(A3,x,y)
            U4,ru4,B4,rb4 = self.chx_ennemi_rec(A4,x,y)
            
            Lu = [ru1,ru2,ru3,ru4]
            LU = [U1,U2,U3,U4]
            Lb = [rb1,rb2,rb3,rb4]
            LB = [B1,B2,B3,B4]
            
            r_min_u = min(Lu)
            umin = LU[ Lu.index(r_min_u) ]
            
            r_min_b = min(Lb)
            bmin = LB[ Lb.index(r_min_b) ]
            
            return(umin,r_min_u,bmin,r_min_b)
            
    def combat_rec(self):
        """
        
        Méthode permettant à l'unité de combattre, si un objet ennemi se trouve 
        dans sa zone d'attaque.
        Elle sélectionne les cases de la sous-carte correspondant à la zone d'attaque
        de l'unité combattante, et applique la méthode chx_ennemi_rec pour trouver
        le batiment et l'unité ennemie les plus proches. Cette dernière méthode est
        récursive.
        Si il n'y a pas d'objet à attaquer, la méthode le signale.
        Si il y a bien un objet, la méthode sélectionne lequel des deux est le plus
        proche de l'unité combattante. Cet objet est alors blessé : il perd de la vie, 
        et est supprimé si sa santé devient nulle ou négative.
        Si cet objet détruit est le QG, la variable V_atta, désignant la victoire ou non
        des attaquants, passe à 1. Les attaquants gagnent alors.
        La méthode signale également quel est l'objet blessé par l'unité.
        
        Paramètres :
        ------------
        Aucun.
        
        Renvoie :
        ---------
        Rien.
        
        """
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
        
        return(Ennemi)
    
    def mvt_poss(self):
        """ Méthode permettant de sélectionner les cases sur lesquelles 
        l'unité peut se déplacer. Ces cases doivent être vides.
        Dans un premier temps, la méthode sélectionne les cases vides et non vides
        dans la zone de déplacement de l'unité.
        Cependant, une case non vide bloque également les cases autour de celles-ci
        (pour des questions de champ de vision, ou d'impossibilité de déplacement au
        delà de l'obstacle). 
        Donc dans un second temps, la méthode retire de la liste les cases qui 
        sont bloqués par les obstacles au déplacement de l'unité.
        Les cases retirées dépendent de la position de l'unité par rapport aux obstacles.
        
        A noter : actuellement, la façon dont les cases bloquées sont choisies a été
        prévu pour des unitées dont les déplacements sont inférieurs ou égaux à 2. 
        Une MAJ pourra être faite plus tard pour corriger ce problème.
        
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        L_vide : list
            La liste contenant toutes les cases où l'unité peut se déplacer.
        
        """
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
        """ Méthode permettant de détruire l'unité. Elle supprime celui-ci
        de l'ensemble des listes/arrays où l'unité est stockée.
        
        Paramètres : 
        ------------
        Aucun.
        
        Renvoie :
        ---------
        Rien.
        
        """
        print("%s est mort! \n"%(self.T_car()))
        (x,y) = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        k = self.num_joueur
        self._carte.L_joueur[k]._liste_unite.remove(self)
        
        
class Scorpion0(Unite_IA_Facile):
    """ Classe spécialisant Unites_IA_facile pour représenter un scorpion de niveau 0.    
    """
    def __init__(self, role, cart, x, y, k):
        """Permet d'initialiser l'unité.
            
    Paramètres
    ----------
    
    role : str
    Le rôle du joueur possèdant l'unité
            
    cart : classe Map
    La carte sur laquelle évolue l'unité.
    
    x, y : int
    Les coordonnées de l'unité en abscisse et en ordonnée
    
    k : int
    La position du joueur possédant l'unité, dans la liste L_joueur.
        """
        super().__init__(x, y, cart)
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
        """Méthode permettant d'afficher le scorpion sur la carte. Elle renvoie
        le symbole associé au scorpion.
        """
        return 's0'
       
    
    def bouger(self):
        """
        Permet le déplacement de l'unité IA. Pour une IA facile (c'est-à-dire de niveau 0), l'unité va se déplacer
        aléatoirement sur le plateau de jeu. Les positions possibles sont récupérées via la méthode mvt_poss().
        
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
        """ Méthode définissant l'action de l'unité, après s'être déplacée.
        Pour un scorpion, cette action est une action de combat.
        
        A noter : il existe deux méthodes pour cette action de combat : une 
        méthode itérative, et une méthode récursive.
        """
        self.combat()
        return(None)
        

