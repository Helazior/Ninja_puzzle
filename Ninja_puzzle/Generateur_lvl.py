#Générateur de lvl

from random import *
import sys, os

from Plateau import *

import pygame

from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()


#0.1: quelle lvl:
pathname = os.path.dirname(sys.argv[0])

os.chdir (os.path.abspath(pathname))
os.chdir ("ressources")

lvl = 2
fileName = "lvl"+str(lvl)+".txt"

with open("lvl_actuel.txt","w") as fill:
    fill.write(str(lvl))

#0.2 creer lvl vide:
with open(fileName, "w") as fill:
    fill.write("")

#0.3 initialisation lvl et affichage:
plateau = Plateau(pygame)

ninja1 = pygame.image.load("ninja1.png").convert_alpha()
ninja2 = pygame.image.load("ninja2.png").convert_alpha()
ninja3 = pygame.image.load("ninja3.png").convert_alpha()
ninja4 = pygame.image.load("ninja4.png").convert_alpha()


#1.1: taille de la map
(taillex, tailley) = (9,3)
debutx = (plateau.nbCasesX - taillex) // 2
debuty = (plateau.nbCasesY - tailley) // 2

finx = debutx + taillex
finy = debuty + tailley

#1.2: nombres de caisses
nbCaisses = 4

#2.1: placer caisses:
listeCaisses = list()
for k in range(nbCaisses + 1):
    while 1:
        posx = debutx + randint(0, taillex - 1)
        posy = debuty + randint(0, tailley - 1)
        if [posx, posy] not in listeCaisses:
            break
    if k < nbCaisses:
        listeCaisses.append([posx, posy])
        plateau.Matrice[posy][posx] = 8
    else:
        #2.2: placer perso
        posPerso = [posx,posy]
        plateau.Matrice[posy][posx] = 3


    
for j in range(len(plateau.Matrice)):
    for i in range(len(plateau.Matrice[0])):
        if plateau.Matrice[j][i] == 8:
            plateau.fenetre.blit(plateau.imageCaissePlace, (30 * i, 30 * j))
        if plateau.Matrice[j][i] == 3:
            plateau.fenetre.blit(plateau.imageEnd, (30 * i, 30 * j))

#plateau.copy_fond = pygame.display.get_surface().copy()
pygame.display.flip()

listeDir = [[0,-1], [0,1], [1,0], [-1,0]]
listeIndexDir = [1,2,-1]

oldSens = -1
oldIncrement = 0

