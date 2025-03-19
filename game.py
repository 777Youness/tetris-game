#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe principale du jeu Tetris à deux joueurs
"""

import tkinter as tk
import random
import time
import threading
import copy
from typing import List, Tuple, Dict, Optional, Set, Callable

from constants import (
    GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE, GRID_BORDER, GRID_PADDING,
    SCOREBOARD_HEIGHT, SCOREBOARD_PADDING, PREVIEW_SIZE, PREVIEW_PADDING,
    COLORS, SHAPES, STANDARD_TETROMINOS, EASY_TETROMINOS, SPECIAL_TETROMINOS,
    PlayerType, GameState
)
from models import Player, GameSession
from ai import TetrisAI

class TetrisGame:
    """Classe principale du jeu Tetris"""
    
    def __init__(self, root):
        """Initialise le jeu"""
        self.root = root
        self.root.title("Tetris à deux joueurs (Humain vs IA)")
        
        # Créer un conteneur principal
        self.main_container = tk.Frame(root, bg='black')
        self.main_container.pack(expand=True, fill='both')
        
        # Augmenter la largeur de la fenêtre pour avoir plus d'espace
        window_width = (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) * 2 + GRID_PADDING * 5 + (PREVIEW_SIZE * BLOCK_SIZE) * 2 + 200
        window_height = GRID_HEIGHT * BLOCK_SIZE + GRID_BORDER * 2 + GRID_PADDING * 2 + SCOREBOARD_HEIGHT + SCOREBOARD_PADDING * 2 + 50
        
        # Positionner la fenêtre au centre de l'écran
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Créer le canevas pour dessiner
        self.canvas = tk.Canvas(self.main_container, width=window_width, height=window_height, bg='black')
        self.canvas.pack(expand=True, fill='both')
        
        # Calculer les positions des grilles avec plus d'espace entre elles
        self.human_grid_x = GRID_PADDING * 2
        self.human_grid_y = GRID_PADDING
        self.ai_grid_x = window_width - GRID_PADDING * 2 - (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2)
        self.ai_grid_y = GRID_PADDING
        
        # Calculer les positions des prévisualisations
        # Prévisualisation du joueur humain à droite de sa grille
        self.human_preview_x = self.human_grid_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) + 20
        self.human_preview_y = self.human_grid_y + 50
        
        # Prévisualisation de l'IA à gauche de sa grille
        self.ai_preview_x = self.ai_grid_x - (PREVIEW_SIZE * BLOCK_SIZE) - 20
        self.ai_preview_y = self.ai_grid_y + 50
        
        # Calculer la position du tableau des scores
        # Positionner le tableau des scores sous les grilles
        self.scoreboard_x = window_width / 2 - ((GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) * 2 + GRID_PADDING) / 2
        self.scoreboard_y = self.human_grid_y + GRID_HEIGHT * BLOCK_SIZE + GRID_BORDER * 2 + SCOREBOARD_PADDING
        
        # Initialiser les grilles
        human_grid = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        ai_grid = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Initialiser les joueurs
        self.human_player = Player(
            type=PlayerType.HUMAN,
            grid=human_grid,
            score=0,
            current_piece=None,
            current_rotation=0,
            current_position=(0, 0),
            next_piece=None
        )
        
        self.ai_player = Player(
            type=PlayerType.AI,
            grid=ai_grid,
            score=0,
            current_piece=None,
            current_rotation=0,
            current_position=(0, 0),
            next_piece=None
        )
        
        # Initialiser la session de jeu
        self.game = GameSession(
            human_player=self.human_player,
            ai_player=self.ai_player,
            state=GameState.RUNNING
        )
        
        # Variables de jeu
        self.rainbow_mode = False
        self.fall_speed = 1.0  # En secondes
        self.game_tick = 50  # En millisecondes
        self.last_fall_time = time.time()
        self.rainbow_colors = list(COLORS.values())[:7]  # Utiliser uniquement les couleurs des pièces standards
        
        # Lier les touches du clavier
        self.root.bind('<Left>', self.move_left)
        self.root.bind('<Right>', self.move_right)
        self.root.bind('<Down>', self.move_down)
        self.root.bind('<Up>', self.rotate)
        self.root.bind('<space>', self.drop)
        self.root.bind('<p>', self.toggle_pause)
        self.root.bind('<P>', self.toggle_pause)
        self.root.bind('<r>', self.restart_game)  # Ajouter la touche 'r' minuscule
        self.root.bind('<R>', self.restart_game)  # Ajouter la touche 'R' majuscule
        
        # Démarrer le jeu
        self.restart_game()
        
        # Démarrer la boucle de jeu
        self.game_loop()
        
        # Démarrer la boucle de l'IA dans un thread séparé
        self.ai_thread = threading.Thread(target=self.ai_loop, daemon=True)
        self.ai_thread.start()
    
    def draw_grid(self, grid_x, grid_y, grid):
        """Dessine une grille de jeu"""
        # Dessiner le fond de la grille
        self.canvas.create_rectangle(
            grid_x - GRID_BORDER,
            grid_y - GRID_BORDER,
            grid_x + GRID_WIDTH * BLOCK_SIZE + GRID_BORDER,
            grid_y + GRID_HEIGHT * BLOCK_SIZE + GRID_BORDER,
            fill=COLORS['GRID'],
            outline=COLORS['BORDER'],
            width=GRID_BORDER
        )
        
        # Dessiner les cellules de la grille
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                x = grid_x + col * BLOCK_SIZE
                y = grid_y + row * BLOCK_SIZE
                if grid[row][col]:
                    color = grid[row][col]
                    # Vérifier si on doit appliquer l'effet arc-en-ciel
                    if self.rainbow_mode:
                        # Utiliser une couleur aléatoire parmi les 7 couleurs standard
                        color = random.choice(self.rainbow_colors)
                    self.canvas.create_rectangle(
                        x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                        fill=color, outline='#444444'
                    )
    
    def draw_piece(self, player, grid_x, grid_y):
        """Dessine la pièce actuelle d'un joueur"""
        if not player.current_piece:
            return
        
        # Obtenir les coordonnées de la pièce
        shape_coords = self.get_piece_coordinates(player)
        row_offset, col_offset = player.current_position
        
        # Dessiner chaque bloc de la pièce
        for row, col in shape_coords:
            grid_row = row + row_offset
            grid_col = col + col_offset
            
            # Ne dessiner que si le bloc est visible sur la grille
            if 0 <= grid_row < GRID_HEIGHT and 0 <= grid_col < GRID_WIDTH:
                x = grid_x + grid_col * BLOCK_SIZE
                y = grid_y + grid_row * BLOCK_SIZE
                
                color = COLORS[player.current_piece]
                # Vérifier si on doit appliquer l'effet arc-en-ciel
                if self.rainbow_mode:
                    # Utiliser une couleur aléatoire parmi les 7 couleurs standard
                    color = random.choice(self.rainbow_colors)
                
                self.canvas.create_rectangle(
                    x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                    fill=color, outline='#444444'
                )
    
    def draw_preview(self, player, preview_x, preview_y):
        """Dessine la prévisualisation de la prochaine pièce"""
        if not player.next_piece:
            return
        
        # Dessiner le fond de la prévisualisation
        preview_width = PREVIEW_SIZE * BLOCK_SIZE
        preview_height = PREVIEW_SIZE * BLOCK_SIZE
        self.canvas.create_rectangle(
            preview_x, preview_y,
            preview_x + preview_width, preview_y + preview_height,
            fill=COLORS['GRID'], outline=COLORS['BORDER']
        )
        
        # Obtenir les coordonnées de la pièce
        shape = SHAPES[player.next_piece][0]  # Utiliser la première rotation
        
        # Calculer le centre de la prévisualisation
        min_row = min(row for row, _ in shape)
        max_row = max(row for row, _ in shape)
        min_col = min(col for _, col in shape)
        max_col = max(col for _, col in shape)
        piece_height = max_row - min_row + 1
        piece_width = max_col - min_col + 1
        
        # Calculer l'offset pour centrer la pièce
        row_offset = (PREVIEW_SIZE - piece_height) // 2
        col_offset = (PREVIEW_SIZE - piece_width) // 2
        
        # Dessiner chaque bloc de la pièce
        for row, col in shape:
            adjusted_row = row - min_row + row_offset
            adjusted_col = col - min_col + col_offset
            
            x = preview_x + adjusted_col * BLOCK_SIZE
            y = preview_y + adjusted_row * BLOCK_SIZE
            
            color = COLORS[player.next_piece]
            # Vérifier si on doit appliquer l'effet arc-en-ciel
            if self.rainbow_mode:
                # Utiliser une couleur aléatoire parmi les 7 couleurs standard
                color = random.choice(self.rainbow_colors)
            
            self.canvas.create_rectangle(
                x, y, x + BLOCK_SIZE, y + BLOCK_SIZE,
                fill=color, outline='#444444'
            )
        
        # Afficher le nom de la pièce
        self.canvas.create_text(
            preview_x + preview_width // 2,
            preview_y + preview_height + 20,
            text=player.next_piece,
            fill=COLORS['TEXT'],
            font=('Helvetica', 12)
        )
    
    def draw_scoreboard(self):
        """Dessine le tableau des scores"""
        # Dessiner le fond du tableau
        self.canvas.create_rectangle(
            self.scoreboard_x,
            self.scoreboard_y,
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) * 2 + GRID_PADDING,
            self.scoreboard_y + SCOREBOARD_HEIGHT,
            fill=COLORS['SCOREBOARD'],
            outline=COLORS['BORDER']
        )
        
        # Afficher les scores
        self.canvas.create_text(
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) // 2,
            self.scoreboard_y + SCOREBOARD_HEIGHT // 4,
            text="JOUEUR HUMAIN",
            fill=COLORS['TEXT'],
            font=('Helvetica', 16, 'bold')
        )
        
        self.canvas.create_text(
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) // 2,
            self.scoreboard_y + SCOREBOARD_HEIGHT // 2,
            text=f"Score: {self.human_player.score}",
            fill=COLORS['TEXT'],
            font=('Helvetica', 14)
        )
        
        self.canvas.create_text(
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) // 2,
            self.scoreboard_y + 3 * SCOREBOARD_HEIGHT // 4,
            text=f"Lignes: {self.human_player.lines_cleared}",
            fill=COLORS['TEXT'],
            font=('Helvetica', 14)
        )
        
        self.canvas.create_text(
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) * 3 // 2 + GRID_PADDING,
            self.scoreboard_y + SCOREBOARD_HEIGHT // 4,
            text="JOUEUR IA",
            fill=COLORS['TEXT'],
            font=('Helvetica', 16, 'bold')
        )
        
        self.canvas.create_text(
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) * 3 // 2 + GRID_PADDING,
            self.scoreboard_y + SCOREBOARD_HEIGHT // 2,
            text=f"Score: {self.ai_player.score}",
            fill=COLORS['TEXT'],
            font=('Helvetica', 14)
        )
        
        self.canvas.create_text(
            self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) * 3 // 2 + GRID_PADDING,
            self.scoreboard_y + 3 * SCOREBOARD_HEIGHT // 4,
            text=f"Lignes: {self.ai_player.lines_cleared}",
            fill=COLORS['TEXT'],
            font=('Helvetica', 14)
        )
        
        # Afficher l'état du jeu
        if self.game.state == GameState.PAUSED:
            self.canvas.create_text(
                self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) + GRID_PADDING // 2,
                self.scoreboard_y + SCOREBOARD_HEIGHT // 2,
                text="PAUSE",
                fill='#FF0000',
                font=('Helvetica', 18, 'bold')
            )
        elif self.game.state == GameState.GAME_OVER:
            self.canvas.create_text(
                self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) + GRID_PADDING // 2,
                self.scoreboard_y + SCOREBOARD_HEIGHT // 2,
                text="GAME OVER",
                fill='#FF0000',
                font=('Helvetica', 18, 'bold')
            )
    
    def draw_special_effects(self):
        """Dessine les effets spéciaux"""
        current_time = time.time()
        
        # Vérifier si on doit afficher l'effet de ralentissement
        if self.human_player.speed_modifier < 1.0 and current_time < self.human_player.speed_modifier_end_time:
            remaining = int(self.human_player.speed_modifier_end_time - current_time)
            self.canvas.create_text(
                self.human_grid_x + (GRID_WIDTH * BLOCK_SIZE) // 2,
                self.human_grid_y - 20,
                text=f"Ralenti pendant {remaining}s",
                fill='#00FFFF',
                font=('Helvetica', 12, 'bold')
            )
        
        if self.ai_player.speed_modifier < 1.0 and current_time < self.ai_player.speed_modifier_end_time:
            remaining = int(self.ai_player.speed_modifier_end_time - current_time)
            self.canvas.create_text(
                self.ai_grid_x + (GRID_WIDTH * BLOCK_SIZE) // 2,
                self.ai_grid_y - 20,
                text=f"Ralenti pendant {remaining}s",
                fill='#00FFFF',
                font=('Helvetica', 12, 'bold')
            )
        
        # Vérifier si on doit afficher l'effet de pause douceur (si les deux joueurs sont ralentis en même temps)
        if (self.human_player.speed_modifier < 1.0 and current_time < self.human_player.speed_modifier_end_time and
            self.ai_player.speed_modifier < 1.0 and current_time < self.ai_player.speed_modifier_end_time):
            remaining = int(min(self.human_player.speed_modifier_end_time, self.ai_player.speed_modifier_end_time) - current_time)
            self.canvas.create_text(
                self.scoreboard_x + (GRID_WIDTH * BLOCK_SIZE + GRID_BORDER * 2) + GRID_PADDING // 2,
                self.scoreboard_y - 20,
                text=f"PAUSE DOUCEUR! ({remaining}s)",
                fill='#FFA500',
                font=('Helvetica', 14, 'bold')
            )
        
        # Vérifier si on doit afficher l'effet arc-en-ciel
        if self.rainbow_mode:
            self.canvas.create_text(
                self.human_grid_x + (GRID_WIDTH * BLOCK_SIZE) // 2,
                self.human_grid_y - 40,
                text="MODE ARC-EN-CIEL !",
                fill='#FF00FF',
                font=('Helvetica', 12, 'bold')
            )
            
            self.canvas.create_text(
                self.ai_grid_x + (GRID_WIDTH * BLOCK_SIZE) // 2,
                self.ai_grid_y - 40,
                text="MODE ARC-EN-CIEL !",
                fill='#FF00FF',
                font=('Helvetica', 12, 'bold')
            )
        
        # Afficher l'indicateur de cadeau surprise
        if self.human_player.gift_next_piece:
            self.canvas.create_text(
                self.human_grid_x + (GRID_WIDTH * BLOCK_SIZE) // 2,
                self.human_grid_y - 60,
                text="CADEAU SURPRISE !",
                fill='#FFFF00',
                font=('Helvetica', 12, 'bold')
            )
        
        if self.ai_player.gift_next_piece:
            self.canvas.create_text(
                self.ai_grid_x + (GRID_WIDTH * BLOCK_SIZE) // 2,
                self.ai_grid_y - 60,
                text="CADEAU SURPRISE !",
                fill='#FFFF00',
                font=('Helvetica', 12, 'bold')
            )
    
    def update_display(self):
        """Met à jour l'affichage du jeu"""
        self.canvas.delete("all")
        
        # Dessiner les grilles
        self.draw_grid(self.human_grid_x, self.human_grid_y, self.human_player.grid)
        self.draw_grid(self.ai_grid_x, self.ai_grid_y, self.ai_player.grid)
        
        # Dessiner les pièces actuelles
        self.draw_piece(self.human_player, self.human_grid_x, self.human_grid_y)
        self.draw_piece(self.ai_player, self.ai_grid_x, self.ai_grid_y)
        
        # Dessiner les prévisualisations
        self.draw_preview(self.human_player, self.human_preview_x, self.human_preview_y)
        self.draw_preview(self.ai_player, self.ai_preview_x, self.ai_preview_y)
        
        # Dessiner le tableau des scores
        self.draw_scoreboard()
        
        # Dessiner les effets spéciaux
        self.draw_special_effects()
    
    def get_piece_coordinates(self, player):
        """Obtient les coordonnées de la pièce actuelle d'un joueur"""
        if not player.current_piece:
            return []
        
        rotation_index = player.current_rotation % len(SHAPES[player.current_piece])
        return SHAPES[player.current_piece][rotation_index]
    
    def is_valid_position(self, player, row_offset=0, col_offset=0, rotation_offset=0):
        """Vérifie si la position est valide pour la pièce actuelle"""
        if not player.current_piece:
            return False
        
        # Calculer la nouvelle rotation
        new_rotation = (player.current_rotation + rotation_offset) % len(SHAPES[player.current_piece])
        
        # Obtenir les coordonnées de la pièce avec la nouvelle rotation
        shape_coords = SHAPES[player.current_piece][new_rotation]
        
        # Calculer la nouvelle position
        current_row, current_col = player.current_position
        new_row = current_row + row_offset
        new_col = current_col + col_offset
        
        # Vérifier chaque bloc de la pièce
        for row, col in shape_coords:
            grid_row = new_row + row
            grid_col = new_col + col
            
            # Vérifier si le bloc est en dehors de la grille
            if grid_row < 0 or grid_row >= GRID_HEIGHT or grid_col < 0 or grid_col >= GRID_WIDTH:
                return False
            
            # Vérifier si le bloc entre en collision avec une cellule occupée
            if grid_row >= 0 and player.grid[grid_row][grid_col]:
                return False
        
        return True
    
    def move_left(self, event=None):
        """Déplace la pièce vers la gauche"""
        if self.game.state != GameState.RUNNING or not self.human_player.current_piece:
            return
        
        if self.is_valid_position(self.human_player, col_offset=-1):
            current_row, current_col = self.human_player.current_position
            self.human_player.current_position = (current_row, current_col - 1)
            self.update_display()
    
    def move_right(self, event=None):
        """Déplace la pièce vers la droite"""
        if self.game.state != GameState.RUNNING or not self.human_player.current_piece:
            return
        
        if self.is_valid_position(self.human_player, col_offset=1):
            current_row, current_col = self.human_player.current_position
            self.human_player.current_position = (current_row, current_col + 1)
            self.update_display()
    
    def move_down(self, event=None):
        """Déplace la pièce vers le bas"""
        if self.game.state != GameState.RUNNING or not self.human_player.current_piece:
            return
        
        if self.is_valid_position(self.human_player, row_offset=1):
            current_row, current_col = self.human_player.current_position
            self.human_player.current_position = (current_row + 1, current_col)
            self.update_display()
        else:
            self.place_piece(self.human_player)
    
    def rotate(self, event=None):
        """Fait pivoter la pièce"""
        if self.game.state != GameState.RUNNING or not self.human_player.current_piece:
            return
        
        if self.is_valid_position(self.human_player, rotation_offset=1):
            self.human_player.current_rotation = (self.human_player.current_rotation + 1) % len(SHAPES[self.human_player.current_piece])
            self.update_display()
    
    def drop(self, event=None):
        """Fait tomber la pièce instantanément"""
        if self.game.state != GameState.RUNNING or not self.human_player.current_piece:
            return
        
        # Déplacer la pièce vers le bas jusqu'à ce qu'elle ne puisse plus descendre
        while self.is_valid_position(self.human_player, row_offset=1):
            current_row, current_col = self.human_player.current_position
            self.human_player.current_position = (current_row + 1, current_col)
        
        # Placer la pièce
        self.place_piece(self.human_player)
        self.update_display()
    
    def toggle_pause(self, event=None):
        """Met le jeu en pause ou le reprend"""
        if self.game.state == GameState.RUNNING:
            self.game.state = GameState.PAUSED
        elif self.game.state == GameState.PAUSED:
            self.game.state = GameState.RUNNING
        
        self.update_display()
    
    def restart_game(self, event=None):
        """Redémarre le jeu"""
        # Réinitialiser les grilles
        self.human_player.grid = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.ai_player.grid = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        
        # Réinitialiser les scores
        self.human_player.score = 0
        self.human_player.lines_cleared = 0
        self.ai_player.score = 0
        self.ai_player.lines_cleared = 0
        
        # Réinitialiser les pièces
        self.human_player.current_piece = None
        self.human_player.next_piece = None
        self.ai_player.current_piece = None
        self.ai_player.next_piece = None
        
        # Réinitialiser les modificateurs de vitesse
        self.human_player.speed_modifier = 1.0
        self.human_player.speed_modifier_end_time = 0
        self.ai_player.speed_modifier = 1.0
        self.ai_player.speed_modifier_end_time = 0
        
        # Réinitialiser l'effet arc-en-ciel
        self.rainbow_mode = False
        
        # Réinitialiser les cadeaux surprises
        self.human_player.gift_next_piece = False
        self.ai_player.gift_next_piece = False
        
        # Réinitialiser l'état du jeu
        self.game.state = GameState.RUNNING
        self.game.start_time = time.time()
        self.game.last_rainbow_time = 0
        self.game.last_special_piece_time = {
            PlayerType.HUMAN: 0,
            PlayerType.AI: 0
        }
        
        # Réinitialiser l'IA
        TetrisAI.last_decision = None
        TetrisAI.decision_piece = None
        
        # Générer de nouvelles pièces pour les deux joueurs
        self.generate_new_piece(self.human_player)
        self.generate_new_piece(self.ai_player)
        
        # Réinitialiser le temps de chute
        self.last_fall_time = time.time()
        
        # Mettre à jour l'affichage
        self.update_display()
    
    def place_piece(self, player):
        """Place la pièce actuelle dans la grille"""
        if not player.current_piece:
            return
        
        # Obtenir les coordonnées de la pièce
        shape_coords = self.get_piece_coordinates(player)
        row_offset, col_offset = player.current_position
        
        # Placer chaque bloc de la pièce dans la grille
        for row, col in shape_coords:
            grid_row = row + row_offset
            grid_col = col + col_offset
            
            # Ne placer que si le bloc est dans la grille
            if 0 <= grid_row < GRID_HEIGHT and 0 <= grid_col < GRID_WIDTH:
                player.grid[grid_row][grid_col] = COLORS[player.current_piece]
        
        # Vérifier les lignes complètes
        lines_cleared = self.clear_lines(player)
        
        # Mettre à jour le score
        if lines_cleared > 0:
            # Système de score progressif
            if lines_cleared == 1:
                player.score += 50
            elif lines_cleared == 2:
                player.score += 100
                # Règle du cadeau surprise : si un joueur complète exactement 2 lignes
                # son adversaire reçoit une pièce facile lors de son prochain tour
                if player.type == PlayerType.HUMAN:
                    self.ai_player.gift_next_piece = True
                else:
                    self.human_player.gift_next_piece = True
            elif lines_cleared == 3:
                player.score += 200
            elif lines_cleared == 4:
                player.score += 300
            
            player.lines_cleared += lines_cleared
            
            # Vérifier si on doit activer la pause douceur (tous les 1000 points)
            if (player.score % 1000 < 50 and player.score > 0):
                # Ralentir les deux joueurs pendant 10 secondes
                self.human_player.speed_modifier = 0.5
                self.human_player.speed_modifier_end_time = time.time() + 10
                self.ai_player.speed_modifier = 0.5
                self.ai_player.speed_modifier_end_time = time.time() + 10
        
        # Vérifier si le jeu est terminé (si la pièce dépasse le haut de la grille)
        if row_offset <= 0:
            self.game.state = GameState.GAME_OVER
            return
        
        # Générer une nouvelle pièce
        self.generate_new_piece(player)
    
    def clear_lines(self, player):
        """Efface les lignes complètes et retourne le nombre de lignes effacées"""
        lines_cleared = 0
        
        # Vérifier chaque ligne de bas en haut
        for row in range(GRID_HEIGHT - 1, -1, -1):
            # Vérifier si la ligne est complète
            if all(player.grid[row]):
                lines_cleared += 1
                
                # Déplacer toutes les lignes au-dessus vers le bas
                for r in range(row, 0, -1):
                    player.grid[r] = player.grid[r - 1].copy()
                
                # Créer une nouvelle ligne vide en haut
                player.grid[0] = ['' for _ in range(GRID_WIDTH)]
        
        return lines_cleared
    
    def generate_new_piece(self, player):
        """Génère une nouvelle pièce pour un joueur"""
        # Utiliser la pièce suivante si elle existe
        if player.next_piece:
            player.current_piece = player.next_piece
        else:
            # Sinon, générer une pièce aléatoire
            player.current_piece = self.get_random_piece(player)
        
        # Générer la prochaine pièce
        player.next_piece = self.get_random_piece(player)
        
        # Réinitialiser la rotation et la position
        player.current_rotation = 0
        
        # Calculer la position initiale (centrer horizontalement)
        shape = SHAPES[player.current_piece][0]
        min_col = min(col for _, col in shape)
        max_col = max(col for _, col in shape)
        piece_width = max_col - min_col + 1
        col_offset = (GRID_WIDTH - piece_width) // 2
        
        player.current_position = (0, col_offset)
    
    def get_random_piece(self, player):
        """Retourne une pièce aléatoire en tenant compte des règles spéciales"""
        current_time = time.time()
        
        # Vérifier si le joueur doit recevoir une pièce facile (cadeau surprise)
        if player.gift_next_piece:
            player.gift_next_piece = False
            return random.choice(EASY_TETROMINOS)
        
        # Vérifier si on doit générer une pièce spéciale
        # (20% de chance tous les 3000 points, mais pas plus d'une fois toutes les 30 secondes)
        if (player.score >= self.game.special_piece_threshold and 
            current_time - self.game.last_special_piece_time[player.type] > 30 and
            random.random() < 0.2):
            self.game.last_special_piece_time[player.type] = current_time
            return random.choice(SPECIAL_TETROMINOS)
        
        # Sinon, générer une pièce standard
        return random.choice(STANDARD_TETROMINOS)
    
    def game_loop(self):
        """Boucle principale du jeu"""
        current_time = time.time()
        
        # Même en cas de Game Over, on continue à mettre à jour l'affichage
        # pour pouvoir détecter les touches de redémarrage
        if self.game.state == GameState.GAME_OVER:
            self.update_display()
            # Continuer la boucle de jeu pour détecter les touches
            self.root.after(self.game_tick, self.game_loop)
            return
        
        # Vérifier si le jeu est en cours
        if self.game.state == GameState.RUNNING:
            # Vérifier si on doit faire tomber les pièces
            elapsed_time = current_time - self.last_fall_time
            
            # Calculer la vitesse de chute pour chaque joueur en tenant compte du modificateur
            human_fall_time = self.fall_speed * self.human_player.speed_modifier
            ai_fall_time = self.fall_speed * self.ai_player.speed_modifier
            
            # Faire tomber la pièce du joueur humain
            if elapsed_time >= human_fall_time and self.human_player.current_piece:
                if self.is_valid_position(self.human_player, row_offset=1):
                    current_row, current_col = self.human_player.current_position
                    self.human_player.current_position = (current_row + 1, current_col)
                else:
                    self.place_piece(self.human_player)
                
                self.last_fall_time = current_time
            
            # Faire tomber la pièce de l'IA
            if elapsed_time >= ai_fall_time and self.ai_player.current_piece:
                if self.is_valid_position(self.ai_player, row_offset=1):
                    current_row, current_col = self.ai_player.current_position
                    self.ai_player.current_position = (current_row + 1, current_col)
                else:
                    self.place_piece(self.ai_player)
                
                self.last_fall_time = current_time
            
            # Vérifier si le mode arc-en-ciel doit être désactivé
            if self.rainbow_mode and current_time - self.game.last_rainbow_time >= 20:
                self.rainbow_mode = False
            
            # Vérifier si on doit activer l'effet arc-en-ciel (toutes les 2 minutes)
            game_duration = current_time - self.game.start_time
            if not self.rainbow_mode and game_duration > 0 and game_duration % 120 < 1 and current_time - self.game.last_rainbow_time > 120:
                self.rainbow_mode = True
                self.game.last_rainbow_time = current_time
        
        # Mettre à jour l'affichage
        self.update_display()
        
        # Planifier la prochaine mise à jour
        self.root.after(self.game_tick, self.game_loop)
    
    def ai_loop(self):
        """Boucle de l'IA"""
        while True:
            # Ne rien faire si le jeu est en pause ou terminé
            if self.game.state != GameState.RUNNING:
                time.sleep(0.1)
                continue
            
            # Ne rien faire si l'IA n'a pas de pièce actuelle
            if not self.ai_player.current_piece:
                time.sleep(0.1)
                continue
            
            # Obtenir le meilleur mouvement
            best_rotation, best_column, _ = TetrisAI.get_best_move(
                self.ai_player.grid,
                self.ai_player.current_piece,
                self.ai_player.current_rotation
            )
            
            # Appliquer la rotation
            while self.ai_player.current_rotation != best_rotation:
                if self.is_valid_position(self.ai_player, rotation_offset=1):
                    self.ai_player.current_rotation = (self.ai_player.current_rotation + 1) % len(SHAPES[self.ai_player.current_piece])
                else:
                    break
                time.sleep(0.1)
            
            # Obtenir la position actuelle
            _, current_col = self.ai_player.current_position
            
            # Déplacer vers la gauche ou la droite
            while current_col != best_column:
                if current_col < best_column:
                    # Déplacer vers la droite
                    if self.is_valid_position(self.ai_player, col_offset=1):
                        current_row, current_col = self.ai_player.current_position
                        self.ai_player.current_position = (current_row, current_col + 1)
                    else:
                        break
                else:
                    # Déplacer vers la gauche
                    if self.is_valid_position(self.ai_player, col_offset=-1):
                        current_row, current_col = self.ai_player.current_position
                        self.ai_player.current_position = (current_row, current_col - 1)
                    else:
                        break
                time.sleep(0.1)
            
            # Faire tomber la pièce
            while self.is_valid_position(self.ai_player, row_offset=1):
                current_row, current_col = self.ai_player.current_position
                self.ai_player.current_position = (current_row + 1, current_col)
                time.sleep(0.05)
            
            # Attendre un peu avant de recommencer
            time.sleep(0.5)