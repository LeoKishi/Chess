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
        self.gui.bind_functions(click=self.click_handler,
                                release=self.click_release)
        self.gui.mainloop()


    def click_handler(self, x, y):
        if game.can_select(x, y) and game.color(x,y) == self.gui.player:
            game.select(x, y)

        elif game.selected == game.get(x,y):
            game.clear_selected()

        elif game.can_change_selection(x, y):
            game.select(x, y)
            
        else:
            game.process_action(x, y)

        if game.selected:
            game.is_dragging = True
            #self.gui.drag_piece(x, y)

        self.gui.draw_elements()


    def click_release(self, x, y):
        game.is_dragging = False



Chess()