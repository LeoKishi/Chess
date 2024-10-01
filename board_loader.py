import tkinter as tk
from piece_behavior import *
from game_state import GameState as game
from game_state import Util
from dragFrame import DragFrame


class BoardLoader:

    @staticmethod
    def create_board(root):
        frame = DragFrame(root, height=550, width=550, bg='#282828')
        frame.pack()
        root.canvas = tk.Canvas(frame, height=488, width=488, highlightthickness=0)
        root.canvas.place(anchor='center', relx=0.5, rely=0.5)
        BoardLoader.load_images(root)
        BoardLoader.create_grid(root)
        BoardLoader.populate_board()
        BoardLoader.set_board_color(root)
        root.bind_functions()
        BoardLoader.load_border(root)

    @staticmethod
    def load_border(root):
        img = root.w_border_img if game.player == 'White' else root.b_border_img
        a = root.canvas.create_image(488, 488, anchor='nw', image=img)
        root.canvas.moveto(a, 0, 0)

    @staticmethod
    def load_images(root):
        root.lightbg_img = tk.PhotoImage(file='assets/light_square.png')
        root.darkbg_img = tk.PhotoImage(file='assets/dark_square.png')
        root.circle_img = tk.PhotoImage(file='assets/circle.png')
        root.dot_img = tk.PhotoImage(file='assets/dot.png')
        root.indicator_img = tk.PhotoImage(file='assets/indicator.png')
        root.hover_img = tk.PhotoImage(file='assets/hover.png')
        root.attack_img = tk.PhotoImage(file='assets/attack.png')
        root.w_border_img = tk.PhotoImage(file='assets/white_border.png')
        root.b_border_img = tk.PhotoImage(file='assets/black_border.png')

    @staticmethod
    def create_grid(root):
        for x, y in Util.range2d():
            root.board_ui[x][y] = Square(root.canvas)

    @staticmethod
    def set_board_color(root):
        offset = 0 if game.player == 'White' else 1

        for x, y in Util.range2d():
            if (x+y+offset) % 2 == 0:
                root.board_ui[x][y].set_bg(root.lightbg_img)
            else:
                root.board_ui[x][y].set_bg(root.darkbg_img)

    @staticmethod
    def populate_board():
        game.pieces = [Pawn, Rook, Knight, Bishop, Queen, King]
        game.populate_board()




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
