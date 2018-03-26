from Batiments import Foreuse,Panneau_solaire
from Constantes import Constante


class Un_Tour_Du_Joueur():


    
    def __init__(self,carte):
        self._carte = carte
        self.L_joueur = self._carte.L_joueur
  
        self.metal_tot=Constante.metal_tot
        self.energie_tot=Constante.energie_tot
        self.nb_unite_IA_In_Wave=0

        self.unite_IA=[]
        self._liste_bat =[]
        self.unite_IA_in_wave=[]
        
        

        #self.Fourmi_Facile=Fourmi_Facile(0,0,self,self,self)
 
            
    def placer_une_foreuse(self)   :
        """
        Permet au joueur s'il le souhaite et s'il en a le droit de construire le batiment Foreuse
        Mets également à jour la quantité de ressource à sa disposition
        """
        while (self.metal_tot>=Constante.cout_M_F and self.energie_tot>=Constante.cout_E_F):
            choix2=input("placer Foreuse ? (YES/NO)")
            if choix2 == 'YES':
                i=float(input("en quelle abscisse ?"))
                j=float(input("en quelle ordonnée ?"))
                for batiment in self.L_batiment:
                    while (i==batiment.x and j==batiment.y) or not ((i>(Constante.xmax-Constante.L_Z_Constructible)/2 and i<((Constante.xmax-Constante.L_Z_Constructible)/2+Constante.L_Z_Constructible)) and (j>(Constante.ymax-Constante.H_Z_Constructible)/2 and j<((Constante.ymax-Constante.H_Z_Constructible)/2+Constante.H_Z_Constructible+(Constante.ymax-Constante.H_Z_Constructible-1)/2))):
                        i=float(input("Emplacement non valide : quelle coordonnée en x ?"))
                        j=float(input("Emplacement non valide : quelle coordonnée en y ?"))
                U = Foreuse(i,j,self._carte)
                self._carte.append(U)
                self._liste_bat.append(U)                
                self.metal_tot=self.metal_tot-Constante.cout_M_F
                self.energie_tot=self.energie_tot-Constante.cout_E_F
                        
            elif choix2=='NO':
                break

    def placer_un_Panneau_solaire(self):
        """
        Permet au joueur s'il le souhaite et s'il en a le droit de construire le batiment Panneau solaire
        Mets également à jour la quantité de ressource à sa disposition
        """
        while (self.metal_tot>=Constante.cout_M_P and self.energie_tot>=Constante.cout_E_P):
            choix2=input("placer Panneau solaire ? (YES/NO)")
            if choix2 == 'YES':
                i=float(input("en quelle abscisse ?"))
                j=float(input("en quelle ordonnée ?"))
                for batiment in self.L_batiment:
                    while (i==batiment.x and j==batiment.y) or not ((i>(Constante.xmax-Constante.L_Z_Constructible)/2 and i<(Constante.xmax+(Constante.L_Z_Constructible-1))/2) and (j>(Constante.ymax-(Constante.H_Z_Constructible))/2 and j<(Constante.ymax+(Constante.H_Z_Constructible-1))/2)):
                        i=float(input("Emplacement occupé : quelle coordonnée en x ?"))
                        j=float(input("Emplacement occupé : quelle coordonnée en y ?"))
                U = Panneau_solaire(i,j,self._carte)
                self._carte.append(U)
                self._liste_bat.append(U)
                self.metal_tot=self.metal_tot-Constante.cout_M_P
                self.energie_tot=self.energie_tot-Constante.cout_E_P
                        
            elif choix2=='NO':
                break
    
    def construction_bat(self):
        """
        Permet au joueur s'il le souhaite de placer un batiment
        """
        choix=input("placer un batiment ? (YES/NO)")
        if choix=='YES':
            Un_Tour_Du_Joueur.placer_une_foreuse(self)
            Un_Tour_Du_Joueur.placer_un_Panneau_solaire(self)
        elif choix=='NO':
            pass
            
        
    def unTour(self):

        """
        Effectue toutes les actions liées à un tour de jeu.
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        Rien
        """
        # rnd.shuffle(self)    Utile si gestion des collisions

        n = len(self.L_joueur)
        for k in range(n):
            print("\\\ Tour du joueur %r ///"%(self.L_joueur[k]._role))
            if self.L_joueur[k]._role[0] == 'D':
                Un_Tour_Du_Joueur.construction_bat(self)
            L_unite = self.L_joueur[k]._liste_unite
            for c in L_unite:
                print("Tour de %r"%(c.T_car()))
                c.bouger()
        
        for obj in self._carte:
            obj.affichage()