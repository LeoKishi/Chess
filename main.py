import tkinter as tk
from gui import ChessBoard
from game_state import GameState as game


# TODO:
# ======= GUI =======
# Drag piece by holding click
# Highlight square that the piece is hovering
# Place piece in square if it is a valid move

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