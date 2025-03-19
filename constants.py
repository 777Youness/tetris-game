#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Constantes pour le jeu Tetris à deux joueurs
"""

from enum import Enum, auto

# Constantes du jeu
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
GRID_BORDER = 4
GRID_PADDING = 20
SCOREBOARD_HEIGHT = 100
SCOREBOARD_PADDING = 10
PREVIEW_SIZE = 4
PREVIEW_PADDING = 10

# Couleurs des pièces (format RGB en hexadécimal)
COLORS = {
    'I': '#00FFFF',  # Cyan
    'J': '#0000FF',  # Bleu
    'L': '#FF8000',  # Orange
    'O': '#FFFF00',  # Jaune
    'S': '#00FF00',  # Vert
    'T': '#800080',  # Violet
    'Z': '#FF0000',  # Rouge
    'HEART': '#FF69B4',  # Rose
    'STAR': '#FFD700',  # Or
    'EMPTY': '#000000',  # Noir (cellule vide)
    'GRID': '#333333',  # Gris foncé (fond de la grille)
    'BORDER': '#FFFFFF',  # Blanc (bordure)
    'TEXT': '#FFFFFF',  # Blanc (texte)
    'SCOREBOARD': '#222222',  # Gris très foncé (fond du tableau de score)
}

# Définition des formes des pièces (les configurations de rotation sont définies plus bas)
SHAPES = {
    'I': [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)]
    ],
    'J': [
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(2, 0), (0, 1), (1, 1), (2, 1)]
    ],
    'L': [
        [(1, 0), (1, 1), (1, 2), (0, 2)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)]
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ],
    'S': [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]
    ],
    'T': [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(1, 0), (0, 1), (1, 1), (1, 2)]
    ],
    'Z': [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)]
    ],
    'HEART': [
        [(0, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2), (1, 3)]
    ],
    'STAR': [
        [(1, 0), (0, 1), (1, 1), (2, 1), (0, 2), (2, 2)]
    ]
}

# Liste des pièces normales (sans les pièces spéciales)
STANDARD_TETROMINOS = ['I', 'J', 'L', 'O', 'S', 'T', 'Z']
EASY_TETROMINOS = ['I', 'O']  # Pièces "faciles"
SPECIAL_TETROMINOS = ['HEART', 'STAR']  # Pièces spéciales

class PlayerType(Enum):
    """Enumération des types de joueurs"""
    HUMAN = auto()
    AI = auto()

class GameState(Enum):
    """Enumération des états du jeu"""
    RUNNING = auto()
    PAUSED = auto()
    GAME_OVER = auto()