ite = 0
nbMoveCrate = 0
while ite <= 3 and nbMoveCrate <= 100:
    nbMoveCrate += 1
    #3: prendre une nouvelle caisse au pif
    while 1:
        numNextCrate = randint(0, nbCaisses - 1)

        posCrate_0 = listeCaisses[numNextCrate]
        directionCrate = listeDir[randint(0, 3)] 
        print()
        print("directionCrate = ",directionCrate) 
        posCrate_1 = [posCrate_0[0] + directionCrate[0], posCrate_0[1] + directionCrate[1]]

        posGo = [posCrate_1[0] - posPerso[0], posCrate_1[1] - posPerso[1]]

        if abs(posGo[0]) + abs(posGo[1]) > 0 and posCrate_1 not in listeCaisses and posCrate_1[0] >= debutx and posCrate_1[0] <= finx and posCrate_1[1] >= debuty and posCrate_1[1] <= finy:
            break
    
    #4: aller jusqu'à la prochaine caisse
    while abs(posGo[0]) + abs(posGo[1]) > 0: 
        sens = int(abs(posGo[0]) < abs(posGo[1]))

        increment = 1 - 2*(posGo[sens] > 0)
        
        posPerso_1 = list(posPerso)
        posPerso_1[sens] -= increment


        ite = 0
        dicoDir = {(0,1): [[1,1],[1,-1],[0,-1]],   (1,1): [[0,-1],[0,1],[1,-1]],    (0,-1): [[1,-1],[1,1],[0,1]],    (1,-1): [[0,1],[0,-1],[1,1]]}
        print(sens,increment)
        listeSensIncrement = dicoDir[(sens, increment)]
        print(listeSensIncrement)
        aleat = randint(0,1)
        while plateau.Matrice[posPerso_1[1]][posPerso_1[0]] >= 5 or (sens == oldSens and increment != oldIncrement):
            if plateau.Matrice[posPerso_1[1]][posPerso_1[0]] >= 5:
                print("caisse")
            if sens == oldSens and increment != oldIncrement:
                print("retour arrière")
            
            if ite >= 3:
                ite = 9
                print("lvl terminé car bloqué !!!")
                break


            if aleat and ite <= 1:
                if ite == 1:
                    [sens, increment] = listeSensIncrement[0]
                elif ite == 0:
                    [sens, increment] = listeSensIncrement[1]

            else:
                [sens, increment] = listeSensIncrement[ite]

            print("[sens, increment]", [sens, increment])
            posPerso_1 = list(posPerso)
            posPerso_1[sens] = posPerso[sens] - increment

            ite += 1
            

        if ite >= 9:
            break

        directionPerso = [0,0]
        directionPerso[sens] -= increment

        posGo[sens] += increment
        
        if plateau.Matrice[posPerso[1]][posPerso[0]] != 3:
            plateau.Matrice[posPerso[1]][posPerso[0]] = 0
            plateau.fenetre.blit(plateau.imageFond, (30 * posPerso[0], 30 * posPerso[1]))
        else:
            plateau.fenetre.blit(plateau.imageEnd, (30 * posPerso[0], 30 * posPerso[1]))

        posPerso[sens] -= increment 

        oldSens = sens
        oldIncrement = increment

        if directionPerso == [0,-1]:
            imageNinja = ninja2
        elif directionPerso == [0,1]:
            imageNinja = ninja1
        elif directionPerso == [1,0]:
            imageNinja = ninja4
        else:
            imageNinja = ninja3
         
        #plateau.fenetre.blit(plateau.copy_fond, (0,0))
        plateau.fenetre.blit(imageNinja, (30 * posPerso[0], 30 * posPerso[1]))

        pygame.display.flip()
        
        #plateau.copy_fond = pygame.display.get_surface().copy()
        
        clock.tick(20)

    if ite >= 9:
        break

    #5: tirer la caisse
    print("Pull crate") 
    nbPull = randint(1, min(3, max(taillex, tailley))) 
    print("nbPull=", nbPull)
    
    sens = int(posCrate_1[0] - posCrate_0[0] == 0)
    increment = 1 - 2*int(directionCrate[sens] > 0)
    directionPerso = [0,0]
    directionPerso[sens] -= increment
    print("directionPerso=", directionPerso)
    if directionPerso == [0,-1]:
        imageNinja = ninja2
    elif directionPerso == [0,1]:
        imageNinja = ninja1
    elif directionPerso == [1,0]:
        imageNinja = ninja4
    else:
        imageNinja = ninja3


    for i in range(nbPull):
        posPerso_1 = list(posPerso)
        posPerso_1[sens] -= increment
        if plateau.Matrice[posPerso_1[1]][posPerso_1[0]] >= 5 or posPerso_1[0] < debutx or posPerso_1[0] > finx or posPerso_1[1] < debuty or posPerso_1[1] > finy:
            print("break")
            break

        #nouvel emplacement de la caisse, ancien du perso
        plateau.Matrice[posPerso[1]][posPerso[0]] += 5
        
        case = plateau.Matrice[posPerso[1]][posPerso[0]]

        caisse = plateau.imageCaisse
        if case == 8:
            caisse = plateau.imageCaissePlace
        elif case == 6:
            plateau.Matrice[posPerso[1]][posPerso[0]] = 5
        
        plateau.fenetre.blit(caisse, (30 * posPerso[0], 30 * posPerso[1]))
        
        #ancien de la caisse
        posAncienCaisse = list(posPerso)
        posAncienCaisse[sens] += increment
        
        plateau.Matrice[posAncienCaisse[1]][posAncienCaisse[0]] -= 5

        if plateau.Matrice[posAncienCaisse[1]][posAncienCaisse[0]] != 3:
            plateau.Matrice[posAncienCaisse[1]][posAncienCaisse[0]] = 0
            plateau.fenetre.blit(plateau.imageFond, (30 * posAncienCaisse[0], 30 * posAncienCaisse[1]))
        else:
            plateau.fenetre.blit(plateau.imageEnd, (30 * posAncienCaisse[0], 30 * posAncienCaisse[1]))


        listeCaisses[numNextCrate][sens] -= increment

        #nouveau pos perso 
        plateau.fenetre.blit(imageNinja, (30 * posPerso_1[0], 30 * posPerso_1[1]))
        
        posPerso = list(posPerso_1)
                
        pygame.display.flip()
        clock.tick(15) 

plateau.Matrice[posPerso[1]][posPerso[0]] = 2

matrice = plateau.Matrice

try:
    with open(fileName, "w") as fichier:
        for ligne in matrice:
            for chiffre in ligne:
                chiffre = str(chiffre)
                fichier.write(chiffre)
            fichier.write("\n")

    print(f"{fileName} a bien été enregistré !")
except:
    print("ERREUR d'enregistrement...")

while 1:
    pass
pygame.quit()
