#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Intelligence artificielle pour le jeu Tetris
"""

import random
import copy
import time
from typing import List, Tuple, Dict
from constants import GRID_WIDTH, GRID_HEIGHT, SHAPES

class TetrisAI:
    """Classe d'intelligence artificielle pour Tetris"""
    
    # Mémoriser la décision pour éviter les changements de dernière minute
    last_decision = None
    decision_piece = None
    
    @staticmethod
    def get_best_move(grid: List[List[str]], piece_type: str, current_rotation: int) -> Tuple[int, int, int]:
        """
        Détermine le meilleur mouvement pour la pièce actuelle
        Retourne (rotation, colonne, score)
        """
        # Si c'est la même pièce et que nous avons déjà pris une décision, la maintenir
        if TetrisAI.decision_piece == piece_type and TetrisAI.last_decision is not None:
            return TetrisAI.last_decision
        
        best_score = float('-inf')
        best_rotation = current_rotation
        best_column = 0
        
        # Essayer toutes les rotations possibles
        for rotation in range(len(SHAPES[piece_type])):
            shape = SHAPES[piece_type][rotation]
            
            # Calculer la largeur et la hauteur de la pièce
            min_col = min(col for _, col in shape)
            max_col = max(col for _, col in shape)
            min_row = min(row for row, _ in shape)
            max_row = max(row for row, _ in shape)
            piece_width = max_col - min_col + 1
            
            # Essayer toutes les positions horizontales possibles
            for col in range(-min_col, GRID_WIDTH - max_col):
                # Créer une copie de la grille pour simulation
                test_grid = copy.deepcopy(grid)
                
                # Simuler la chute de la pièce
                row = 0
                while TetrisAI._is_valid_position(test_grid, piece_type, rotation, row + 1, col):
                    row += 1
                
                # Si la pièce est placée trop haut, c'est un mauvais mouvement
                if row < 2:
                    continue
                
                # Placer la pièce dans la grille de test
                TetrisAI._place_piece(test_grid, piece_type, rotation, row, col)
                
                # Effacer les lignes complètes
                lines_cleared = TetrisAI._clear_lines(test_grid)
                
                # Évaluer la position
                score = TetrisAI._evaluate_position(test_grid, lines_cleared)
                
                # Mettre à jour le meilleur mouvement si nécessaire
                if score > best_score:
                    best_score = score
                    best_rotation = rotation
                    best_column = col
        
        # Mémoriser la décision pour cette pièce
        TetrisAI.last_decision = (best_rotation, best_column, best_score)
        TetrisAI.decision_piece = piece_type
        
        return best_rotation, best_column, best_score
    
    @staticmethod
    def _is_valid_position(grid: List[List[str]], piece_type: str, rotation: int, row: int, col: int) -> bool:
        """Vérifie si la position est valide pour une pièce"""
        shape = SHAPES[piece_type][rotation]
        
        for block_row, block_col in shape:
            grid_row = row + block_row
            grid_col = col + block_col
            
            # Vérifier si le bloc est en dehors de la grille
            if grid_row < 0 or grid_row >= GRID_HEIGHT or grid_col < 0 or grid_col >= GRID_WIDTH:
                return False
            
            # Vérifier si le bloc entre en collision avec une cellule occupée
            if grid_row >= 0 and grid[grid_row][grid_col]:
                return False
        
        return True
    
    @staticmethod
    def _place_piece(grid: List[List[str]], piece_type: str, rotation: int, row: int, col: int) -> None:
        """Place une pièce dans la grille"""
        shape = SHAPES[piece_type][rotation]
        
        for block_row, block_col in shape:
            grid_row = row + block_row
            grid_col = col + block_col
            
            if 0 <= grid_row < GRID_HEIGHT and 0 <= grid_col < GRID_WIDTH:
                grid[grid_row][grid_col] = piece_type
    
    @staticmethod
    def _clear_lines(grid: List[List[str]]) -> int:
        """Efface les lignes complètes et retourne le nombre de lignes effacées"""
        lines_cleared = 0
        new_grid = copy.deepcopy(grid)
        
        # Vérifier chaque ligne de bas en haut
        for row in range(GRID_HEIGHT - 1, -1, -1):
            # Vérifier si la ligne est complète
            if all(cell for cell in new_grid[row]):
                lines_cleared += 1
                
                # Déplacer toutes les lignes au-dessus vers le bas
                for r in range(row, 0, -1):
                    new_grid[r] = new_grid[r - 1].copy()
                
                # Créer une nouvelle ligne vide en haut
                new_grid[0] = ['' for _ in range(GRID_WIDTH)]
        
        # Mettre à jour la grille originale
        for row in range(GRID_HEIGHT):
            grid[row] = new_grid[row].copy()
        
        return lines_cleared
    
    @staticmethod
    def _evaluate_position(grid: List[List[str]], lines_cleared: int) -> float:
        """Évalue une position de jeu"""
        # Paramètres d'évaluation optimisés
        aggregate_height_weight = -0.510066
        complete_lines_weight = 0.760666
        holes_weight = -0.35663
        bumpiness_weight = -0.184483
        
        # Nouveaux paramètres
        well_weight = 0.3  # Favoriser les "puits" pour les pièces I
        top_row_penalty = -1.0  # Pénaliser fortement les pièces trop hautes
        deep_well_bonus = 0.2  # Bonus pour les puits profonds
        
        # Calculer les métriques
        heights = TetrisAI._get_heights(grid)
        aggregate_height = sum(heights)
        holes = TetrisAI._get_holes(grid, heights)
        bumpiness = TetrisAI._get_bumpiness(heights)
        wells = TetrisAI._get_wells(heights)
        top_row_blocks = TetrisAI._get_top_row_blocks(grid)
        deep_wells = TetrisAI._get_deep_wells(heights)
        
        # Calculer le score
        score = (
            aggregate_height_weight * aggregate_height +
            complete_lines_weight * lines_cleared +
            holes_weight * holes +
            bumpiness_weight * bumpiness +
            well_weight * wells +
            top_row_penalty * top_row_blocks +
            deep_well_bonus * deep_wells
        )
        
        # Bonus pour les lignes complètes
        if lines_cleared > 0:
            score += lines_cleared * lines_cleared * 10
        
        return score
    
    @staticmethod
    def _get_heights(grid: List[List[str]]) -> List[int]:
        """Calcule la hauteur de chaque colonne"""
        heights = [0] * GRID_WIDTH
        
        for col in range(GRID_WIDTH):
            for row in range(GRID_HEIGHT):
                if grid[row][col]:
                    heights[col] = GRID_HEIGHT - row
                    break
        
        return heights
    
    @staticmethod
    def _get_holes(grid: List[List[str]], heights: List[int]) -> int:
        """Compte le nombre de trous dans la grille"""
        holes = 0
        
        for col in range(GRID_WIDTH):
            if heights[col] == 0:
                continue
            
            # Trouver la première cellule occupée
            top_block_row = None
            for row in range(GRID_HEIGHT):
                if grid[row][col]:
                    top_block_row = row
                    break
            
            if top_block_row is None:
                continue
            
            # Compter les trous en dessous
            for row in range(top_block_row + 1, GRID_HEIGHT):
                if not grid[row][col] and row < GRID_HEIGHT:
                    # Vérifier s'il y a un bloc au-dessus
                    has_block_above = False
                    for r in range(row - 1, -1, -1):
                        if grid[r][col]:
                            has_block_above = True
                            break
                    
                    if has_block_above:
                        holes += 1
        
        return holes
    
    @staticmethod
    def _get_bumpiness(heights: List[int]) -> int:
        """Calcule l'irrégularité de la surface"""
        bumpiness = 0
        
        for i in range(GRID_WIDTH - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        
        return bumpiness
    
    @staticmethod
    def _get_wells(heights: List[int]) -> int:
        """Calcule le nombre de puits (colonnes entourées de colonnes plus hautes)"""
        wells = 0
        
        # Vérifier les colonnes intérieures
        for i in range(1, GRID_WIDTH - 1):
            if heights[i] < heights[i-1] - 1 and heights[i] < heights[i+1] - 1:
                wells += 1
        
        # Vérifier les colonnes aux bords
        if heights[0] < heights[1] - 1:
            wells += 1
        if heights[GRID_WIDTH-1] < heights[GRID_WIDTH-2] - 1:
            wells += 1
        
        return wells
    
    @staticmethod
    def _get_deep_wells(heights: List[int]) -> int:
        """Calcule le nombre de puits profonds (au moins 3 blocs de profondeur)"""
        deep_wells = 0
        
        # Vérifier les colonnes intérieures
        for i in range(1, GRID_WIDTH - 1):
            if heights[i] + 3 <= min(heights[i-1], heights[i+1]):
                deep_wells += 1
        
        # Vérifier les colonnes aux bords
        if heights[0] + 3 <= heights[1]:
            deep_wells += 1
        if heights[GRID_WIDTH-1] + 3 <= heights[GRID_WIDTH-2]:
            deep_wells += 1
        
        return deep_wells
    
    @staticmethod
    def _get_top_row_blocks(grid: List[List[str]]) -> int:
        """Compte le nombre de blocs dans les 4 premières lignes"""
        top_blocks = 0
        
        for row in range(4):
            for col in range(GRID_WIDTH):
                if grid[row][col]:
                    top_blocks += 1
        
        return top_blocks