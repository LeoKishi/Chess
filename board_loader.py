import tkinter as tk
from piece_behavior import *
from game_state import GameState as game
from game_state import Util
from dragFrame import DragFrame
from gui_behavior import Command
from gui_behavior import Draw


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
        BoardLoader.load_selectors(root)

    @staticmethod
    def load_selectors(root):
        root.w_selector = Selector(root.canvas, 'White')
        root.b_selector = Selector(root.canvas, 'Black')

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

        self.elements = [self.bg,
                         self.highlight,
                         self.indicator,
                         self.hover,
                         self.piece]
        

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




class Selector:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.color = color
        self.pos = None
        self.load_image(color)

        self.selector = self.new_image(self.selector_img)
        self.hover = self.new_image(self.hover_img)
        self.queen = self.new_image(self.queen_img)
        self.knight = self.new_image(self.knight_img)
        self.rook = self.new_image(self.rook_img)
        self.bishop = self.new_image(self.bishop_img)

        self.elements = [self.queen, self.knight, self.rook, self.bishop]
        
        if color != game.player:
            self.elements = self.elements[::-1]
        
        self.bind_events()

    def set_pos(self, x, y):
        self.pos = (x, y)

    def place(self, x, y):
        x, y = (x*60)+4, (y*60)+4
        offset = 0
        self.canvas.moveto(self.selector, y-6, x-6)
        for elem in self.elements:
            self.canvas.moveto(elem, y, x+offset)
            offset += 60
        self.show()
    
    def load_image(self, color):
        loader = SpriteSheet(file='assets/ChessPiecesArray.png')
        row = 1 if color == 'White' else 0
        self.queen_img = loader.get_sprite((60,60), (row,0))
        self.knight_img = loader.get_sprite((60,60), (row,3))
        self.rook_img = loader.get_sprite((60,60), (row,2))
        self.bishop_img = loader.get_sprite((60,60), (row,4))
        self.selector_img = tk.PhotoImage(file='assets/selector.png')
        self.hover_img = tk.PhotoImage(file='assets/selector_hover.png')

    def new_image(self, img):
        return self.canvas.create_image(0, 0, anchor='nw', image=img, state='hidden')

    def bind_events(self):
        for i in self.elements:
            self.canvas.tag_bind(i, '<Enter>', lambda event, i=i: self.show_hover(i))
            self.canvas.tag_bind(i, '<ButtonPress-1>', lambda event, i=i: self.action(i-self.queen))

    def show_hover(self, elem):
        x, y = self.canvas.coords(elem)
        self.canvas.moveto(self.hover, x, y)
        self.canvas.itemconfigure(self.hover, state='normal')

    def action(self, option):
        self.hide()
        self.canvas.winfo_toplevel().bind_functions()
        game.selected = [Queen, Knight, Rook, Bishop][option](self.color, self.pos)
        x, y = self.pos
        game.board[x][y] = None
        Command.try_process(self.canvas.winfo_toplevel(), x, y)
        Draw.draw_elements(self.canvas.winfo_toplevel())

    def hide(self):
        for i in range(7):
            self.canvas.itemconfigure(self.selector+i, state='hidden')

    def show(self):
        for i in [self.selector, self.hover] + self.elements:
            self.canvas.itemconfigure(i, state='normal')
            self.canvas.tag_raise(i)