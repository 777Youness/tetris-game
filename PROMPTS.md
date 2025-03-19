# PROMPTS.md

## Présentation du Projet

Ce projet Tetris à deux joueurs (Humain vs IA) a été créé en utilisant des prompts de ChatGPT pour Claude 3.7 Sonnet, et a été édité par le chat de l'éditeur Cursor pour les améliorations et la finition. Voici la liste des prompts utilisés.

Au début, j'ai fourni le PDF du projet à ChatGPT, qui m'a généré un **prompt global** pour créer le projet dans son ensemble. Ensuite, j'ai **redonné ce prompt global à ChatGPT** pour qu'il me crée des **prompts spécifiques à utiliser avec Claude 3.7 Sonnet**, afin d'implémenter chaque fonctionnalité étape par étape.

## Prompt Principal

```
Crée moi des prompts pour Claude 3.7 afin qu'il me génère un projet Tetris en Python avec Tkinter à deux joueurs : un humain et une IA. Le jeu doit inclure les fonctionnalités suivantes :

Grilles de jeu : Deux grilles de 10x20 cases, placées côte à côte, une pour le joueur humain et une pour l'IA.

Pièces : Implémente les 7 pièces classiques (I, O, T, L, J, S, Z) avec des couleurs distinctes et la possibilité de pivoter.

Contrôles du joueur humain :
- Flèche gauche : déplacer la pièce à gauche.
- Flèche droite : déplacer la pièce à droite.
- Flèche bas : accélérer la descente.
- Flèche haut : faire pivoter la pièce.

IA : Une IA basique qui joue automatiquement, cherchant à minimiser les trous et éviter les empilements trop hauts.

Système de score :
- 50 points par ligne complétée.
- Bonus : 100 points pour 2 lignes, 200 points pour 3 lignes, et 300 points pour un Tetris (4 lignes).

Règles spéciales :
- 🎁 Cadeau surprise : Si un joueur complète 2 lignes en une fois, l'adversaire reçoit une "pièce facile" (carré ou ligne droite) au tour suivant.
- ⏳ Pause douceur : Tous les 1 000 points, la chute des pièces ralentit de 20 % pendant 10 secondes pour les deux joueurs.
- ⭐ Pièce rigolote : Tous les 3 000 points, fais apparaître une pièce spéciale (en forme de cœur ou d'étoile) qui rapporte 100 points si bien placée.
- 🌈 Arc-en-ciel : Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes, pour le fun visuel sans impact sur le gameplay.

Affichage des scores : Montre le score en temps réel pour les deux joueurs.

Optimisation : Assure-toi que le code est lisible, modulaire, avec des classes distinctes pour la grille, les pièces, le joueur et l'IA.
```

## Prompts Spécifiques

### 1. Structure de Base
```
Crée la structure de base pour un projet Tetris en Python avec Tkinter. Le projet doit inclure deux joueurs : un humain et une IA, chacun ayant sa propre grille. Ajoute un tableau de scores pour afficher les points des deux joueurs.
```

### 2. Création des Grilles et Gestion des Pièces
```
Implémente les grilles de jeu 10x20 cases et les pièces du Tetris (I, O, T, L, J, S, Z) en Python avec Tkinter. Chaque pièce doit avoir une couleur différente et pouvoir pivoter. Utilise des classes pour gérer la grille et les pièces.
```

### 3. Contrôles du Joueur Humain
```
Ajoute les contrôles pour le joueur humain : flèche gauche pour déplacer à gauche, flèche droite pour déplacer à droite, flèche bas pour descendre rapidement et flèche haut pour faire pivoter la pièce.
```

### 4. IA Basique
```
Crée une IA basique pour le Tetris. L'IA doit jouer automatiquement avec une logique simple : remplir les trous et éviter les empilements trop hauts. Elle joue dans sa propre grille indépendamment du joueur humain.
```

### 5. Système de Score
```
Ajoute un système de score pour le Tetris : 50 points par ligne complétée, 100 pour 2 lignes, 200 pour 3 lignes et 300 pour un Tetris (4 lignes). Affiche les scores en temps réel pour les deux joueurs.
```

### 6. Cadeau Surprise
```
Ajoute la règle "cadeau surprise" : si un joueur complète 2 lignes en une fois, l'adversaire reçoit une pièce facile (carré ou ligne droite) lors de son prochain tour.
```

### 7. Pause Douceur
```
Ajoute la règle "pause douceur" : tous les 1 000 points, ralentis la chute des pièces de 20 pour cent pendant 10 secondes pour les deux joueurs.
```

### 8. Pièce Rigolote
```
Implémente la règle "pièce rigolote" : tous les 3 000 points, fais apparaître une pièce spéciale en forme de cœur ou d'étoile qui donne un bonus de 100 points si bien placée.
```

### 9. Arc-en-Ciel
```
Ajoute l'effet "arc-en-ciel" : toutes les 2 minutes, change la couleur des pièces pendant 20 secondes sans modifier le gameplay.
```

### 10. Optimisation de la Structure du Code
```
Réorganise le code pour qu'il soit plus lisible, utilise des fonctions claires, évite les répétitions et ajoute des commentaires pour expliquer les parties importantes.
```

### 11. Amélioration des Performances
```
Optimise les performances du jeu pour éviter les ralentissements surtout lorsque les deux grilles sont actives. Utilise des timers efficaces et réduis les calculs nécessaires dans la boucle principale.
```

### 12. Nettoyage du Code
```
Vérifie le code pour enlever les répétitions, ajouter des commentaires clairs et améliorer la lisibilité générale.
```

### 13. Correction des Bugs
```
Teste le projet pour identifier et corriger les bugs potentiels : problèmes de collision, mauvaise gestion des scores ou comportements inattendus de l'IA.
```
