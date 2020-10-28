# Ninja_puzzle
Sokoban amélioré.

Flêches pour se déplacer, le but est d'arriver au point noir.
'+' pour passer au niveau suivant.
Sur certains niveaux:
'w' ou 'z' pour sauter 2 blocs
'u' pour revenir en arrière

Editeur_de_map.py: pour créer de nouvelles maps
- 0,1,2,3,5 pour choisir le bloc correspondant (0 par défaut)
- clique pour poser un bloc
- rester appuyé et bouger la souris pour poser plein de blocs
- 's' pour enregistrer (en fait pour l'instant ça enregistre automatiquement quand on quitte)
- 'u' pour revenir à la dernière sauvegarde, utile pour ne pas enregistrer ('z' était trop proche de 's')
- "Entrer" pour tester le lvl, ne fonctionne que sur Linux.
- flêches droite/gauche pour se déplacer dans les niveaux.

- fileName est le nom du fichier texte, il doit exister. Maintenant contenu dans le fichier lvl_actuel.txt

Generateur_lvl.py:
C'est un test pour générer des maps automatiquement qui fonctionne mais donne des maps extrêment simples.

** **

Étapes d'améliorations dans le Main.c en commentaire 
