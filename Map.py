
from numpy.random import randint
from numpy.random import choice
import time
from Un_Tour_Joueur import Un_Tour_Du_Joueur
from Ressource import metal
from Batiments import Foreuse,QG,Panneau_solaire
from unites_IA_facile import Scorpion0
from unites_IA_Moyenne import Scorpion1
from Constantes import Constante

class Map(list):
    """
    Classe gérant le déroulement du jeu. 
    """
    def __init__(self,L_joueur):
        self.__xmax = Constante.xmax
        self.__ymax = Constante.ymax  
        self.nbtour = Constante.nbt 
        self.L_joueur = L_joueur
        self.H=Constante.H_Z_Constructible
        self.L=Constante.L_Z_Constructible
        self.spawn_ress=Constante.spawn_ress

        self.Tr = Un_Tour_Du_Joueur(self)
        self.metal_tot=Constante.metal_tot
        self.energie_tot=Constante.energie_tot
        self.nb_unite_IA_In_Wave=0
        self.createInitObject()
        
        self.ss_carte = [[' ' for j in range(Constante.ymax)] for i in range(Constante.xmax)]
        U = QG(Constante.xmax/2,Constante.ymax/2,self,self)
        self.ss_carte[int(Constante.xmax/2)][int(Constante.ymax/2)] = U
        self.append(U)
