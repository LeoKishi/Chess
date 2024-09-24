import tkinter as tk
from image_canvas import *
from game_state import GameState as gs
from logic import *


class ChessBoard(tk.Tk):
    board_ui = [[None for x in range(8)] for y in range(8)]


    def __init__(self, player_color:str = 'White'):
        super().__init__()
        self.title('Chess')
        self.circle_img = CircleImage()
        self.dot_img = DotImage()
        self.indicator_img = IndicatorImage()
        self.player = player_color
        self.highlights = list()
        self.indicators = list()
        self.create_board()


    def create_board(self):
        self.draw_grid()
        self.populate_board()
        self.draw_elements()


    def bind_to_squares(self, func):
        for x in range(8):
            for y in range(8):
                self.board_ui[x][y].bind('<Button-1>', lambda event=None, x=x, y=y: func(x,y))
    

    def draw_grid(self):
        for x in range(8):
            for y in range(8):
                self.board_ui[x][y] = ImageCanvas(self, height=50, width=50, bg='#d5ebde')
                self.board_ui[x][y].bind('<Button-1>', lambda event=None, x=x, y=y: self.click_handler(x,y))
                self.board_ui[x][y].pack_propagate(0)
                self.board_ui[x][y].grid(row=x, column=y)
    

    def draw_elements(self):
        for x in range(8):
            for y in range(8):
                self.draw_square(x, y)

        self.draw_highlight()
        self.draw_indicator()


    def draw_square(self, x, y):
        piece = gs.get(x,y)

        if piece is None:
            img = ''
        elif piece.color == 'White':
            img = piece.white_img
        else:
            img = piece.black_img

        self.board_ui[x][y].set_image(img)


    def draw_highlight(self):
        for x,y in self.highlights:
            self.board_ui[x][y].set_highlight('')

        if gs.moves:
            for x,y in gs.moves:
                self.board_ui[x][y].set_highlight(self.dot_img)
                self.highlights.append((x,y))

        if gs.captures:
            for x,y in gs.captures:
                self.board_ui[x][y].set_highlight(self.circle_img)
                self.highlights.append((x,y))


    def draw_indicator(self):
        for x,y in self.indicators:
            self.board_ui[x][y].set_indicator('')

        if gs.last_move:
            for x,y in gs.last_move:
                self.board_ui[x][y].set_indicator(self.indicator_img)
                self.indicators.append((x,y))


    def set_board_color(self, player1, color1, color2):
        offset = 1 if player1 == 'White' else 0

        for x in range(8):
            for y in range(8):
                if (x+y+offset) % 2 == 0:
                    self.board_ui[x][y].set_color(color1)
                else:
                    self.board_ui[x][y].set_color(color2)


    def populate_board(self):
        player1 = self.player
        player2 = 'Black' if player1 == 'White' else 'White'
        self.set_board_color(player1, '#d4d4d4', 'white')

        for y in range(8):
            self.new_piece(Pawn, player2, (1,y))
            self.new_piece(Pawn, player1, (6,y))

        self.new_piece(Pawn, player2, (5,2))

        self.new_piece(Rook, player2, (0,0))
        self.new_piece(Rook, player2, (0,7))
        self.new_piece(Rook, player1, (7,0))
        self.new_piece(Rook, player1, (7,7))

        self.new_piece(Knight, player2, (0,1))
        self.new_piece(Knight, player2, (0,6))
        self.new_piece(Knight, player1, (7,1))
        self.new_piece(Knight, player1, (7,6))

        self.new_piece(Bishop, player2, (0,2))
        self.new_piece(Bishop, player2, (0,5))
        self.new_piece(Bishop, player1, (7,2))
        self.new_piece(Bishop, player1, (7,5))

        offset = 1 if player1 == 'Black' else 0

        self.new_piece(Queen, player2, (0,3+offset))
        self.new_piece(Queen, player1, (7,3+offset))

        self.new_piece(King, player2, (0,4-offset))
        self.new_piece(King, player1, (7,4-offset))


    def new_piece(self, piece_type, color, pos):
        gs.board[pos[0]][pos[1]] = piece_type(color, pos)
