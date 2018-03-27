from Batiments import Foreuse,Panneau_solaire
from Constantes import Constante
from Unites_Humain_Defenseur import Robot_combat
from Unites_Humain_Attaquant import Scorpion
from numpy import randint


class Un_Tour_Du_Joueur():


    
    def __init__(self,carte,role):
        self._carte = carte
        self._role = role
        self.L_joueur = self._carte.L_joueur
        self.unite_disp_/_tour=0
        self.metal_tot=Constante.metal_tot
        self.energie_tot=Constante.energie_tot
        self.nb_unite_IA_In_Wave=0

        self.unite_IA=[]
        self.unite_IA_in_wave=[]
        
        
         
            
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
                Obj = self._carte.ss_carte[int(i)][int(j)]
                if Obj == ' ' :
                    U = Foreuse(i,j,self._carte,self)
                    self._carte.append(U)
                    self._carte.L_joueur._liste_bat.append(U)
                    self._carte.ss_carte[i][j]=U
                    self.metal_tot=self.metal_tot-Constante.cout_M_F
                    self.energie_tot=self.energie_tot-Constante.cout_E_F
                    self.coords = i, j
                
                else:   
                    while (Obj!=' ') or not ((i>(Constante.xmax-Constante.L_Z_Constructible)/2 and i<((Constante.xmax-Constante.L_Z_Constructible)/2+Constante.L_Z_Constructible)) and (j>(Constante.ymax-Constante.H_Z_Constructible)/2 and j<((Constante.ymax-Constante.H_Z_Constructible)/2+Constante.H_Z_Constructible+(Constante.ymax-Constante.H_Z_Constructible-1)/2))):
                        i=float(input("Emplacement non valide : quelle coordonnée en x ?"))
                        j=float(input("Emplacement non valide : quelle coordonnée en y ?"))
                    U = Foreuse(i,j,self._carte,self)
                    self._carte.append(U)
                    self._carte.L_joueur.L_batiment.append(U)
                    self._carte.ss_carte[i][j]=U
                    self.metal_tot=self.metal_tot-Constante.cout_M_F
                    self.energie_tot=self.energie_tot-Constante.cout_E_F
                    self.coords = i, j
                    
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
                Obj = self._carte.ss_carte[i][j]
                if Obj == ' ' :
                    U = Panneau_solaire(i,j,self._carte)
                    self._carte.append(U)                
                    self.metal_tot=self.metal_tot-Constante.cout_M_F
                    self.energie_tot=self.energie_tot-Constante.cout_E_F
                    self.coords = i, j
                else:
                    while (Obj!=' ') or not ((i>(Constante.xmax-Constante.L_Z_Constructible)/2 and i<(Constante.xmax+(Constante.L_Z_Constructible-1))/2) and (j>(Constante.ymax-(Constante.H_Z_Constructible))/2 and j<(Constante.ymax+(Constante.H_Z_Constructible-1))/2)):
                        i=float(input("Emplacement occupé : quelle coordonnée en x ?"))
                        j=float(input("Emplacement occupé : quelle coordonnée en y ?"))
                U = Panneau_solaire(i,j,self._carte)
                self._carte.append(U)
                self.metal_tot=self.metal_tot-Constante.cout_M_P
                self.energie_tot=self.energie_tot-Constante.cout_E_P
                self.coords = i, j     
            
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

    def placement_pos_unite(L,C):
            l = len(L)
            c = len(   C)
            L_pos_disp = []
            for i in range(l):
                for j in range(c):
                    Obj = Un_Tour_Du_Joueur._carte.ss_carte[i][j]
                    if Obj == ' ' :
                        L_pos_disp .append((i,j))                   
            if L_pos_disp==[]:
                print("Aucun emplacement dispo")
            return(L_pos_disp )
                
                
    def production_unite(self):
        """
        Permet au joueur défenseur s'il le souhaite et s'il en a le droit de construire un robot
        """       
        if self.role[0:2]=='DH':
            if (self.metal_tot>=Constante.cout_M_RC and self.energie_tot>=Constante.cout_E_RC):
                choix_DH=input("construire un robot ? (YES/NO)")
                if choix_DH=='YES':
                    L_pos_dispo = self.placement_pos_unite([i in range (Constante.xmax/2-1,Constante.xmax/2+2)],[j in range (Constante.ymax/2-1,Constante.ymax/2+2)])
                    L= list(input("abscisse ordonnée? (format x,y)")) 
                    print(' ',L_pos_dispo)
                    i,j = int(L[0]),int(L[2])
                    
                    while (i,j) not in L_pos_dispo :
                        if L_pos_dispo==[]:
                            break
                        L= list(input("Position non disponible, abscisse ordonnée? (format x,y)"))                                               
                        i,j = int(L[0]),int(L[2])
                        
                    U=Robot_combat(self._role,self._carte,i,j,self)
                    self._carte.append(U)
                    self.metal_tot=self.metal_tot-Constante.cout_M_P
                    self.energie_tot=self.energie_tot-Constante.cout_E_P
                                                                    
                elif choix_DH=='NO':
                    pass
        
        if self.role[0:2]=='AH':
            unite_disp_Tot+=self.unite_disp_/_tour
            
            while unite_disp_Tot>0:
                choix_AH=input("placer un Sorpion ? (YES/NO)")
                if choix_AH == 'YES':
                    L= list(input("abscisse ordonnée? (format x,y)"))                                               
                    i,j = int(L[0]),int(L[2])
            
                    A=[(Constante.xmax-Constante.L_Z_Constructible)/2+i in range ((Constante.xmax-constante.L_Z_Constructible)/2,(Constante.xmax-Constante.L_Z_Constructible)/2+Constante.L_Z_Constructible+1)]
                    B=[(Constante.ymax-Constante.H_Z_Constructible)/2+i in range ((Constante.ymax-Constante.H_Z_Constructible)/2,(Constante.ymax-Constante.H_Z_Constructible)/2+Constante.L_H_Constructible+1)]
                    L_pos_dispo_O = self.placement_pos_unite([0],B)
                    L_pos_dispo_E = self.placement_pos_unite([1],B)
                    L_pos_dispo_N = self.placement_pos_unite(A,[0])
                    L_pos_dispo_S = self.placement_pos_unite(A,[1])
            
                    L= list(input("abscisse ordonnée? (format x,y)")) 
                    print(' ',L_pos_dispo_N,' ',L_pos_dispo_S,' ',L_pos_dispo_O,' ',L_pos_dispo_E)

                    while ((i,j) not in L_pos_dispo_O or (i,j) not in L_pos_dispo_E or (i,j) not in L_pos_dispo_N or (i,j) not in L_pos_dispo_S):
                        if (L_pos_dispo_O == [] and L_pos_dispo_E ==[] and L_pos_dispo_N == [] and L_pos_dispo_S ==[]):
                            break
                        else:
                            L= list(input("abscisse ordonnée? (format x,y)"))                                               
                            i,j = int(L[0]),int(L[2])
                     
                    U = Scorpion (self._role,self._carte,x,y, self, self)
                    self._carte.append(U)
                    unite_disp_Tot-=1
                    self.unite_disp_/_tour-=1
            
                elif choix_AH == 'NO':
                    break

            
                    
            
            
        
    
        
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
        self.unite_disp_/_tour=0
        n = len(self.L_joueur)
        for k in range(n):
            print("\\\ Tour du joueur %r ///"%(self.L_joueur[k]._role))
            if self.L_joueur[k]._role[0] == 'D':
                Un_Tour_Du_Joueur.construction_bat(self)
            if self.L_joueur[k]._role[0][2] == 'AH':
                Un_Tour_Du_Joueur.production_unite(self)
                self.unite_disp_/_tour+=1
            L_unite = self.L_joueur[k]._liste_unite
            for c in L_unite:
                print("Tour de %r"%(c.T_car()))
                c.bouger()
        
        for obj in self._carte:
            obj.affichage()
            
    