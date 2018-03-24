import numpy as np

from numpy.random import randint
from numpy.random import choice
import time
from Ressource import metal
from Batiments import Foreuse,QG,Panneau_solaire
from IA_facile import Scorpion_Facile,Scorpion_Moins_Facile


class Map(list):
    """
    Classe gérant le déroulement du jeu. 
    """
    def __init__(self,xmax,ymax,nbt,L=19,H=15,spawn_ress=2,metal_tot=5,energie_tot=5):
        self.__xmax = xmax
        self.__ymax = ymax  
        self.nbtour =  nbt  
        self.H=H
        self.L=L
        self.spawn_ress=spawn_ress
        self.metal_tot=metal_tot
        self.energie_tot=energie_tot
        self.nb_unite_IA_In_Wave=0
        self.createInitObject()
        self.ss_carte = [[' ' for j in range(ymax)] for i in range(xmax)]
        U = QG(xmax/2,ymax/2,self)
        self.ss_carte[int(xmax/2)][int(ymax/2)] = U

        self.append(U)

        """Actuellement, carte contient l'ensemble des objets en jeu """
        
        
        

    def createInitObject(self):        
        self.Panneau_solaire=Panneau_solaire(0,0,self)
        self.Foreuse=Foreuse(0,0,self)

        
    
    @property
    def dims(self):
        """
        Renvoies les dimensions du plateau de jeu
        """
        return (self.__xmax, self.__ymax)
    
    def __str__(self):
        """Affiche le plateau de jeu en mode texte 
        
        Paramètres
        ----------
        Aucun
        
        Renvoie
        -------
        s: string
            La chaîne de caractères qui sera affichée via ''print''
            
       
        """

        return self.generation_Terrain()

        # Pour l'affichage sur deux caractères
    
    def generation_Terrain(self):
        """
        Conversion en chaîne avec deux caractères par case.
        """

        pos={}
        s=""
         
        for obj in self:
            pos[obj.coords]=obj.car()
        for i in range(self.__xmax):
            for j in range(self.__ymax):  
                if (i>(self.__xmax-(self.L))/2 and i<(self.__xmax+(self.L-1))/2) and (j>(self.__ymax-(self.H))/2 and j<(self.__ymax+(self.H-1))/2):
                    s += "#" #zone constructible
                elif (((i> (self.__xmax - self.L )/2-1 and i< (self.__xmax - self.L )/2+self.L/2-1)) or((i> (self.__xmax - self.L )/2+self.L/2) and i< (self.__xmax - self.L )/2+self.L)) and (((j> (self.__ymax - self.H )/2-1) and (j< (self.__ymax - self.H )/2+self.H/2-1)) or((j> (self.__ymax - self.H )/2+self.H/2) and j< (self.__ymax - self.H )/2+self.H)):
                    s += "/" #Mur de protection                            
                elif ((i==0 ) and (j>(self.__ymax-1-self.H-(self.__ymax - self.H)/2) and (j< (self.__ymax - self.H )/2+self.H))) or ((i==self.__xmax-1 ) and (j>(self.__ymax-1-self.H-(self.__ymax - self.H)/2) and (j< (self.__ymax - self.H )/2+self.H))) or ((j==0) and ((i>self.__xmax-1-self.L-(self.__xmax-self.L)/2) and (i<self.__xmax-(self.__xmax-self.L)/2))) or ((j==self.__ymax-1) and ((i>self.__xmax-1-self.L-(self.__xmax-self.L)/2) and (i<self.__xmax-(self.__xmax-self.L)/2))) :
                    s +="!" #zone d'apparition des unites qui attaques   
                else:
                    s += "."
                if (i, j) in pos:
                    s += pos[(i,j)]
                else:
                    s += " "
            s += "\n"
        return s
    

    
            
    def placer_une_foreuse(self)   :
        """
        Permet au joueur s'il le souhaite et s'il en a le droit de construire le batiment Foreuse
        Mets également à jour la quantité de ressource à sa disposition
        """
        while (self.metal_tot>=self.Foreuse.cout_M and self.energie_tot>=self.Foreuse.cout_E):
            choix2=input("placer Foreuse ? (YES/NO)")
            if choix2 == 'YES':
                i=float(input("en quelle abscisse ?"))
                j=float(input("en quelle ordonnée ?"))
                for batiment in self:
                    while (i==batiment.x and j==batiment.y) or not ((i>(self.__xmax-(self.L))/2 and i<(self.__xmax+(self.L-1))/2) and (j>(self.__ymax-(self.H))/2 and j<(self.__ymax+(self.H-1))/2)):
                        i=float(input("Emplacement non valide : quelle coordonnée en x ?"))
                        j=float(input("Emplacement non valide : quelle coordonnée en y ?"))
                self.append(Foreuse(i,j,self))                
                self.metal_tot=self.metal_tot-self.Foreuse.cout_M
                self.energie_tot=self.energie_tot-self.Foreuse.cout_E
                        
            elif choix2=='NO':
                break

    def placer_un_Panneau_solaire(self):
        """
        Permet au joueur s'il le souhaite et s'il en a le droit de construire le batiment Panneau solaire
        Mets également à jour la quantité de ressource à sa disposition
        """
        while (self.metal_tot>=self.Panneau_solaire.cout_M and self.energie_tot>=self.Panneau_solaire.cout_E):
            choix2=input("placer Panneau solaire ? (YES/NO)")
            if choix2 == 'YES':
                i=float(input("en quelle abscisse ?"))
                j=float(input("en quelle ordonnée ?"))
                for batiment in self:
                    while (i==batiment.x and j==batiment.y) or not ((i>(self.__xmax-(self.L))/2 and i<(self.__xmax+(self.L-1))/2) and (j>(self.__ymax-(self.H))/2 and j<(self.__ymax+(self.H-1))/2)):
                        i=float(input("Emplacement occupé : quelle coordonnée en x ?"))
                        j=float(input("Emplacement occupé : quelle coordonnée en y ?"))
                self.append(Panneau_solaire(i,j,self))
                self.metal_tot=self.metal_tot-self.Panneau_solaire.cout_M
                self.energie_tot=self.energie_tot-self.Panneau_solaire.cout_E
                        
            elif choix2=='NO':
                break
    
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
        
    def spawn_ressource(self):
        """
        permet de faire apparaitre une ressource de metal en dehors de la zone 
        constructible(#) et du murs de défense(/)
        """
        val=randint(0,1)
        if val==0:
            for z in range(int(self.spawn_ress/2)): #spawn les ressource en generation de map
                i=randint(0,self.__xmax)
                j=choice([randint(0,(self.__ymax-self.H)/2),randint((self.__ymax-self.H)/2+self.H+1,self.__ymax)])
                for obj in self:
                    if obj.name != "Scorpion":
                        while i==obj.x and j==obj.y:
                            i=randint(0,self.__xmax)
                            j=choice([randint(0,(self.__ymax-self.H)/2),randint((self.__ymax-self.H)/2+self.H+1,self.__ymax)])                        
                self.append(metal(i,j,self,self))
        elif val==1:
            for z in range(int(self.spawn_ress/2)):                      
                i=choice([randint(0,(self.__xmax-self.L)/2),randint((self.__xmax-self.L)/2+self.L+1,self.__xmax)])
                j=randint(0,self.__ymax)
                for obj in self:
                    if obj.name != "Scorpion":
                        while i==obj.x and j==obj.y:
                            i=choice([randint(0,(self.__xmax-self.L)/2),randint((self.__xmax-self.L)/2+self.L+1,self.__xmax)])
                            j=randint(0,self.__ymax)
                self.append(metal(i,j,self,self))
                
    def grossir_wave(self):
        """
        Permet d'augmenter le nombre d'unite de l'IA lors de la prochaine vague
        """
        self.nb_unite_IA_In_Wave+=1
    
    def Zone1(self):
            self.j_Z1=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
            self.i_Z1=0
            for obj in self:
                while self.i_Z1 ==obj.x and self.j_Z1==obj.y:
                    self.j_Z1=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                    self.i_Z1=0            
    
    def spawn_wave_Niveau_0(self):
        """
        Permet de faire apparaitre une vague d'unite de l'IA niveau facile sur une des 4 
        zones prévues à cette effet (!)
        """
        zone_app=randint(1,5)
        for k in range(self.nb_unite_IA_In_Wave):
                
            if zone_app==1:
                self.Zone1()
                self.append(Scorpion_Facile(self.i_Z1,self.i_Z1,self))
        
            if zone_app==2:
                j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                i=self.__xmax-1
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                        i=self.__xmax-1
                self.append(Scorpion_Facile(i,j,self))
            
            if zone_app==3:
                j=0
                i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
                for obj in self:
                    while (i ==obj.x and j==obj.y):
                        j=0
                        i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                self.append(Scorpion_Facile(i,j,self))
        
            if zone_app==4:
                j=self.__ymax-1
                i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=self.__ymax-1
                        i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                self.append(Scorpion_Facile(i,j,self))
             
    def spawn_wave_Niveau_1(self):
        """
        Permet de faire apparaitre une vague d'unite de l'IA niveau facile sur une des 4 
        zones prévues à cette effet (!)
        """
        zone_app=randint(1,5)
        for k in range(self.nb_unite_IA_In_Wave):
                
            if zone_app==1:
                j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                i=0
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                        i=0
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion_Facile(i,j,self))
                else:
                    self.append(Scorpion_Moins_Facile(i,j,self))
        
            if zone_app==2:
                j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                i=self.__xmax-1
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                        i=self.__xmax-1
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion_Facile(i,j,self))
                else:
                    self.append(Scorpion_Moins_Facile(i,j,self))
            
            if zone_app==3:
                j=0
                i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
                for obj in self:
                    while (i ==obj.x and j==obj.y):
                        j=0
                        i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion_Facile(i,j,self))
                else:
                    self.append(Scorpion_Moins_Facile(i,j,self))
        
            if zone_app==4:
                j=self.__ymax-1
                i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=self.__ymax-1
                        i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion_Facile(i,j,self))
                else:
                    self.append(Scorpion_Moins_Facile(i,j,self))
        
    def spawn_wave_Niveau_2(self):
        """
        Permet de faire apparaitre une vague d'unite de l'IA niveau facile sur une des 4 
        zones prévues à cette effet (!)
        """
        zone_app=randint(1,5)
        for k in range(self.nb_unite_IA_In_Wave):
                
            if zone_app==1:
                j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                i=0
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                        i=0
                self.append(Scorpion_Moins_Facile(i,j,self))
        
            if zone_app==2:
                j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                i=self.__xmax-1
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                        i=self.__xmax-1
                self.append(Scorpion_Moins_Facile(i,j,self))
            
            if zone_app==3:
                j=0
                i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
                for obj in self:
                    while (i ==obj.x and j==obj.y):
                        j=0
                        i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                self.append(Scorpion_Moins_Facile(i,j,self))
        
            if zone_app==4:
                j=self.__ymax-1
                i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
                for obj in self:
                    while i ==obj.x and j==obj.y:
                        j=self.__ymax-1
                        i=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                self.append(Scorpion_Moins_Facile(i,j,self))  
        
        
    def ressource_tot(self):
        """
        renvoie au joueur l'information su nombre de ressources qu'il possède
        """
        for obj in self:
            if obj.name == "Panneau_solaire":
                self.energie_tot+=self.Panneau_solaire.prod_E
            elif obj.name == "Foreuse":
                self.metal_tot+=self.Foreuse.prod_M
        print('energie total = ' + str(self.energie_tot))
        print('metal total = ' + str(self.metal_tot))                
        
    def choix_niveau(self):
        """
        Permet au joueur de choisir le niveau de difficulté de l'IA
        """
        self.niveau=input("Quelle niveau voulez vous jouer ? Niveau0 / Niveau1 / Niveau2")
        
        if self.niveau=='Niveau0' or self.niveau=='Niveau1' or self.niveau=='Niveau2':
            self.lvl=True
        else:
            self.lvl=False
            
            while self.lvl==False:
                self.niveau=input("Erreur. Quelle niveau voulez vous jouer ? Niveau0 / Niveau1 / Niveau2")                    
                if self.niveau=='Niveau0' or self.niveau=='Niveau1' or self.niveau=='Niveau2':
                    self.lvl=True
                else:
                    self.lvl=False
    
    def niveau_choisi(self):
        """
        Execute les actions liées au choix du niveau par le joueur
        """
        if self.niveau == 'Niveau0':
            self.spawn_wave_Niveau_0()
            self.grossir_wave()
        if self.niveau == 'Niveau1':
            self.spawn_wave_Niveau_1()
            self.grossir_wave()
        if self.niveau == 'Niveau2':
            self.spawn_wave_Niveau_2()
            self.grossir_wave()

        
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
        self.construction_bat()
        for unite in self:
            if unite.name=="Scorpion":
                unite.bouger()
        for obj in self:
            obj.affichage()
        
            
    def simuler (self):
        """
        Contrôle l'évolution du jeu, affiche le résultat de chaque tour dans
        un terminal.
        
        Paramètres
        ----------
        Aucun

        Renvoie
        -------
        Rien  
        """
        self.choix_niveau()
            
        for t in range(self.nbtour):
            print("### Tour %i ###"%(t))
            if t%5==0:
                self.spawn_ressource()
            if t%2==0:
                self.niveau_choisi()
                    
            self.ressource_tot()
            self.unTour()
            print(self)
            time.sleep(0.2)

                 
if __name__ == "__main__":
    carte = Map(40,30,10)
    print(carte)
    carte.simuler()
