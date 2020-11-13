#Perso

import pygame

def conv_pixel(pos):
    return [pos[0]*30, pos[1]*30]

def recherche_debut(plateau):
    matrice = plateau.Matrice
    for j in range(len(matrice)):
        for i in range(len(matrice[j])):
            if matrice[j][i] == 2:
                return [i,j]
    print("Erreur: Pas de départ sur la map")
    return [21,19]


class Perso():
    def __init__(self, plateau):
        self.image1 = pygame.image.load("ninja1.png").convert_alpha()
        self.image2 = pygame.image.load("ninja2.png").convert_alpha()
        self.image3 = pygame.image.load("ninja3.png").convert_alpha()
        self.image4 = pygame.image.load("ninja4.png").convert_alpha()

        posDebut = recherche_debut(plateau)
        self.posMatrice = posDebut #on place le perso au début
        plateau.fenetre.blit(self.image1, conv_pixel(self.posMatrice)) #On affiche le perso
        self.dicoDirections = {1:[0,-1], 2:[0,1], 3:[1,0], 4:[-1,0]}
        self.direction = self.dicoDirections[1]
        self.lastPosMatrice = []
        self.lastDirection = []
        self.win = False
        
    def move(self, plateau, key):
        direction = self.dicoDirections[key - 272]
        self.show(plateau, 1, direction)
        

    def jump(self, plateau):
        self.show(plateau, 2, self.direction)

    def back(self, plateau):
        self.posMatrice = self.lastPosMatrice[-1]
        del self.lastPosMatrice[-1]
        self.direction = self.lastDirection[-1]
        del self.lastDirection[-1]
        plateau.fenetre.blit(plateau.copy_fond,(0, 0))        
        plateau.fenetre.blit(self.imageDirection(), conv_pixel(self.posMatrice))


    def show(self, plateau, step, direction):
 
        posx_0 = self.posMatrice[0]
        posy_0 = self.posMatrice[1]
        
        posx_1 = posx_0 + step * direction[0]
        posy_1 = posy_0 + step * direction[1]

        posx_2 = posx_1 + direction[0]
        posy_2 = posy_1 + direction[1]

        setGround = {0,2,3}
        if posx_1 >= 0 and posx_1 < plateau.nbCasesX and posy_1 >= 0 and posy_1 < plateau.nbCasesY:
            if plateau.Matrice[posy_1][posx_1] in setGround or (posy_2 <= 19 and posy_2 >= 0 and posx_2 <= 39 and posx_2 >= 0 and plateau.Matrice[posy_1][posx_1] >= 5 and plateau.Matrice[posy_2][posx_2] in setGround) and step == 1:
                self.lastDirection.append(list(direction))
                self.lastPosMatrice.append(list(self.posMatrice))

                if plateau.Matrice[posy_1][posx_1] >= 5 and step == 1:
                    plateau.Matrice[posy_1][posx_1] -= 5 
                    plateau.Matrice[posy_2][posx_2] += 5

                    plateau.fenetre.blit(plateau.copy_fond,(0, 0))
                    
                    mat = plateau.Matrice[posy_1][posx_1]
                    pos1 = (30*posx_1, 30*posy_1)
                    if (posx_0 + posy_0) % 2: 
                        plateau.fenetre.blit(plateau.imageFond2, pos1)
                    else:
                        plateau.fenetre.blit(plateau.imageFond, pos1)

                    if mat == 2:
                        plateau.fenetre.blit(plateau.imageStart, pos1)
                    elif mat == 3:
                        plateau.fenetre.blit(plateau.imageEnd, pos1)                 
                    
                    image = plateau.imageCaisse
                    if plateau.Matrice[posy_2][posx_2] == 8:
                        plateau.nbEnd -= 1
                        image = plateau.imageCaissePlace
                    
                    plateau.fenetre.blit(image, (30*posx_2, 30*posy_2))

                    if plateau.Matrice[posy_1][posx_1] == 3:
                        plateau.nbEnd += 1


                    plateau.copy_fond = pygame.display.get_surface().copy()
                


                self.posMatrice[0] = posx_1
                self.posMatrice[1] = posy_1
                self.direction = direction
  
                plateau.fenetre.blit(plateau.copy_fond,(0, 0))
                plateau.fenetre.blit(self.imageDirection(), conv_pixel(self.posMatrice))
                self.direction = direction


                if plateau.Matrice[posy_1][posx_1] == 3:
                    plateau.nbEnd -= 1

                if plateau.Matrice[posy_0][posx_0] == 3:
                    plateau.nbEnd += 1

                if plateau.nbEnd == 0:
                    self.win = True

                

    def imageDirection(self):

        if self.direction == [0,-1]:
            return self.image1
        elif self.direction == [0,1]:
            return self.image2
        elif self.direction == [1,0]:
            return self.image3
        else:
            return self.image4

        

