#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tetris à deux joueurs (Humain vs IA)
Développé avec Python et Tkinter
"""

import tkinter as tk
from game import TetrisGame

def main():
    """Fonction principale"""
    # Créer la fenêtre principale
    root = tk.Tk()
    
    # Créer le jeu
    game = TetrisGame(root)
    
    # Lancer la boucle principale
    root.mainloop()

if __name__ == "__main__":
    main() 