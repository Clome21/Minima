# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 13:30:19 2018

@author: Erwann Landais
"""


import unittest
from numpy.random import randint
from numpy.random import choice
import time
from Un_Tour_Hn import Un_Tour_Joueur_Hn
from Un_Tour_IA import Un_Tour_Joueur_IA
from Ressource import metal
from Batiments import Foreuse,QG,Panneau_solaire
from unites_IA_facile import Scorpion0
from unites_IA_Moyenne import Scorpion1
from Constantes import Constante
import Save_Load as sl
import numpy as np
from Partie import Partie 
from Map import Map


class TestPartie(unittest.TestCase):
    """
    Classe gérant les tests effectués sur la classe Partie.
    """
    def testInit_Hn(self):
        """
        Test vérifiant :
            *Que tous les joueurs humains ont bien été crées. (3, d'après
            le paramètre d'entrée de Game)
            *Que le premier joueur humain est bien un défenseur, avec le bon
            nombre de métal et d'énergie initial.
            *Que l'objet Game est bien une instance de la classe Partie.
        
        """
        Game = Partie(0,3)
        self.assertEqual(Game.nb_hn,0)

        self.assertEqual(len(Game.L_joueur),3)
        self.assertEqual(Game.L_joueur[0]._role,'DH')
        self.assertEqual(Game.L_joueur[0].metal_tot,Constante.metal_tot)
        self.assertEqual(Game.L_joueur[0].energie_tot, Constante.energie_tot)
        self.assertIsInstance(Game,Partie)
    
    def testInit_IA(self):
        """
        Test vérifiant :
            *Que tous les joueurs humains ont bien été crées. (1, d'après
            le paramètre d'entrée de GamePC)
            *Qu'il y a bien trois joueurs de crées (donc deux joueurs IA et
            un joueur humain).
            *Que le premier joueur humain est bien un défenseur, avec le bon
            nombre de métal et d'énergie initial.
            *Que l'objet GamePC est bien une instance de la classe Partie.
        
        """
                
        self.assertEqual(GamePC.nb_hn,0)
        self.assertEqual(len(GamePC.L_joueur),3)
        self.assertEqual(GamePC.L_joueur[0].metal_tot,Constante.metal_tot)
        self.assertEqual(GamePC.L_joueur[0].energie_tot, Constante.energie_tot)
        self.assertIsInstance(GamePC,Partie)
        

class TestMap(unittest.TestCase):
    """
    Classe gérant les tests effectués sur la classe Map
    """
    def testInit(self):
        """
        Test vérifiant :
            *Que les dimensions de la carte correspondent à celles de la
            classe Constante.
            *Que la taille de la sous-carte correspond à celle de la carte.
            *Que le défenseur possède bien un QG.
            *Que la variable V_atta (indiquant la victoire ou non des attaquants)
            est bien initialisée à 0; indiquant donc que les attaquants n'ont pas
            encore gagnés.
            *Que l'objet Carte est une instance du type list.
        
        """
        x,y = Carte.dims
        self.assertEqual(x,Constante.xmax)
        self.assertEqual(y,Constante.ymax)
        self.assertEqual(np.shape(Carte.ss_carte),Carte.dims)
        self.assertEqual(len(Carte.L_joueur[0]._liste_bat[0]),1)
        self.assertEqual(Carte.V_atta,0)
        self.assertIsInstance(Carte,list)
        
    def testAppa_ressources(self):
        """
        Test vérifiant :
            *Que les dimensions de la carte correspondent à celles de la
            classe Constante.
            *Que la taille de la sous-carte correspond à celle de la carte.
            *Que le défenseur possède bien un QG.
            *Que la variable V_atta (indiquant la victoire ou non des attaquants)
            est bien initialisée à 0; indiquant donc que les attaquants n'ont pas
            encore gagnés.
            *Que l'objet Carte est une instance du type list.
        
        """
        x,y = Carte.dims
        L = Carte.L
        H = Carte.H
        x_inf_b = (x - L )//2 +1
        x_sup_b = (x + L)//2 
        y_inf_b =  (y - H)//2 +1
        y_sup_b = (y + H)//2 
        Terrain_const = Carte.ss_carte[x_inf_b:x_sup_b,y_inf_b:y_sup_b]
        for k in range(10):
            Carte.apparition_ressource()
        for obj in Carte:
            if obj.car == 'M ':
                self.assertNotIn(obj,Terrain_const)   
        
    def testRessources_tot(self):
        """
        Test vérifiant qu'après avoir ajouté trois foreuses et 3 panneaux solaires,
        et après 10 tours de jeu sans avoir effectué aucune dépense, que le défenseur 
        ait bien le bon total de ressources.
        """
        Def = Game.L_joueur[0]
        for i in range(3):
            X = i
            Y = i
            Def._liste_bat[1].append(Panneau_solaire(X,Y,Carte))
            Def._liste_bat[2].append(Foreuse(X+1,Y+1,Carte))
        for k in range(10):
            Carte.ressource_tot()

        M = 10*(Constante.prod_M_F*3 + Constante.prod_M_QG)+Constante.metal_tot
        E = 10*(Constante.prod_E_P*3 + Constante.prod_E_QG)+Constante.energie_tot
        self.assertEqual(Def.metal_tot,M)
        self.assertEqual(Def.energie_tot,E)

class TestRessources(unittest.TestCase):
    """
    Classe gérant les tests effectués sur la classe Ressource.
    """
    def testInit(self):
        """
        Test vérifiant :
            *Que la carte et la sous-carte possédées par la ressource correspondent 
            bien à celles de l'objet Carte.
            *Que la ressource se trouve bien dans la carte de jeu.
            *Que les variables de la ressource (position, valeur, identifiant) sont
            corrects.
        """
        U = metal(0,0,Carte,2)
        self.assertEqual(U._cart,Carte)
        self.assertIn(U,Carte)
        self.assertIn(U,Carte.ss_carte)
        self.assertEqual(U.coords,(0,0))
        self.assertEqual(U.valeur,2)
        self.assertEqual(U.T_car(),'N_O_M')
        
class TestSave(unittest.TestCase):
    """
    Classe gérant les tests effectués sur la classe Save.
    """
    def testSave(self):
        """
        Test vérifiant que, sur une partie avec 3 joueurs humains qui vient juste
        d'être initialisée : 
            *Que le nom de la sauvegarde (appelée blob.txt ici) est bien correct.
            *Que la sauvegarde possède le bon nombre de lignes (34 ici).
            *Que la dernière ligne de la sauvegarde est correcte.
        """
        Game = Partie(0,3)
        Carte = Game.carte
        Save = sl.Save("blob",Carte)
        self.assertEqual(Save.Nme,"blob.txt")
        with open(Save.Nme, 'r') as f:
                List_Save = [line.strip() for line in f]
        self.assertEqual(len(List_Save),56)
        self.assertEqual(List_Save[-1],"Fin sauvegarde")
      

class TestLoad(unittest.TestCase):
    """
    Classe gérant les tests effectués sur la classe Load.
    """
    def testInit_Carte(self):
        """
        Test vérifiant que la création d'une carte (de type chargée; c'est-à-dire 
        issue d'une sauvegarde) possède bien, initialement :
            *Les bonnes dimensions (issues de l'objet Constante).
            *La bonne liste joueur.
            *La bonne variable V_atta.
        """
        CarteL = Map([],1)     
        x,y = CarteL.dims
        self.assertEqual(x,Constante.xL)
        self.assertEqual(y,Constante.yL)
        self.assertEqual(CarteL.L_joueur,[])
        self.assertEqual(CarteL.V_atta,0)
        
    def testLoad(self): 
        """
        Test vérifiant que le chargement de la sauvegarde effectuée s'est bien déroulé.
        Pour cela, après avoir sauvegardé la partie, la méthode vérifie :
            *Que le tour actuel de la carte chargée correspond bien au tour actuel
            de la sauvegarde (c'est-à-dire au tour en cours lorsque la sauvegarde a
            eu lieu).
            *Que le QG de la sauvegarde est identique au QG chargé.
            *Que les joueurs et les unités de la partie chargée ont les bonnes variables,
            identiques à celles de la sauvegarde.
        """
        
        Save = sl.Save("blob",Carte)
        Load = sl.Load("blob.txt")
        self.assertEqual(Load.Lcarte.Ltr_actuel,Constante.Lnbta)

# Teste si le QG est identique

        self.assertEqual(Load.Lcarte.L_joueur[0]._liste_bat[0][0].T_car(),Game.L_joueur[0]._liste_bat[0][0].T_car())
        self.assertEqual(Load.Lcarte.L_joueur[0]._liste_bat[0][0].sante,Game.L_joueur[0]._liste_bat[0][0].sante)
        self.assertEqual(Load.Lcarte.L_joueur[0]._liste_bat[0][0].coords,Game.L_joueur[0]._liste_bat[0][0].coords)

# Teste si les joueurs sont identiques (mêmes variables, mêmes listes d'unité)

        for k in range(len(Game.L_joueur)):
            if Load.Lcarte.L_joueur[k]._liste_unite == []:
                self.assertEqual(Load.Lcarte.L_joueur[k]._liste_unite, Game.L_joueur[k]._liste_unite)
            else:
                for i in range(len(Load.Lcarte.L_joueur[k]._liste_unite)):
                    Unite = Load.Lcarte.L_joueur[k]._liste_unite[i]
                    self.assertEqual(Unite.sante,Game.L_joueur[k]._liste_unite[i].sante)
                    self.assertEqual(Unite.coords,Game.L_joueur[k]._liste_unite[i].coords)
                    self.assertEqual(Unite._role, Game.L_joueur[k]._liste_unite[i]._role)
                    
            self.assertEqual(Load.Lcarte.L_joueur[k].metal_tot,Game.L_joueur[k].metal_tot)
            self.assertEqual(Load.Lcarte.L_joueur[k].energie_tot, Game.L_joueur[k].energie_tot)
            self.assertEqual(Load.Lcarte.L_joueur[k].nbe_unite_restantes,Game.L_joueur[k].nbe_unite_restantes)
            self.assertEqual(Load.Lcarte.L_joueur[k].IdU, Game.L_joueur[k].IdU)
            self.assertEqual(Load.Lcarte.L_joueur[k]._role,Game.L_joueur[k]._role)

class TestUn_Tour(unittest.TestCase):
    """
    Classe gérant les tests effectués sur la classe Un_Tour_Hn et Un_Tour_IA.
    """
    def testInit_Tour(self):
        """
        Test vérifiant que l'objet TrHn Possède bien la même carte et la même liste
        des joueurs que l'objet Carte.
        Ce test vérifie aussi que la variable nombre d'unités disponible par tour 
        de cet objet est bien nulle à l'initialisation.
        """
        self.assertEqual(Carte.TrHn._carte,Carte)
        self.assertEqual(Carte.TrHn.L_joueur,Carte.L_joueur)
        self.assertEqual(Carte.TrHn.unite_disp_par_tour,0)
        
    def testPlacer_Foreuse(self):
        """
        Test vérifiant que :
            *Changer les valeurs des ressources possédées par le défenseur,
            dans la liste de joueurs de l'objet Carte, modifie bien les valeurs des
            ressources du défenseur dans la liste de joueurs de l'objet Un_Tour_Hn.
            *La méthode placer_une_foreuse de la classe Un_Tour_Hn fonctionne bien;
            c'est-à-dire que le défenseur obtient bien un objet Foreuse, et que cette
            foreuse est bien placée dans la zone de terrain constructible.
        """
        L = Carte.L
        H = Carte.H
        x,y = Carte.dims
        x_inf_b = (x - L )//2 +1
        x_sup_b = (x + L)//2 
        y_inf_b =  (y - H)//2 +1
        y_sup_b = (y + H)//2 
        Terrain_const = Carte.ss_carte[x_inf_b:x_sup_b,y_inf_b:y_sup_b]
        Carte.L_joueur[0].metal_tot = 30
        Carte.L_joueur[0].energie_tot = 30
        Tr_jeu_0_Hn = Carte.TrHn
        self.assertEqual(Tr_jeu_0_Hn.L_joueur[0].metal_tot, 30)
        self.assertEqual(Tr_jeu_0_Hn.L_joueur[0].energie_tot, 30)
        for k in range(3):
            Tr_jeu_0_Hn.placer_une_foreuse()
            self.assertIn(Game.L_joueur[0]._liste_bat[2][-1],Terrain_const)
        
    def testPlacer_Unite_IA_0(self):
        """
        Test vérifiant le bon fonctionnement de la méthode de productions d'unité
        attaquantes, pour le joueur IA.
        Elle vérifie :
            *Que l'attaquant 1 obtienne bien l'unité Scorpion crée.
            *Que ce Scorpion se trouve bien dans la zone d'apparition des unités
            attaquantes, sur la carte.
            *Que la variable unite_disp_par_tour ne change pas avec la production
            d'une unité d'attaque.
        """        
        x, y = GamePC.carte.dims
        TrPC = Tr_jeu_0_IAA
        TrPC.unite_disp_par_tour = 1
        
        L_Ht = TrPC.placement_pos(0,TrPC.Epp + 1,(y -TrPC.H )//2,(y + TrPC.H )//2,' ')
        self.assertEqual(len(L_Ht),(TrPC.Epp+1)*TrPC.H)
        
        L_Bas = TrPC.placement_pos(x-1-TrPC.Epp, x,(y - TrPC.H)//2,(y + TrPC.H )//2,' ')
        self.assertEqual(len(L_Bas),(TrPC.Epp+1)*TrPC.H)
        
        L_Gche = TrPC.placement_pos((x - TrPC.L)//2 , (x + TrPC.L )//2,0, TrPC.Epp+1,' ')
        self.assertEqual(len(L_Gche),(TrPC.Epp+1)*TrPC.L)
        
        L_Dte = TrPC.placement_pos((x - TrPC.L )//2,(x + TrPC.L )//2,y -1- TrPC.Epp, y,' ')
        self.assertEqual(len(L_Dte),(TrPC.Epp+1)*TrPC.L)
        
        L_pos = L_Ht + L_Bas + L_Gche + L_Dte 
        for k in range(3):    
            TrPC.production_unite_attaque_IA_0(1)
            self.assertIn(GamePC.L_joueur[1]._liste_unite[-1].coords,L_pos)
            self.assertEqual(TrPC.unite_disp_par_tour,1)


   
if __name__ == "__main__":
    Game = Partie(0,3)
    GamePC = Partie(2,)
    Carte = Game.carte
    Tr_jeu_0_Hn = Carte.TrHn
    Tr_jeu_0_IA = Carte.TrIA    
    Tr_jeu_0_IAA = GamePC.carte.TrIA
    unittest.main()
    
