#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#main
"""
-enregistrer map éditeur lors que -> ou <- que lors d'une modification sur la map
-pouvoir agrandir la fenêtre
-faire un menu avec tous les lvl
-retour en arrière avec les caisses (limiter à quelques coups)



faire ennemie statique qui tirent boules de feu en ligne et meurent quand on les touches


Voir uniquement dans la direction qu'on regarde, le reste est noir. (comme warcraft III)
i.e. on découvre la map au début, puis quand on l'a vu elle est juste sombre,
par contre les ennemies ne sont visibles que lorsqu'on les regarde en face.
une caisse va, par exemple, cacher la vision (mais aussi nous proteger).
Les enemies laissent des traces, donc on peut se douter de leure présence.

On peut débloquer des téléporteurs en plaçant les caisses à certains endroits;
Et ouvrir des murs de la même manière
"""

import sys
import os
import pygame
from pygame.locals import *

from perso import *
from plateau import * #sous-programme comprennant toutes les fonctions et la classe concernant la map

pygame.init()

pathname = os.path.dirname(sys.argv[0]) #mur du programme

os.chdir (os.path.abspath(pathname))    #c'est pour que le repertoire courant soit au niveau du programme
try:
    os.chdir ("ressources")                 #c'est pour que le repertoire courant soit dans "ressources"
except FileNotFoundError:
    print("\nFileNotFoundError : Le fichier ressources n'existe pas")
    sys.exit(1)
clock = pygame.time.Clock() #initialise une horloge pour gerer le temps

KEYS_ARROWS = [K_DOWN, K_UP, K_RIGHT, K_LEFT]
KEYS_JUMPS = [K_w, K_SPACE]
#setup pour le plateau
continuer = True


#_________________________________________________boucle principale:_________________________________________________
pygame.key.set_repeat(300, 120)#temps avant de rep la touche et temps entre chaque touches

while continuer: #tout ce passe là dedans
    #_________________________________________________création objet:___________________________________________________

    restart = False
    plateau = Plateau(pygame)
    ninja = Perso(plateau)

    while not restart:
        for event in pygame.event.get(): #il passe toutes les touches en revu pour voir lorsque tu appuies sur une touche
            pygame.event.pump() #c'est pour pas qu'il fasse "le programme ne répond plus", normalement ça marche sans mais pour moi non

            if event.type == pygame.QUIT: #quand t'appuies sur la croix ça quitte
                restart = True
                continuer = False
                #retenir le lvl

            elif event.type == pygame.KEYDOWN:
                if event.key in KEYS_ARROWS: # on a appuyé sur une flêche
                    ninja.move(plateau, event.key) #bouger ninja

                elif event.key in KEYS_JUMPS and plateau.lvl.jump: # touche w
                    ninja.jump(plateau) #sauter de 2 cases
                elif event.key == K_u and ninja.lastPosMatrice != [] and plateau.lvl.back: #touche u
                    ninja.back(plateau)
                elif event.key == K_r:
                    print("Restart")
                    restart = True

                elif event.key == K_ESCAPE:
                    restart = True
                    continuer = False

                elif event.key in [K_PLUS, K_EQUALS]:
                    change_lvl(plateau, 1)
                    restart = True
                elif event.key == K_MINUS:
                    change_lvl(plateau, -1)
                    restart = True


        if ninja.win:
            print("lvl terminée !")
            change_lvl(plateau, 1)
            restart = True

        clock.tick(45) #en fps, valeur +grande = plateau + rapide
        pygame.display.flip() #rafraichit l'image

pygame.quit()
