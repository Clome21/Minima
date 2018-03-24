
class Batiment(object):
    """
    Classe décrivant les comportement par défaut des batiments. Peut-être 
    utilisée en l'état ou sous classée pour définir des comportements différents.
    """
    def __init__(self, abscisse, ordonnee, cart,capacite=20):
        """
        Crée un Batiment aux coordonnées désirées.
        
        Paramètres
        ----------
        abscisse, ordonnée: int
            Les coordonnées auxquelles le batiment sera créé.
            
        capacité: int
            niveau de santé maximal du batiment. Vaut 20 par défaut.
        """
        self._max = capacite
        self.__sante = 20
        self._cart = cart
        self.coords = abscisse, ordonnee

    def __str__(self):
        """
        Affiche l'état courant du batiment.
        
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
            self.sante, self._max
            )
    
    def car(self):
        """
        Renvoie l'identifiant de l'espèce de l'animal.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        c: str
            Le caractère représentant l'animal.
        """
        return 'B' 

    
    def affichage(self):
        print(str(self))

#    def attaquer(self):
#        """
#        Le batiment perd un niveau de sante si attaque par ennemie
#        """

    @property
    def coords(self):
        """
        coords: tuple
            Les coordonnées du batiment sur le plateau de jeu
        """
        return self.__coords

    @property
    def x(self):
        """
        x: nombre entier
            Abscisse du batiment
        """
        return self.coords[0]

    @property
    def y(self):
        """
        y: nombre entier
            Ordonné du batiment
        """
        return self.coords[1]

    @coords.setter
    def coords(self, nouv_coords):
        """
        Met à jour les coordonnées du batiment.
        Garantit qu'ils arrivent dans la zone définie par
        la map self._cart.
    
        Paramètres
        ----------
        nouv_coords : tuple représentant les coordonnées auquelles 
                      le batiment essaie de se rendre.
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
            Le niveau de santé du batiment. Si ce niveau arrive à 0 le batiment
            est marqué comme détruit et sera retiré du plateau de jeu
        """
        return self.__sante
    
    @sante.setter
    def sante(self, value):
        """
        Met à jour le niveau de santé du batiment. Garantit que la valeur arrive 
        dans l'intervalle [0, self._max]. Met à 0 les valeurs négatives, ne
        fait rien pour les valeurs trop grandes.
        """
        if value <= self._max:
            self.__sante = value
        if value <= 0:  # <= car certaines cases enlèvent plus de 1 en santé
            value = 0   # ce qui gèrera les décès plus tard
            
class QG(Batiment):
    """
    Classe spécialisant Batiments pour représenter le QG.
    """
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.sante = self._max
        self.name = "QG"

    def car(self):
        return 'Q'
    
    def T_car(self):
        return("D_B_QG")
    



class Panneau_solaire(Batiment):
    """
    Classe spécialisant Batiments pour représenter le panneau solaire.
    """
    Id = 0
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.name = "Panneau_solaire"
        self.cout_E=2
        self.cout_M=2
        self.prod_E=5
        self.id = Panneau_solaire.Id
        Panneau_solaire.Id += 1
        self.sante = self._max
        
    def car(self):
        return 'P'
    
    def T_car(self):
        return("%D_B_P%i"%( self.id ))


    
class Foreuse(Batiment):
    """
    Classe spécialisant Batiments pour représenter le panneau solaire.
    """
    Id = 0
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.name = "Foreuse"
        self.cout_E=2
        self.cout_M=3
        self.prod_M=5
        self.id = Foreuse.Id
        Foreuse.Id += 1
        self.sante = self._max

    def car(self):
        return 'F'
    
    def T_car(self):
        return("%D_B_F%i"%( self.id ))
    
        

            
            
            
            
            
