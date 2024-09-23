import tkinter as tk
from image_canvas import ImageCanvas, BlankImage
from game_state import GameState as gs
from logic import *


class Display(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Chess')
        self.board_ui = [[None for row in range(8)] for col in range(8)]
        self.blank = BlankImage()

        self.create_board()
        self.set_board_color('#d4d4d4', 'white')
        self.populate_board(player1='White')
        self.update_board()

    
    def create_board(self):
        for row in range(8):
            for col in range(8):
                self.board_ui[row][col] = ImageCanvas(self, height=70, width=70, bg='#d5ebde')
                self.board_ui[row][col].bind('<Button-1>', lambda event=None, x=row, y=col: self.handler(x,y))
                self.board_ui[row][col].pack_propagate(0)
                self.board_ui[row][col].grid(row=row, column=col)


    def set_board_color(self, color1, color2):
        for row in range(8):
            for col in range(8):
                if (row+col) % 2 != 0:
                    self.board_ui[row][col].set_color(color1)
                else:
                    self.board_ui[row][col].set_color(color2)


    def handler(self, x, y):
        if gs.selected is None:
            if gs.board[x][y] is None:
                return
            gs.selected = gs.board[x][y]
            gs.find_possible_actions(x, y)

        else:
            gs.process_action(x,y)

        self.update_board()
    

    def update_board(self):
        for row in range(8):
            for col in range(8):
                piece = gs.board[row][col]

                if piece is None:
                    img = self.blank
                elif piece.color == 'White':
                    img = piece.white_img
                else:
                    img = piece.black_img

                self.board_ui[row][col].set_image(img)


    def populate_board(self, player1:str):
        player2 = 'Black' if player1 == 'White' else 'White'

        for col in range(8):
            self.new_piece(Pawn, player2, (1,col))
            self.new_piece(Pawn, player1, (6,col))

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

        self.new_piece(Queen, player2, (0,3))
        self.new_piece(Queen, player1, (7,3))

        self.new_piece(King, player2, (0,4))
        self.new_piece(King, player1, (7,4))


    def new_piece(self, piece_type, color, pos):
        gs.board[pos[0]][pos[1]] = piece_type(color, pos)
        piece = gs.board[pos[0]][pos[1]]

        if color == 'White':
            img = piece.white_img
        else:
            img = piece.black_img

        piece.tklabel = tk.Label(self.board_ui[pos[0]][pos[1]], image=img)




Display().mainloop()