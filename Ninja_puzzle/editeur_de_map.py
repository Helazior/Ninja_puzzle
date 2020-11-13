#Editeur

"""
_______________help________________

- 0,1,2,3,5 pour choisir le bloc correspondant (0 par défaut)
- clique pour poser un bloc
- rester appuyer et bouger la souris pour poser plein de blocs
- 's' pour enregistrer (en fait pour l'instant ça enregistre automatiquement quand on quitte)
- 'u' pour revenir à la dernière sauvegarde, utile pour ne pas enregistrer ('z' était trop proche de 's')
- entrer pour tester le lvl

- fileName est le nom du fichier texte, il doit exister. Maintenant contenu dans le fichier lvl_actuel.txt

"""

import pygame
from pygame.locals import *
import sys, os

from plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

pygame.init()

pathname = os.path.dirname(sys.argv[0])     #mur du programme

os.chdir (os.path.abspath(pathname))        #c'est pour que le repertoire courant soit au niveau du programme
os.chdir ("ressources")                     #c'est pour que le repertoire courant soit dans "ressources"

clock = pygame.time.Clock() 				#initialise une horloge pour gerer le temps


#setup pour le plateau
plateau = Plateau(pygame)
fileName = plateau.lvl.maptxt 

print("map: ", fileName)

#je charge et convertis les images dans des variables
fond = pygame.image.load("fond.png").convert()
mur = pygame.image.load("mur.png").convert()
start = pygame.image.load("start.png").convert_alpha()
end = pygame.image.load("end.png").convert_alpha()
caisse = pygame.image.load("caisse.png").convert_alpha()
caissePlace = pygame.image.load("caissePlace.png").convert_alpha()


          
#______________save_______________
def save(matrice, fileName):
    try:
        with open(fileName,"w") as fichier:     #ouverture du fichier texte en mode écriture
            for ligne in matrice:
                for chiffre in ligne:
                    chiffre = str(chiffre)
                    fichier.write(chiffre)
                fichier.write("\n")


        print(f"{fileName} a bien été enregistrée !")
    except:
        print("ERREUR d'enregistrement...")

def is_in_matrice(matrice, n): #test si n est dans la matrice
    for ligne in matrice:
        if n in ligne:
            return True
    return False

def put_a_block(plateau, event, numCase, dictImage):
    x = event.pos[0] // 30
    y = event.pos[1] // 30
    try:
        numCaseActuel = plateau.Matrice[y][x]
        if numCase != numCaseActuel:
            plateau.Matrice[y][x] =  numCase
            plateau.fenetre.blit(dictImage[numCase], (30*x,30*y))
            pygame.display.flip() #rafraichit l'image
                                 
    except:
        pass



dictKey = {256 : 0, 257 : 1, 258 : 2, 259 : 3, 224 : 0, 38 : 1, 233 : 2, 34 : 3, 40 : 5, 95 : 8}
dictImage = {0: fond, 1: mur, 2: start, 3: end, 5: caisse, 8: caissePlace}
numCase = 0
clique = False
continuer = True


#_________________________________________________boucle principale:_________________________________________________

while continuer: #tout ce passe là dedans
    
    for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
        pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non
            
        if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte et enregistre
            save(plateau.Matrice, fileName)
            continuer = False


        elif event.type == pygame.MOUSEBUTTONDOWN:
            clique = True
            put_a_block(plateau, event, numCase, dictImage)
        elif event.type == pygame.MOUSEMOTION and clique:
            put_a_block(plateau, event, numCase, dictImage)
        elif event.type == pygame.MOUSEBUTTONUP:
            clique = False
        elif event.type == pygame.KEYDOWN:
            try:
                numCase = dictKey[event.key]
                print(numCase)
            except:
                if event.key == K_s: #appuyer sur 's' pour enregistrer la map
                    save(plateau.Matrice, fileName)
                elif event.key == K_u: #'u' revient à la dernière sauvegarde
                    plateau = Plateau(pygame)
                elif event.key == K_RIGHT or event.key == K_LEFT: #sur une flêche
                    save(plateau.Matrice, fileName)
                    with open("lvl_actuel.txt","w") as fill:
                        lvl = plateau.lvl.num
                        if event.key == K_RIGHT: #fleche de droite -> +1 lvl
                            if lvl < plateau.maxLvl:
                                fill.write(str(lvl + 1))
                            else:
                                fill.write("1")
                        elif event.key == K_LEFT: #fleche de gauche -> -1 lvl
                            if lvl > 1:
                                fill.write(str(lvl - 1))
                            else:
                                fill.write(str(plateau.maxLvl))
                    
                    plateau = Plateau(pygame)
                    fileName = plateau.lvl.maptxt

                elif event.key == 13: #touche 'Entrer'
                    save(plateau.Matrice, fileName)
                    os.system("python3 ../Main.py")
                    plateau = Plateau(pygame)
                    fileName = plateau.lvl.maptxt


    clock.tick(60) #en fps, valeur +grande = jeu + rapide



pygame.quit()
