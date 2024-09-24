import tkinter as tk
from user_interface import ChessBoard
from game_state import GameState as game


# TODO:
# ======= logic =======
# Rook logic
# Knight logic
# bishop logc
# queen logic
# king logic
# checking mechanic
# discovered check mechanic
# check mate
# castling
# en passant mechanic
# pawn promotion

# ======= extra =======
# timer
# stockfish bot
# evaluation
# review



class Chess:
    gui = ChessBoard(player_color='White')


    def __init__(self):

        self.gui.mainloop()









Chess()