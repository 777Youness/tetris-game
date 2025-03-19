#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classes de données pour le jeu Tetris à deux joueurs
"""

import time
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional, Set, Callable
from constants import PlayerType, GameState

@dataclass
class Player:
    """Classe représentant un joueur"""
    type: PlayerType
    grid: List[List[str]]  # Grille contenant les pièces placées
    score: int = 0
    current_piece: Optional[str] = None  # Type de la pièce actuelle
    current_rotation: int = 0  # Rotation actuelle de la pièce
    current_position: Tuple[int, int] = (0, 0)  # Position (ligne, colonne) de la pièce actuelle
    next_piece: Optional[str] = None  # Type de la prochaine pièce
    lines_cleared: int = 0  # Nombre total de lignes complétées
    speed_modifier: float = 1.0  # Modificateur de vitesse (< 1.0 = plus lent)
    speed_modifier_end_time: float = 0  # Temps de fin de l'effet de vitesse
    rainbow_end_time: float = 0  # Temps de fin de l'effet arc-en-ciel
    gift_next_piece: bool = False  # Indique si le joueur doit recevoir une pièce facile

@dataclass
class GameSession:
    """Classe représentant une session de jeu"""
    human_player: Player
    ai_player: Player
    state: GameState = GameState.RUNNING
    start_time: float = 0
    last_rainbow_time: float = 0
    special_piece_threshold: int = 3000  # Seuil de points pour la pièce spéciale
    last_special_piece_time: Dict[PlayerType, float] = None

    def __post_init__(self):
        if self.last_special_piece_time is None:
            self.last_special_piece_time = {
                PlayerType.HUMAN: 0,
                PlayerType.AI: 0
            }
        self.start_time = time.time()