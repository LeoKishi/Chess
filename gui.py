import tkinter as tk
from image_canvas import *
from game_state import GameState as game
from logic import *

from SpriteLoader import SpriteSheet


class ChessBoard(tk.Tk):
    board_ui = [[None for x in range(8)] for y in range(8)]


    def __init__(self, player_color:str = 'White'):
        super().__init__()
        self.title('Chess')
        self.geometry('480x480')

        self.player = player_color
        self.highlights = list()
        self.indicators = list()
        
        self.create_images()
        self.create_board()
        

    def create_images(self):
        self.circle_img = CircleImage()
        self.dot_img = DotImage()
        self.indicator_img = IndicatorImage()
        self.lightbg_img = LightSquareImage()
        self.darkbg_img = DarkSquareImage()
        #self.hover_img = HoverImage()


    def create_board(self):
        self.canvas = tk.Canvas(self, height=480, width=480)
        self.canvas.pack()
        self.draw_grid()
        self.populate_board()
        self.draw_elements()

    # broken
    def bind_functions(self, *, click, release):
        pass
    
    # broken
    def drag_piece(self, x, y):
        if game.is_dragging:
            self.hover_img.set_image(game.selected.image)
            mouse_x, mouse_y = self.get_mouse_pos()
            self.hover_img.place(x=mouse_x-22, y=mouse_y-22)
            self.after(1000//60, self.drag_piece, *(x, y))


    def draw_grid(self):
        for x in range(8):
            for y in range(8):
                self.board_ui[x][y] = Square(self.canvas)
                self.board_ui[x][y].place(x*60, y*60)

    
    def draw_elements(self):
        for x in range(8):
            for y in range(8):
                self.draw_square(x, y)

        self.draw_highlight()
        self.draw_indicator()


    def draw_square(self, x, y):
        piece = game.get(x,y)

        if piece is None:
            img = ''
        else:
            img = piece.image

        self.board_ui[x][y].set_piece(img)

    # broken ?
    def draw_highlight(self):
        for x,y in self.highlights:
            self.board_ui[x][y].set_highlight('')

        if game.moves:
            for x,y in game.moves:
                self.board_ui[x][y].set_highlight(self.dot_img)
                self.highlights.append((x,y))

        if game.captures:
            for x,y in game.captures:
                self.board_ui[x][y].set_highlight(self.circle_img)
                self.highlights.append((x,y))

    # broken ?
    def draw_indicator(self):
        for x,y in self.indicators:
            self.board_ui[x][y].set_indicator('')

        if game.last_move:
            for x,y in game.last_move:
                self.board_ui[x][y].set_indicator(self.indicator_img)
                self.indicators.append((x,y))


    def set_board_color(self, player1):
        offset = 1 if player1 == 'White' else 0

        for x in range(8):
            for y in range(8):
                if (x+y+offset) % 2 == 0:
                    self.board_ui[x][y].set_bg(self.lightbg_img)
                else:
                    self.board_ui[x][y].set_bg(self.darkbg_img)


    def populate_board(self):
        player1 = self.player
        player2 = 'Black' if player1 == 'White' else 'White'
        self.set_board_color(player1)

        def new_piece(piece_type, color, pos):
            game.board[pos[0]][pos[1]] = piece_type(color, pos)

        for y in range(8):
            new_piece(Pawn, player2, (1,y))
            new_piece(Pawn, player1, (6,y))

        new_piece(Pawn, player2, (5,2))

        new_piece(Rook, player2, (0,0))
        new_piece(Rook, player2, (0,7))
        new_piece(Rook, player1, (7,0))
        new_piece(Rook, player1, (7,7))

        new_piece(Knight, player2, (0,1))
        new_piece(Knight, player2, (0,6))
        new_piece(Knight, player1, (7,1))
        new_piece(Knight, player1, (7,6))

        new_piece(Bishop, player2, (0,2))
        new_piece(Bishop, player2, (0,5))
        new_piece(Bishop, player1, (7,2))
        new_piece(Bishop, player1, (7,5))

        offset = 1 if player1 == 'Black' else 0

        new_piece(Queen, player2, (0,3+offset))
        new_piece(Queen, player1, (7,3+offset))

        new_piece(King, player2, (0,4-offset))
        new_piece(King, player1, (7,4-offset))


    def get_mouse_pos(self) -> tuple:
        x = self.winfo_pointerx() - self.winfo_rootx()
        y = self.winfo_pointery() - self.winfo_rooty()
        return (x, y)