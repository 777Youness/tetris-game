# Tetris à deux joueurs (Humain vs IA)

Un jeu de Tetris à deux joueurs où un joueur humain affronte une IA, avec des règles spéciales pour rendre le jeu plus dynamique et amusant.

## Comment lancer le jeu

1. Assurez-vous d'avoir Python 3.6 ou supérieur installé sur votre système.
2. Aucune bibliothèque externe n'est nécessaire, le jeu utilise uniquement Tkinter qui est inclus dans l'installation standard de Python.
3. Exécutez le jeu avec la commande suivante :

python main.py

## Commandes pour le joueur humain

- **Flèche gauche** : Déplacer la pièce vers la gauche
- **Flèche droite** : Déplacer la pièce vers la droite
- **Flèche bas** : Accélérer la descente de la pièce
- **Flèche haut** : Faire pivoter la pièce
- **Espace** : Faire tomber la pièce instantanément
- **P** : Mettre le jeu en pause / Reprendre le jeu
- **R** : Redémarrer le jeu

## Règles spéciales

Le jeu inclut plusieurs règles spéciales pour rendre l'expérience plus intéressante :

### Système de score
- 1 ligne complétée = 50 points
- 2 lignes complétées = 100 points
- 3 lignes complétées = 200 points
- 4 lignes complétées (Tetris) = 300 points

### Cadeau surprise
Si un joueur complète exactement 2 lignes en une fois, son adversaire reçoit une pièce facile (I ou O) lors de son prochain tour.

### Pause douceur
Tous les 1 000 points, la chute des pièces est ralentie de 20% pendant 10 secondes pour les deux joueurs, offrant un moment de répit.

### Pièce rigolote
Tous les 3 000 points, une pièce spéciale (en forme de cœur ou d'étoile) peut apparaître avec une probabilité de 20%.
- Le cœur ralentit la chute des pièces de l'adversaire pendant 15 secondes.
- L'étoile active le mode arc-en-ciel pendant 10 secondes.

### Effet arc-en-ciel
Toutes les 2 minutes, les pièces changent de couleur aléatoirement pendant 20 secondes, sans modifier le gameplay.

## Stratégie de l'IA

L'IA utilise un algorithme d'évaluation pour déterminer le meilleur placement pour chaque pièce. Elle prend en compte plusieurs facteurs comme la hauteur de la pile, les trous créés, et la complétion des lignes.

