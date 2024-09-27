import tkinter as tk
from piece_behavior import *
from game_state import GameState as game
from game_state import Util


class BoardLoader:

    @staticmethod
    def create_board(root):
        root.canvas = tk.Canvas(root, height=480, width=480)
        root.canvas.pack()
        BoardLoader.load_images(root)
        BoardLoader.create_grid(root)
        BoardLoader.populate_board(root)
        BoardLoader.set_board_color(root)
        root.bind_functions()

    @staticmethod
    def load_images(root):
        root.lightbg_img = tk.PhotoImage(file='assets/light_square.png')
        root.darkbg_img = tk.PhotoImage(file='assets/dark_square.png')
        root.circle_img = tk.PhotoImage(file='assets/circle.png')
        root.dot_img = tk.PhotoImage(file='assets/dot.png')
        root.indicator_img = tk.PhotoImage(file='assets/indicator.png')
        root.hover_img = tk.PhotoImage(file='assets/hover.png')
        root.attack_img = tk.PhotoImage(file='assets/attack.png')

    @staticmethod
    def create_grid(root):
        for x, y in Util.range2d():
            root.board_ui[x][y] = Square(root.canvas)

    @staticmethod
    def set_board_color(root):
        offset = 1 if root.player == 'White' else 0

        for x, y in Util.range2d():
            if (x+y+offset) % 2 == 0:
                root.board_ui[x][y].set_bg(root.lightbg_img)
            else:
                root.board_ui[x][y].set_bg(root.darkbg_img)

    @staticmethod
    def populate_board(root):
        player1 = root.player
        player2 = 'Black' if player1 == 'White' else 'White'

        def new_piece(piece_type, color, pos):
            game.board[pos[0]][pos[1]] = piece_type(color, pos)

        for y in range(8):
            #new_piece(Pawn, player2, (1,y))
            #new_piece(Pawn, player1, (6,y))
            pass

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




class Square:
    def __init__(self, canvas):
        self.canvas = canvas

        def new_image():
            return canvas.create_image(60, 60, anchor='nw')

        self.bg = new_image()
        self.highlight = new_image()
        self.hover = new_image()
        self.piece = new_image()
        self.indicator = new_image()
        # DEVTOOL
        self.attack = new_image()

        self.elements = [self.bg,
                         self.highlight,
                         self.indicator,
                         self.hover,
                         self.piece,
                         # DEVTOOL
                         self.attack]
        

    def move(self, mouse_x, mouse_y):
        self.canvas.moveto(self.piece, mouse_x-30, mouse_y-30)
        
    def raise_piece(self):
        self.canvas.tag_raise(self.piece)

    def place(self, x, y):
        for elem in self.elements:
            self.canvas.moveto(elem, y, x)
    
    def set_bg(self, img):
        self.canvas.itemconfig(self.bg, image=img)

    def set_highlight(self, img):
        self.canvas.itemconfig(self.highlight, image=img)
        self.canvas.tag_raise(self.highlight)

    def set_indicator(self, img):
        self.canvas.itemconfig(self.indicator, image=img)

    def set_hover(self, img):
        self.canvas.itemconfig(self.hover, image=img)

    def set_piece(self, img):
        self.canvas.itemconfig(self.piece, image=img)

    # DEVTOOL
    def set_attack(self, img):
        self.canvas.itemconfig(self.attack, image=img)
