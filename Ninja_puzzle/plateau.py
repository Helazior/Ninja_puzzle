#Plateau

from random import randint

from Choix_lvl import *

def change_lvl(plateau, increment):
    with open("lvl_actuel.txt","w") as fill:
        fill.write(str(plateau.lvl.num + increment))


def initFenetre(pygame, nbCasesX, nbCasesY, tailleFenetre, Matrice): #crée et affiche la fenêtre
    pygame.display.set_caption("Ninja Puzzle")

    fenetre = pygame.display.set_mode(tailleFenetre)

    #je charge et convertis les images dans des variables
    fond = pygame.image.load("fond.png").convert()
    fond2 = pygame.image.load("fond2.png").convert()
    mur = pygame.image.load("mur.png").convert()
    start = pygame.image.load("start.png").convert_alpha()
    end = pygame.image.load("end.png").convert_alpha()
    caisse = pygame.image.load("caisse.png").convert()
    caissePlace = pygame.image.load("caissePlace.png").convert()

    fondMenu = pygame.image.load("fondMenu.png").convert_alpha()

    fenetre.blit(pygame.transform.scale(fondMenu, (1280, 680)), (0, 0))

    for i in range(nbCasesX):
        for j in range(nbCasesY):
            pos = (30*i,30*j)
            if Matrice[j][i] == 1:
                fenetre.blit(mur, pos) #on place un mur quand c'est pas le fond
            else:
                if (i+j)%2:
                    fenetre.blit(fond, pos)
                else:
                    fenetre.blit(fond2, pos)
            if Matrice[j][i] == 5:
                fenetre.blit(caisse, pos)
            if Matrice[j][i] == 8:
                fenetre.blit(caissePlace, pos)

            if Matrice[j][i] == 2:
                fenetre.blit(start, pos) #on place le start
            elif Matrice[j][i] == 3:
                fenetre.blit(end, pos)  #on place l'arrivé des mobs


    pygame.display.flip() #rafraichit l'image !

    copy_fond = pygame.display.get_surface().copy() #Copie du fond pour faire bouger les trucs devant
    return fenetre, copy_fond, fond, fond2, caisse, caissePlace, start, end



def creationMatrice(tailleFenetre, nbCasesX, nbCasesY, fileName):
    Matrice = [1]*nbCasesY #on met des 1 sur toute la hauteur de la future matrice
    for i in range (nbCasesY):
        Matrice[i] = [1]*nbCasesX
        #on craie la matrice de la map avec des 1

    #On fait la map à partir du fichier texte
    with open(fileName,"r") as fichier:    #ouverture du fichier texte
        texte_grille = fichier.read()
        liste_grille = texte_grille.split("\n") #On fait une liste du fichier texte, qui est séparée à chaque saut à la ligne

        messageErreur = False
        for i in range(nbCasesX):
            for j in range(nbCasesY):
                try:
                    Matrice[j][i] = int(liste_grille[j][i])
                except:
                    if not(messageErreur):
                        if texte_grille == "":
                            print("Nouvelle map")
                        else:
                            print("ERROR: fichier txt de mauvaise dim")
                        messageErreur = 1
                
    return Matrice
    




class Plateau: #classe de la map attributs: Matrice, nbCasesX, nbCasesY, tailleFenetre, fenetre
    maxLvl = 10
    def __init__(self, pygame):
       
        with open("lvl_actuel.txt","r") as fichier:    #ouverture du fichier texte donnant le lvl
            try:
                lvl = int(fichier.read())
            except ValueError:
                print("error lvl")
                lvl = 0

        if lvl <= 0 or lvl > self.maxLvl: #si lvl est erroné
            print("lvl",lvl,"est erroné")
            lvl = 1
            with open("lvl_actuel.txt","w") as fichier:
                fichier.write(str(lvl))


        print("lvl ",lvl)
        
        self.lvl = Map_lvl(lvl) 
        fileName = self.lvl.maptxt

        nbCasesX = 40
        nbCasesY = 20
        tailleFenetre = (nbCasesX*30 + 80,nbCasesY*30 + 80)
        
        self.nbCasesX = nbCasesX
        self.nbCasesY = nbCasesY
        self.tailleFenetre = tailleFenetre
        Matrice = creationMatrice(tailleFenetre, nbCasesX, nbCasesY, fileName)
        self.Matrice = Matrice

        margeFenetreGauche = 15
        margeFenetreHaut = 15

        nbEnd = 0
        for i in range(nbCasesX):
                for j in range(nbCasesY):
                    if Matrice[j][i] == 3:
                        nbEnd += 1
        if nbEnd == 0:
            print("Erreur map: pas d'arrivée !")
        self.nbEnd = nbEnd

        
        self.fenetre, self.copy_fond, self.imageFond, self.imageFond2, self.imageCaisse, self.imageCaissePlace, self.imageStart, self.imageEnd = initFenetre(pygame, nbCasesX, nbCasesY,tailleFenetre, Matrice)
