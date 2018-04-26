
class Batiment(object):
    """
    Classe décrivant les comportement par défaut des batiments. 
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
        self._carte = cart
        self.coords = abscisse, ordonnee
        self._carte.ss_carte[abscisse][ordonnee] = self
        self._carte.append(self)

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
        return "%r : position (%i, %i) etat %i/%i"%(
            self.T_car(), self.x, self.y,
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
        """ Affiche le batiment, selon la méthode str.
        """
        print(str(self))

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
            Ordonnée du batiment
        """
        return self.coords[1]

    @coords.setter
    def coords(self, nouv_coords):
        """
        Met à jour les coordonnées du batiment.
        Garantit qu'ils arrivent dans la zone définie par
        la map self._carte.
    
        Paramètres
        ----------
        nouv_coords : tuple représentant les nouvelles coordonnées du
        batiment.
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
        if value <= 0:  # <= car certaines unités pourraient enlever plus de 1 en santé
            value = 0   # ce qui gèrera les destructions.
    

            
class QG(Batiment):
    """
    Classe spécialisant Batiments pour représenter le QG.
    """
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.sante = self._max


    def car(self):
        """Méthode permettant d'afficher le batiment sur la carte. Elle renvoie
        le symbole associé au batiment.
        """
        return 'Q '
    
    def T_car(self):
        """Méthode contenant l'ensemble des informations permettant d'identifier le batiment.
        Dans l'ordre : 
            D : le rôle du joueur possédant l'objet. Ici, le défenseur.
            B : le type global de l'objet. Ici, batiment.
            QG : le role de l'objet. Ici, QG.
        """
        return("D_B_QG")
    
    def disparition(self):
        """ Méthode permettant de détruire le batiment. Elle supprime celui-ci
        de l'ensemble des listes/arrays où le batiment est stocké.
        """
        print("%s est mort! \n"%(self.T_car()))
        x,y = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        self._carte.L_joueur[0]._liste_bat[0].remove(self)



class Panneau_solaire(Batiment):
    
    Id=0
    """
    Classe spécialisant Batiments pour représenter le panneau solaire.
    """
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.sante = self._max
        self.id = Panneau_solaire.Id
        Panneau_solaire.Id += 1

    def T_car(self):
        """Méthode contenant l'ensemble des informations permettant d'identifier le batiment.
        Dans l'ordre : 
            D : le rôle du joueur possédant l'objet. Ici, le défenseur.
            B : le type global de l'objet. Ici, batiment.
            P : le role de l'objet. Ici, Panneau Solaire.
            self.id : l'identifiant de l'objet, afin de le différencier des autres
            panneaux solaires.
        """
        return("D_B_P%i"%( self.id ))
        
    def car(self):
        """Méthode permettant d'afficher le batiment sur la carte. Elle renvoie
        le symbole associé au batiment.
        """
        return 'P '
    
    def disparition(self):
        """ Méthode permettant de détruire le batiment. Elle supprime celui-ci
        de l'ensemble des listes/arrays où le batiment est stocké.
        """
        print("%s est mort! \n"%(self.T_car()))
        x,y = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        self._carte.L_joueur[0]._liste_bat[1].remove(self)

    
class Foreuse(Batiment):
    
    Id=0
    """
    Classe spécialisant Batiments pour représenter le panneau solaire.
    """
    def __init__(self, x, y, cart):
        super().__init__(x, y, cart)
        self.sante = self._max
        self.id = Foreuse.Id
        Foreuse.Id += 1

    def car(self):
        """Méthode permettant d'afficher le batiment sur la carte. Elle renvoie
        le symbole associé au batiment.
        """
        return 'F '
    
    def T_car(self):
        """Méthode contenant l'ensemble des informations permettant d'identifier le batiment.
        Dans l'ordre : 
            D : le rôle du joueur possédant l'objet. Ici, le défenseur.
            B : le type global de l'objet. Ici, batiment.
            F : le role de l'objet. Ici, Foreuse.
            self.id : l'identifiant de l'objet, afin de le différencier des autres
            foreuses.
        """
        return("D_B_F%i"%( self.id ))
    
    def disparition(self):
        """ Méthode permettant de détruire le batiment. Elle supprime celui-ci
        de l'ensemble des listes/arrays où le batiment est stocké.
        """
        print("%s est mort! \n"%(self.T_car()))
        x,y = self.coords
        self._carte.remove(self)
        self._carte.ss_carte[x][y] = ' '
        self._carte.L_joueur[0]._liste_bat[2].remove(self)
        

            
            
            
            
            