#        self.L_joueur[0]._liste_bat.append(U)

        """Actuellement, carte contient l'ensemble des objets en jeu """


    def createInitObject(self):        
        self.Panneau_solaire=Panneau_solaire(0,0,self,self)
        self.Foreuse=Foreuse(0,0,self,self)

        
    
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
        return self.generation_Terrain()     # Pour l'affichage sur deux caractères
    
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
                    self.ss_carte[i][j]='/'                           
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
        
    def apparition_ressource(self):
        """
        permet de faire apparaitre une ressource de metal en dehors de la zone 
        constructible(#) et du murs de défense(/)
        """
        val=randint(0,1)
        if val==0:
            for z in range(int(self.spawn_ress/2)): #spawn les ressource en generation de map
                i=randint(0,self.__xmax)
                j=choice([randint(0,(self.__ymax-self.H)/2),randint((self.__ymax-self.H)/2+self.H+1,self.__ymax)])
                Obj = self.ss_carte[i][j]
                if Obj == ' ' :                    
                    U=metal(i,j,self,self)
                    self.append(U)
                    self.ss_carte[i][j]=U
                    
                else:
                    A=self[i][j]
                    if A.car != 'M':
                        U=metal(i,j,self,self)
                        self.append(U)
                        self.ss_carte[i][j]=U
                    else:
                        while ( A.car == 'M'):
                            i=randint(0,self.__xmax)
                            j=choice([randint(0,(self.__ymax-self.H)/2),randint((self.__ymax-self.H)/2+self.H+1,self.__ymax)])
                            U=metal(i,j,self,self)
                            self.append(U)
                            self.ss_carte[i][j]=U
        
        elif val==1:
            for z in range(int(self.spawn_ress/2)):                      
                i=choice([randint(0,(self.__xmax-self.L)/2),randint((self.__xmax-self.L)/2+self.L+1,self.__xmax)])
                j=randint(0,self.__ymax)
                Obj = self.ss_carte[i][j]
                if Obj == ' ' :                    
                    U=metal(i,j,self,self)
                    self.append(U)
                    self.ss_carte[i][j]=U
                    
                else:
                    A=self[i][j]
                    if A.car != 'M':
                        U=metal(i,j,self,self)
                        self.append(U)
                        self.ss_carte[i][j]=U
                    else:
                        while ( A.car == 'M'):
                            i=choice([randint(0,(self.__xmax-self.L)/2),randint((self.__xmax-self.L)/2+self.L+1,self.__xmax)])
                            j=randint(0,self.__ymax)
                            U=metal(i,j,self,self)
                            self.append(U)
                            self.ss_carte[i][j]=U
                
    
    def grossir_vague(self):
        """
        Permet d'augmenter le nombre d'unite de l'IA lors de la prochaine vague (toujours inférieur à la taille de la zone d'apparition)
        """
        self.nb_unite_IA_In_Wave+=1
        if self.nb_unite_IA_In_Wave > min(Constante.L_Z_Constructible,Constante.H_Z_Constructible):
            self.nb_unite_IA_In_Wave=min(Constante.L_Z_Constructible,Constante.H_Z_Constructible)
            
            
    def Zone_Nord(self):
            self.j_Z1=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
            self.i_Z1=0
            for obj in self:
                while self.i_Z1 ==obj.x and self.j_Z1==obj.y:
                    self.j_Z1=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                    self.i_Z1=0   
                    
    def Zone_Sud(self):
         self.j_Z2=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
         self.i_Z2=self.__xmax-1
         for obj in self:
             while self.i_Z2 ==obj.x and self.j_Z2==obj.y:
                 self.j_Z2=randint((self.__ymax-1-self.H-(self.__ymax - self.H)/2),((self.__ymax - self.H )/2+self.H))
                 self.i_Z2=self.__xmax-1
                 
    def Zone_Ouest(self):
        self.j_Z3=0
        self.i_Z3=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
        for obj in self:
            while (self.i_Z3 ==obj.x and self.j_Z3==obj.y):
                self.j_Z3=0
                self.i_Z3=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
    
    
    def Zone_Est(self):
        self.i_Z4=self.__ymax-1
        self.i_Z4=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))           
        for obj in self:
            while self.i_Z4 ==obj.x and self.i_Z4==obj.y:
                self.i_Z4=self.__ymax-1
                self.i_Z4=randint(self.__ymax-self.H-(self.__ymax-self.H)/2,(self.__xmax-(self.__xmax-self.L)/2))
                
   
    def apparition_vague_Niveau_0(self):
        """
        Permet de faire apparaitre une vague de scorpion1 sur une des 4 
        zones prévues à cette effet (!)
        """
        zone_app=randint(1,5)
        for k in range(self.nb_unite_IA_In_Wave):
                
            if zone_app==1:
                self.Zone_Nord()
                U=Scorpion0(self.i_Z1,self.j_Z1,self,self,self)
                self.append(U)
                self.L_Joueur.L_unite.append(U)
                self.ss_carte[self.i_Z1][self.j_Z1]=U
            if zone_app==2:
               self.Zone_Sud()
               U=Scorpion0(self.i_Z2,self.j_Z2,self,self,self)
               self.append(U)
               self.L_Joueur.L_unite.append(U)
               self.ss_carte[self.i_Z2][self.j_Z2]=U
            if zone_app==3:
                self.Zone_Ouest()
                U=Scorpion0(self.i_Z3,self.j_Z3,self,self,self)
                self.append(U)
                self.L_Joueur.L_unite.append(U)
                self.ss_carte[self.i_Z3][self.j_Z3]=U
            if zone_app==4:
                U=Scorpion0(self.i_Z14,self.j_Z4,self,self,self)
                self.append(U)
                self.L_Joueur.L_unite.append(U)
                self.ss_carte[self.i_Z4][self.j_Z4]=U
                
    def apparition_vague_Niveau_1(self):
        """
        Permet de faire apparaitre une vague de 60% de Scorpion1 et 30% de Scorpion2 sur une des 4 
        zones prévues à cette effet (!)
        """
        zone_app=randint(1,5)
        for k in range(self.nb_unite_IA_In_Wave):
                
            if zone_app==1:
                self.Zone_Nord()
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion0(self.i_Z1,self.j_Z1,self,self,self))
                else:
                    self.append(Scorpion1(self.i_Z1,self.j_Z1,self,self,self))
        
            if zone_app==2:
                self.Zone_Sud()
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion0(self.i_Z2,self.j_Z2,self,self,self))
                else:
                    self.append(Scorpion1(self.i_Z2,self.j_Z2,self,self,self))
            
            if zone_app==3:
                self.Zone_Ouest()
                if (p ==0 or p==1):
                    self.append(Scorpion0(self.i_Z3,self.j_Z3,self,self,self))
                else:
                    self.append(Scorpion1(self.i_Z3,self.j_Z3,self,self,self))
        
            if zone_app==4:
                self.Zone_Est()
                p=randint(0,3)
                if (p ==0 or p==1):
                    self.append(Scorpion0(self.i_Z4,self.j_Z4,self,self,self))
                else:
                    self.append(Scorpion1(self.i_Z4,self.j_Z4,self,self,self))
        
    def apparition_vague_Niveau_2(self):
        """
        Permet de faire apparaitre une vague de Scorpion2 sur une des 4 
        zones prévues à cette effet (!)
        """
        zone_app=randint(1,5)
        for k in range(self.nb_unite_IA_In_Wave):
                
            if zone_app==1:
                self.Zone1()
                self.append(Scorpion1(self.i_Z1,self.j_Z1,self,self,self))
        
            if zone_app==2:
                self.Zone2()
                self.append(Scorpion1(self.i_Z2,self.j_Z2,self,self,self))
            
            if zone_app==3:
                self.Zone_Ouest()
                self.append(Scorpion1(self.i_Z3,self.j_Z3,self,self,self))
        
            if zone_app==4:
                self.Zone_Est()
                self.append(Scorpion1(self.i_Z4,self.j_Z4,self,self,self))  
        
        
    def ressource_tot(self):
        """
        renvoie au joueur l'information su nombre de ressources qu'il possède
        """
        for obj in self:
            if obj.car == 'P':
                self.energie_tot+=self.Panneau_solaire.prod_E
            elif obj.car == 'F':
                self.metal_tot+=self.Foreuse.prod_M
        print('energie total = ' + str(self.energie_tot))
        print('metal total = ' + str(self.metal_tot))                
        
    
    def choix_niveau(self):
        """
        Permet au joueur de choisir le niveau de difficulté de l'IA
        """
        self.niveau=input("Quel niveau voulez vous jouer ? Niveau0 / Niveau1 / Niveau2")
        
        if self.niveau=='Niveau0' or self.niveau=='Niveau1' or self.niveau=='Niveau2':
            self.lvl=True
        else:
            self.lvl=False
            
            while self.lvl==False:
                self.niveau=input("Erreur. Quel niveau voulez vous jouer ? Niveau0 / Niveau1 / Niveau2")                    
                if self.niveau=='Niveau0' or self.niveau=='Niveau1' or self.niveau=='Niveau2':
                    self.lvl=True
                else:
                    self.lvl=False
    
    def niveau_choisi(self):
        """
        Execute les actions liées au choix du niveau par le joueur
        """
        if self.niveau == 'Niveau0':
            self.apparition_vague_Niveau_0()
            self.grossir_vague()
        if self.niveau == 'Niveau1':
            self.apparition_vague_Niveau_1()
            self.grossir_vague()
        if self.niveau == 'Niveau2':
            self.apparition_vague_Niveau_2()
            self.grossir_vague()
       
            
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
#            if t%5==0:
            self.apparition_ressource()
            if t%2==0:
                self.niveau_choisi()
                    
            self.ressource_tot()
            self.Tr.unTour()
            print(self)
            time.sleep(0.2)

                 
#if __name__ == "__main__":
#    carte = Map()
#    print(carte)
#    carte.simuler()
