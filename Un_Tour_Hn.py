from Batiments import Foreuse,Panneau_solaire
from Constantes import Constante
from Unites_Hn_Defenseur import Robot_combat, Robot_Ouvrier
from Unites_Hn_Attaquant import Scorpion
from numpy.random import randint

import numpy as np


class Un_Tour_Joueur_Hn():


    
    def __init__(self,carte):
        self._carte = carte
        self.L_joueur = self._carte.L_joueur
        self.unite_disp_par_tour = 0
        
        self.__xmax = Constante.xmax
        self.__ymax = Constante.ymax  
        self.Epp = Constante.Ep_app

        self.H=Constante.H_Z_Constructible
        self.L=Constante.L_Z_Constructible

        
         
    def placer_une_foreuse(self)   :
        """
        Permet au joueur s'il le souhaite et s'il en a le droit de construire le batiment Foreuse
        Mets également à jour la quantité de ressource à sa disposition
        """
        if (self.L_joueur[0].metal_tot>=Constante.cout_M_F and self.L_joueur[0].energie_tot>=Constante.cout_E_F):
            choix2=input("placer Foreuse ? (YES/NO)")
            if choix2 == 'YES':
                x_inf_b = (self.__xmax - self.L )//2 +1
                x_sup_b = (self.__xmax + self.L )//2 -1
                y_inf_b =  (self.__ymax - self.H )//2 +1
                y_sup_b = (self.__ymax + self.H)//2 -1

                L_pos = self.placement_pos_bat(x_inf_b,x_sup_b,y_inf_b,y_sup_b,' ')
                if len(L_pos) == 0:
                    print('Aucune position disponible, étape suivante. \n')
                else:    
                    print('Positions possibles :', L_pos)
                    L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                    k = L.find(',')
                    while k == -1:
                        print("Erreur de synthaxe. Recommencez svp")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                    X = int(L[0:k])
                    Y = int(L[k+1:])
                    while (X,Y) not in L_pos:
                        print("Position hors du rayon d'action de l'unité. \n")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                        X,Y = int(L[0:k]) , int(L[k+1:])
                    U = Foreuse(X,Y,self._carte)
                    self.L_joueur[0]._liste_bat[2].append(U)
                    self.L_joueur[0].metal_tot=self.L_joueur[0].metal_tot-Constante.cout_M_F
                    self.L_joueur[0].energie_tot=self.L_joueur[0].energie_tot-Constante.cout_E_F
                    print("Energie restante :", self.L_joueur[0].energie_tot, "\n")
                    print("Métal restant :", self.L_joueur[0].energie_tot, "\n")
                    
                    print(self._carte.ss_carte[X][Y])


    def placer_un_Panneau_solaire(self):
        """
        Permet au joueur s'il le souhaite et s'il en a le droit de construire le batiment Panneau solaire
        Mets également à jour la quantité de ressource à sa disposition
        """

        if (self.L_joueur[0].metal_tot>=Constante.cout_M_P and self.L_joueur[0].energie_tot>=Constante.cout_E_P):
            choix2=input("placer Panneau solaire ? (YES/NO)")
            if choix2 == 'YES':
                x_inf_b = (self.__xmax - self.L )//2 +1
                x_sup_b = (self.__xmax + self.L )//2 -1
                y_inf_b =  (self.__ymax - self.H )//2 +1
                y_sup_b = (self.__ymax + self.H)//2 -1
                #Noter que x_inf et x_sup doivent être +1 par rapport à leur valeur réelle (pour bien tout sélectionner dans la matrice)

                L_pos = self.placement_pos_bat(x_inf_b,x_sup_b,y_inf_b,y_sup_b,' ')
                if len(L_pos) == 0:
                    print('Aucune position disponible, étape suivante. \n')
                else:
                    print('Positions possibles :', L_pos)
                    L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                    k = L.find(',')
                    while k == -1:
                        print("Erreur de synthaxe. Recommencez svp")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')                        
                    X = int(L[0:k])
                    Y = int(L[k+1:])
                    while (X,Y) not in L_pos:
                        print("Position hors du rayon d'action de l'unité. \n")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                        X,Y = int(L[0:k]) , int(L[k+1:])
                        
                    U = Panneau_solaire(X,Y,self._carte)
                    self.L_joueur[0]._liste_bat[1].append(U)
                        
                    self.L_joueur[0].metal_tot=self.L_joueur[0].metal_tot-Constante.cout_M_P
                    self.L_joueur[0].energie_tot=self.L_joueur[0].energie_tot-Constante.cout_E_P
                    print("Energie restante :", self.L_joueur[0].energie_tot, "\n")
                    print("Métal restant :", self.L_joueur[0].energie_tot, "\n")

        
    def placement_pos(self,x_inf,x_sup,y_inf,y_sup,typ):
        A = self._carte.ss_carte[x_inf : x_sup , y_inf : y_sup]
        L_pos = []

        Coords = np.where( A == typ)
        for k in range(len(Coords[0])):
            i,j = Coords[0][k]+ x_inf , Coords[1][k] + y_inf
            L_pos.append((i,j))
        return(L_pos)
        
    def placement_pos_bat(self,x_inf_b,x_sup_b,y_inf_b,y_sup_b,typ):
        
        L_pos = self.placement_pos(x_inf_b,x_sup_b,y_inf_b,y_sup_b,typ)
        print(L_pos)
        x_inf = (self.__xmax )//2 -1
        x_sup = (self.__xmax)//2 +2
        y_inf =  (self.__ymax)//2 - 1
        y_sup = (self.__ymax)//2 +2
        
        L_pos_imp1 = [(i,j) for i in range(x_inf,x_sup) for j in range( (self.__ymax -self.H)//2 +1, (self.__ymax + self.H)//2)]
        L_pos_imp2 = [(i,j) for i in range((self.__xmax - self.L)//2+1 , (self.__xmax + self.L)//2) for j in range(y_inf,y_sup)]
        E_pos_imp = set(L_pos_imp1 + L_pos_imp2)
        """Définit les coordonnées où placer un bâtiment est impossible"""
        E_pos = set(L_pos)
        L_pos_tot =list( E_pos - (E_pos&E_pos_imp))
        return(L_pos_tot)

    
    def construction_bat(self):
        """
        Permet au joueur s'il le souhaite de placer un batiment
        """
        choix=input("placer un batiment ? (YES/NO)")
        if choix=='YES':
            self.placer_une_foreuse()
            self.placer_un_Panneau_solaire()
        elif choix=='NO':
            pass
        
    def production_unite(self,role,k):
        if role[0] == 'D':
            self.production_unite_defense()
        elif role[0] == 'A':
            self.production_unite_attaque(role,k)

    def production_unite_defense(self):
        if (self.L_joueur[0].metal_tot>=Constante.cout_M_RO and self.L_joueur[0].energie_tot>=Constante.cout_E_RO):
            choix_DH = input("Construire un robot? (YES/NO)")
            if choix_DH == 'YES':
                self.production_unite_defense_combat()
                self.production_unite_defense_production()

    
    def production_unite_defense_combat(self):
        if (self.L_joueur[0].metal_tot>=Constante.cout_M_RC and self.L_joueur[0].energie_tot>=Constante.cout_E_RC):
            choix_DH=input("construire un robot de combat?  (YES/NO)")
            if choix_DH=='YES':
                
                x_inf = (self.__xmax )//2 -1
                x_sup = (self.__xmax)//2 +2
                y_inf =  (self.__ymax)//2 - 1
                y_sup = (self.__ymax)//2 +2
                #A VERIF

                L_pos = self.placement_pos(x_inf,x_sup,y_inf,y_sup,' ')
                if len(L_pos) == 0:
                    print('Aucune position disponible, étape suivante. \n')
                else:
                    print('Positions possibles :', L_pos)
                    L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                    k = L.find(',')
                    while k == -1:
                        print("Erreur de synthaxe. Recommencez svp")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                    X = int(L[0:k])
                    Y = int(L[k+1:])
                    while (X,Y) not in L_pos:
                        print("Position hors du rayon d'action de l'unité. \n")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                        X,Y = int(L[0:k]) , int(L[k+1:])
                U=Robot_combat(self.L_joueur[0]._role,self._carte,X,Y)
                self.L_joueur[0]._liste_unite.append(U)
                self.L_joueur[0].metal_tot=self.L_joueur[0].metal_tot-Constante.cout_M_P
                self.L_joueur[0].energie_tot=self.L_joueur[0].energie_tot-Constante.cout_E_P
                print("Energie restante :", self.L_joueur[0].energie_tot, "\n")
                print("Métal restant :", self.L_joueur[0].energie_tot, "\n")
                                                                    
            elif choix_DH=='NO':
                pass
            
    def production_unite_defense_production(self):
        if (self.L_joueur[0].metal_tot>=Constante.cout_M_RO and self.L_joueur[0].energie_tot>=Constante.cout_E_RO):
            choix_DH=input("Construire un robot ouvrier?  (YES/NO)")
            if choix_DH=='YES':
                
                x_inf = (self.__xmax )//2 -1
                x_sup = (self.__xmax)//2 +2
                y_inf =  (self.__ymax)//2 - 1
                y_sup = (self.__ymax)//2 +2
                #A VERIF

                L_pos = self.placement_pos(x_inf,x_sup,y_inf,y_sup,' ')
                if len(L_pos) == 0:
                    print('Aucune position disponible, étape suivante. \n')
                else:
                    print('Positions possibles :', L_pos)
                    L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                    k = L.find(',')
                    while k == -1:
                        print("Erreur de synthaxe. Recommencez svp")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                    X = int(L[0:k])
                    Y = int(L[k+1:])
                    while (X,Y) not in L_pos:
                        print("Position hors du rayon d'action de l'unité. \n")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        k = L.find(',')
                        X,Y = int(L[0:k]) , int(L[k+1:])
                U=Robot_Ouvrier(self.L_joueur[0]._role,self._carte,X,Y)
                self.L_joueur[0]._liste_unite.append(U)
                self.L_joueur[0].metal_tot=self.L_joueur[0].metal_tot-Constante.cout_M_P
                self.L_joueur[0].energie_tot=self.L_joueur[0].energie_tot-Constante.cout_E_P
                print("Energie restante :", self.L_joueur[0].energie_tot, "\n")
                print("Métal restant :", self.L_joueur[0].energie_tot, "\n")
                                                                    
            elif choix_DH=='NO':
                pass
        
    def production_unite_attaque(self,role,k):
        if role[0:2] == 'AI':
            if role[3] == '0':
                self.production_unite_attaque_IA_0(k)
        elif role[0:2] == 'AH' :
            self.production_unite_attaque_Hn(k)
    
    def production_unite_attaque_Hn(self,k):
        
        Jr = self.L_joueur[k]
        unite_disp = self.unite_disp_par_tour + Jr.nbe_unite_restantes
        
        if unite_disp < 1:
            print("Aucune unité à placer pour ce tour. \n")
        
        else:
        
            L_Ht = self.placement_pos(0,self.Epp + 1,(self.__ymax -self.H)//2,(self.__ymax + self.H )//2,' ')
            
            L_Bas = self.placement_pos(self.__xmax-1-self.Epp,self.__xmax,(self.__ymax -self.H)//2,(self.__ymax + self.H )//2,' ')
        
            L_Gche = self.placement_pos((self.__xmax - self.L )//2 , (self.__xmax + self.L )//2,0,self.Epp+1,' ')
        
            L_Dte = self.placement_pos((self.__xmax - self.L )//2, (self.__xmax + self.L )//2,self.__ymax -1-self.Epp,self.__ymax,' ')
        
            #Sélectionne les 4 zones d'apparitions
        
            L_pos = L_Ht + L_Bas + L_Gche + L_Dte 
        
            #Sélectionne les emplacements disponibles
            if len(L_pos) == 0 :
                print("Aucune zone d'apparition d'unité disponible, étape suivante. \n")
        
            else : 
                print("Nombre de scorpions disponibles : ", int(unite_disp) )
                
                choix_AH=input("placer un Scorpion ? (YES/NO)")
            
                while len(L_pos) != 0 and unite_disp >=1 and choix_AH == 'YES':
                    print('Positions possibles :', L_pos)
                    L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                    c = L.find(',')
                    while c == -1:
                        print("Erreur de synthaxe. Recommencez svp")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        c = L.find(',')                        
                    X = int(L[0:c])
                    Y = int(L[c+1:])
                    while (X,Y) not in L_pos:
                        print("Position hors de la zone d'apparition. \n")
                        L = input('Envoyez la nouvelle position en x et en y (format x,y). \n')
                        c = L.find(',')
                        X,Y = int(L[0:c]) , int(L[c+1:])

                    L_pos.remove((X,Y))
                    self.U = Scorpion(Jr._role,self._carte,X,Y,k)
                    Jr._liste_unite.append(self.U)
                    unite_disp-=1
                
                    if unite_disp <1:
                        print("Plus d'unité disponible, étape suivante \n")
                        break
                
                    if len(L_pos) == 0:
                        print("Aucune zone d'apparition d'unité disponible, étape suivante. \n")
                        break
                        
                    else:
                        print("Nombre de scorpions disponibles : ", int(unite_disp))
                        choix_AH=input("placer un autre Scorpion ? (YES/NO)")
            
                if choix_AH == 'NO' or len(L_pos) == 0:
                    Jr.nbe_unite_restantes = unite_disp

 
                
        
    def unTourHn(self):

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
            if self._carte.V_atta == 1:
                break
            role = self.L_joueur[k]._role
            if role[1] == 'H':
                print("\\\ Tour du joueur %r ///"%(role))
                if role[0] == 'D':
                    self.construction_bat()
                self.production_unite(role,k)
                L_unite = self.L_joueur[k]._liste_unite
                for c in L_unite:
                    if self._carte.V_atta == 1:
                        break
    
                    print("Tour de %r \n"%(c.T_car()))
                    print("Position actuelle : (%i,%i) \n"%(c.x,c.y))
                    if c._role[1] == 'H':
                        Chx = input("Voulez-vous la déplacer? (Y/N) \n")
                        if Chx == "Y":
                            c.bouger()
                    else : 
                        c.bouger()
                    c.action()
    
        self.unite_disp_par_tour += Constante.nbe_unite_ajoute
        if self.unite_disp_par_tour > min(self.L,self.H):
            self.unite_disp_par_tour = min(self.L,self.H)
            
            
    