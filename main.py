import tkinter as tk
from game_state import GameState as game
from game_state import Info
from board_loader import BoardLoader
from gui_behavior import *


class ChessBoard(tk.Tk):
    def __init__(self, player_color:str = 'White'):
        super().__init__()
        self.title('Chess')
        self.geometry('550x550')
        self.resizable(1,1)
        self.config(bg='#282828')
        self.board_ui = [[None for x in range(8)] for y in range(8)]

        game.set_player(player_color)
        BoardLoader.create_board(self)
        Draw.draw_pieces(self)

        # DEVTOOL
        self.attack_indicator = False


    def bind_functions(self):
        self.canvas.bind('<ButtonPress-1>', lambda event: self.click_handler(event.y, event.x))
        self.canvas.bind('<ButtonRelease-1>', self.click_release)

    def unbind_functions(self):
        self.canvas.unbind('<ButtonPress-1>')
        self.canvas.unbind('<ButtonRelease-1>')


    def click_handler(self, raw_x, raw_y):
        if not Mouse.is_in_bounds(raw_x, raw_y):
            return

        x, y = (raw_x-4)//60, (raw_y-4)//60

        if Info.can_select(x, y) and Info.get(x,y).color == game.turn:
            Drag.start_drag(self, x, y)

        elif game.selected == Info.get(x,y):
            game.clear_selected()

        elif game.selected and Info.is_same_color(x, y):
            if not Drag.stop_drag():
                Drag.start_drag(self, x, y)

        elif (x,y) in Info.possible_moves():
            if game.process_action(x, y):
                Draw.draw_last_move(self)
                Draw.draw_indicator(self)
                if game.check_mate:
                    Draw.draw_elements(self)
                    self.board_ui[x][y].raise_piece()
                    self.unbind_functions()
                    return
            else:
                Draw.undo_draw_last_move(self)
            Drag.stop_drag()
            # DEVTOOL
            if self.attack_indicator:
                Draw.draw_attacks(self)

        elif game.selected and not Info.is_same_color(x, y):
            if not Drag.stop_drag():
                game.clear_selected()
                
        else:
            Drag.stop_drag()

        Draw.draw_elements(self)
        self.board_ui[x][y].raise_piece()


    def click_release(self, event):
        if game.selected is None:
            return
        
        if game.selected.pos == Mouse.get_mouse_pos(self, on_grid=True, invert=True):
            Drag.stop_drag()
            Draw.draw_pieces(self)
            game.select(*Mouse.get_mouse_pos(self, on_grid=True, invert=True))
        else:
            if Mouse.is_in_bounds(event.y, event.x):
                self.click_handler(event.y, event.x)




if __name__ == '__main__':
    ChessBoard().mainloop()